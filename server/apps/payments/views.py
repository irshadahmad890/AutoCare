from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from apps.user.models import Role
from .models import Invoice, Payment
from .serializers import (
    InvoiceSerializer,
    GenerateInvoiceSerializer,
    PaymentSerializer,
    PaymentCreateSerializer
)
from apps.common.permissions import IsAdmin, IsAdminOrInvoiceCustomer
from .services import generate_invoice, record_payment

@extend_schema(tags=['Invoices'])
class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInvoiceCustomer]

    def get_queryset(self):
        user = self.request.user
        queryset = Invoice.objects.select_related('job', 'job__vehicle', 'job__vehicle__customer').prefetch_related('payments')
        if not user.is_authenticated:
            return queryset.none()
        if getattr(user, 'role', None) == Role.ADMIN:
            return queryset
        return queryset.filter(job__vehicle__customer__user = user)

@extend_schema(tags=['Invoices'])
class InvoiceDetailView(generics.RetrieveAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInvoiceCustomer]

    def get_queryset(self):
        user = self.request.user
        queryset = Invoice.objects.select_related('job', 'job__vehicle', 'job__vehicle__customer').prefetch_related('payments')
        if getattr(user, 'role', None) == Role.ADMIN:
            return queryset
        return queryset.filter(job__vehicle__customer__user = user)


class GenerateInvoiceView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        tags=['Invoices'], request=GenerateInvoiceSerializer,
        responses={201: InvoiceSerializer},
    )
    def post(self, request, job_pk):
        serializer = GenerateInvoiceSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        invoice = generate_invoice(
            job_id = job_pk,
            issued_by = request.user,
            discount = serializer.validated_data['discount'],
            tax_percent = serializer.validated_data['tax_percent']
        )

        return Response(
            InvoiceSerializer(invoice).data,
            status = status.HTTP_201_CREATED
        )


class RecordPaymentView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInvoiceCustomer]

    def get_invoice(self, request, pk):
        queryset = Invoice.objects.select_related(
            'job', 'job__vehicle', 'job__vehicle__customer'
        )

        if request.user.role == Role.CUSTOMER:
            queryset = queryset.filter(job__vehicle__customer__user = request.user)
        invoice = get_object_or_404(queryset, pk = pk)
        self.check_object_permissions(request, invoice)
        return invoice

    @extend_schema(tags=['Payments'], responses={200: PaymentSerializer(many=True)})
    def get(self, request, pk):
        invoice = self.get_invoice(request, pk)
        payments = invoice.payments.select_related('received_by')
        return Response(PaymentSerializer(payments, many = True).data)

    @extend_schema(
        tags=['Payments'], request=PaymentCreateSerializer,
        responses={201: PaymentSerializer},
    )
    def post(self, request, pk):
        if request.user.role != Role.ADMIN:
            raise PermissionDenied("Only Admin can record payments.")
        invoice = self.get_invoice(request, pk)
        serializer = PaymentCreateSerializer(
            data = request.data,
            context = {'invoice': invoice}
        )
        serializer.is_valid(raise_exception = True)

        payment = record_payment(
            invoice_id = invoice.pk,
            amount = serializer.validated_data['amount'],
            method = serializer.validated_data['method'],
            reference = serializer.validated_data['reference'],
            received_by = request.user
        )

        return Response(
            PaymentSerializer(payment).data,
            status = status.HTTP_201_CREATED
        )


@extend_schema(tags=['Payments'])
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInvoiceCustomer]

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.select_related(
            'invoice', 'invoice__job', 'invoice__job__vehicle',
            'invoice__job__vehicle__customer', 'received_by'
        )
        if not user.is_authenticated:
            return queryset.none()

        if getattr(user, 'role', None) == Role.ADMIN:
            return queryset

        return queryset.filter(
            invoice__job__vehicle__customer__user = user
        )


@extend_schema(tags=['Payments'])
class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInvoiceCustomer]

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.select_related(
            'invoice', 'invoice__job', 'invoice__job__vehicle',
            'invoice__job__vehicle__customer', 'received_by'
        )
        if getattr(user, 'role', None) == Role.ADMIN:
            return queryset
        return queryset.filter(
            invoice__job__vehicle__customer__user = user
        )


class InvoicePrintView(InvoiceDetailView):
    """Server-rendered, print-friendly invoice; access rules match the API."""

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        invoice = Invoice.objects.select_related(
            'job__vehicle__customer', 'issued_by'
        ).prefetch_related('job__used_parts__part', 'job__mechanic_assignments__mechanic').get(pk=invoice.pk)
        return TemplateResponse(request, 'payments/invoice_print.html', {'invoice': invoice})


class ReceiptPrintView(PaymentDetailView):
    """Server-rendered, print-friendly payment receipt."""

    def get(self, request, *args, **kwargs):
        payment = self.get_object()
        payment = Payment.objects.select_related(
            'invoice__job__vehicle__customer', 'received_by'
        ).get(pk=payment.pk)
        return TemplateResponse(request, 'payments/receipt_print.html', {'payment': payment})
