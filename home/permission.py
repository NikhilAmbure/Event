# Custom permission class

from rest_framework.permissions import BasePermission

# Only Admin can create the event
class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
