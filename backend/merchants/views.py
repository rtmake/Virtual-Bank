from django.shortcuts import render
from .serializers import MerchantSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Merchant
from rest_framework import generics
from rest_framework import permissions

from accounts.models import Account


class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantCreate(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account = Account.objects.get(
            number=serializer.validated_data.pop("account_number")
        )

        if not account:
            raise PermissionDenied("Not Found")

        if account.user != self.request.user:
            raise PermissionDenied("Account does not belong to this user")

        merchant = Merchant.objects.filter(account=account)
        if merchant:
            raise PermissionDenied("Merchant Account Exists")

        serializer.save(account=account)


class MerchantDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        merchant = Merchant.objects.filter(account__user=user).first()
        if not merchant:
            raise PermissionDenied("Merchant account not found for this user")
        return merchant

    def perform_update(self, serializer):
        if serializer.validated_data['account_number']:
            serializer.validated_data.pop('account_number')
        serializer.save(account__user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
