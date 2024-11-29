from rest_framework import filters
from rest_framework_json_api.views import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from wallet.settings import PAGE_SIZE

from rest_framework_json_api.pagination import JsonApiPageNumberPagination


class PagePagination(JsonApiPageNumberPagination):
    page_query_param = 'page_number'
    page_size_query_param = 'page_length'
    page_size = PAGE_SIZE
    max_page_size = 1000


class WalletList(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['label', 'balance']
    ordering_fields = ['id', 'label', 'balance']
    ordering = ['id']
    http_method_names = ['get', 'post']


class TransactionList(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['txid', 'wallet__label', 'wallet', 'amount']
    ordering_fields = ['id', 'wallet__label', 'txid', 'amount']
    ordering = ['id']
    http_method_names = ['get', 'post']
