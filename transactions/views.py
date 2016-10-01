from rest_framework import mixins, permissions, viewsets

from .serializers import LoanRequestSerializer


class LoanRequestViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A viewset for creating Loan Requests.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanRequestSerializer
