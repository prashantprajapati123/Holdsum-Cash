from rest_framework.exceptions import PermissionDenied
from rest_framework import decorators, mixins, permissions, response, viewsets

from accounts.models import STATUS_CHOICES
from . import docusign
from .models import LoanRequest
from .serializers import LoanRequestSerializer


class LoanRequestViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A viewset for creating Loan Requests.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanRequestSerializer
    queryset = LoanRequest.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.status != STATUS_CHOICES.approved:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    @decorators.detail_route(methods=['POST'], url_path='signing-url')
    def signing_url(self, request, pk=None):
        lr = self.get_object()
        url = docusign.get_signing_url(lr)
        return response.Response(url)
