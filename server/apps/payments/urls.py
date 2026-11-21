from django.urls import path

from . import views

urlpatterns = [
    # Invoice APIs
    path('invoices/', views.InvoiceListView.as_view(), name = 'invoice-list'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name = 'invoice-detail'),
    path('invoices/<int:pk>/print/', views.InvoicePrintView.as_view(), name = 'invoice-print'),

    # Generate invoice from job
    path('jobs/<int:job_pk>/generate-invoice/', views.GenerateInvoiceView.as_view(), name = 'job-generate-invoice'),

    # Payment APIs
    path('invoices/<int:pk>/payments/', views.RecordPaymentView.as_view(), name = 'invoice-payments'),
    path('receipts/', views.PaymentListView.as_view(), name = 'receipt-list'),
    path('receipts/<int:pk>/', views.PaymentDetailView.as_view(), name = 'receipt-detail'),
    path('receipts/<int:pk>/print/', views.ReceiptPrintView.as_view(), name = 'receipt-print'),
]
