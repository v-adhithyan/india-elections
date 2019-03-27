import socket

from rest_framework.permissions import BasePermission

LOCALHOST = socket.gethostname()


class JobAccess(BasePermission):

    def has_permission(self, request, view):
        host = request.META.get('HTTP_REFERER', None)

        return host and host == LOCALHOST
