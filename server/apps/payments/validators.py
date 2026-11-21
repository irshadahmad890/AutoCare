from rest_framework.exceptions import ValidationError

def validate_discount(discount, subtotal):
    if discount > subtotal:
        raise ValidationError({'discount': 'Discount cannot be greater than the subtotal.'})

def validate_payment_amount(amount, balance_due):
    if amount <= 0:
        raise ValidationError({'amount': 'Payment amount must be greater than zero.'})
    if amount > balance_due:
        raise ValidationError({'amount': 'Payment cannot be greater than the remaining balance.'})
