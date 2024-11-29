from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'wallet', views.WalletList)
router.register(r'transaction', views.TransactionList)

urlpatterns = router.urls
