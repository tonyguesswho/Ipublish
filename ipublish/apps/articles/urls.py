from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import ArticleViewset

router = DefaultRouter(trailing_slash=False)


router.register(r'articles', ArticleViewset)
app_name = 'articles'

urlpatterns = [
    path('', include(router.urls))
]
