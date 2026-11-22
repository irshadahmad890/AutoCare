from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.user.models import Role
from apps.payments.models import Invoice

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.CUSTOMER

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ADMIN


class IsAdminOrMechanicReadOnly(BasePermission):
    """Inventory is editable by admins; mechanics need catalog visibility to log used parts."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == Role.ADMIN:
            return True
        return request.method in SAFE_METHODS and request.user.role == Role.MECHANIC

class IsCustomerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and ( request.user.role == Role.ADMIN or request.user.role == Role.CUSTOMER)


class VehiclePermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == Role.ADMIN:
            return True
        if request.user.role == Role.CUSTOMER:
            if request.method == "DELETE":
                return False
            return obj.customer.user_id == request.user.id
        return False

class IsAdminOrOwnMechanic(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        is_admin = user.role == Role.ADMIN
        is_mechanic = user.role == Role.MECHANIC
        if request.method in SAFE_METHODS:
            return is_admin or is_mechanic
        return is_admin

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == Role.ADMIN:
            return True
        if user.role == Role.MECHANIC:
            return request.method in SAFE_METHODS and obj.user_id == user.id
        return False

class IsAdminOrAssignedMechanic(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.role in [Role.ADMIN, Role.MECHANIC]

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == Role.ADMIN:
            return True
        if user.role == Role.MECHANIC:
            return obj.mechanic.user_id == user.id
        return False

class IsAdminOrAssignedJobMechanic(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.role in [Role.ADMIN, Role.MECHANIC]

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == Role.ADMIN:
            return True
        if user.role == Role.MECHANIC:
            return obj.job.mechanic_assignments.filter(mechanic__user = user).exists()
        return False
    
class IsAdminOrInvoiceCustomer(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role in [Role.ADMIN, Role.CUSTOMER]

    def has_object_permission(self, request, view, obj):
        if request.user.role == Role.ADMIN:
            return True
        invoice = obj if isinstance(obj, Invoice) else obj.invoice
        return invoice.job.vehicle.customer.user_id == request.user.id
