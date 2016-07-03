from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        # TODO: 이거 try-except로 obj.author 등 추가해서 로그인말고도 다른곳에서도 쓸수 있게
        return obj == request.user
