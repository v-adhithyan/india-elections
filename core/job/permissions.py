from rest_framework.permissions import BasePermission


LOCALHOST = '127.0.0.1'


class JobAccess(BasePermission):

    def has_permission(self, request, view):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

        if not ip_address:
            ip_address = request.META.get('REMOTE_ADDR')

        return ip_address == LOCALHOST
