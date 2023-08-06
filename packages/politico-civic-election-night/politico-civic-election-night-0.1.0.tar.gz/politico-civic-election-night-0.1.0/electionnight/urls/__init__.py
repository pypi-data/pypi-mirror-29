from .viewsets import urlpatterns as viewsets
from .views import urlpatterns as views

urlpatterns = views + viewsets
