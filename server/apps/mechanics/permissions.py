from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )

class IsAdminOrOwnMechanic(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role == 'admin' or request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return request.method in SAFE_METHODS and obj.user_id == request.user.id

class IsAdminOrAssignedMechanic(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role == 'admin' or request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH']:
            return obj.mechanic.user_id == request.user.id
        return False
