
from decimal import Decimal

from rest_framework import serializers

from .models import Invoice, Payment, PaymentMethod
from .validators import validate_discount, validate_payment_amount


class InvoiceSerializer(serializers.ModelSerializer):

    amount_paid = serializers.DecimalField(max_digits = 12, decimal_places = 2, read_only = True)
    balance_due = serializers.DecimalField(max_digits = 12, decimal_places = 2, read_only = True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'job', 'status',
            'parts_total', 'labor_total', 'subtotal',
            'discount', 'tax_percent', 'tax_amount', 'total',
            'amount_paid', 'balance_due',
            'issued_at', 'due_date', 'paid_at',
            'issued_by', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class GenerateInvoiceSerializer(serializers.Serializer):

    discount = serializers.DecimalField(max_digits = 12, decimal_places = 2, default = Decimal('0.00'), min_value = 0)
    tax_percent = serializers.DecimalField(max_digits = 5, decimal_places = 2, default = Decimal('0.00'), min_value = 0, max_value = 100)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id', 'receipt_number', 'invoice', 'amount',
            'method', 'reference', 'paid_at',
            'received_by', 'created_at'
        ]
        read_only_fields = fields


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['amount', 'method', 'reference']

    def validate_amount(self, value):
        invoice = self.context['invoice']
        validate_payment_amount(value, invoice.balance_due)
        return value
