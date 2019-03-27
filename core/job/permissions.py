import socket

from rest_framework.permissions import BasePermission

LOCALHOST = socket.gethostname()


class JobAccess(BasePermission):

    def has_permission(self, request, view):
        host = request.META.get('HTTP_REFERER', None)

        is_allowed = [host and host == LOCALHOST]
        if "-" in host and "-" in LOCALHOST:
            host = host.split("-")[0]
            localhost = LOCALHOST.split('-')[0]
            is_allowed.append(host == localhost)

        return any(is_allowed)
