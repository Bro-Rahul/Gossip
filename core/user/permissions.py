from rest_framework.permissions import BasePermission

class ActualUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE','PATCH']:
            return obj.username == request.user
        return True
    