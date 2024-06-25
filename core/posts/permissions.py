from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class CommentorCreatorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print(obj)
        return obj.created_by == request.user
    