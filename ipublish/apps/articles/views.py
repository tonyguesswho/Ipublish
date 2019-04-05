from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
from .renderers import ArticleJsonRenderer


class ArticleViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):

    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializer


    def create(self, request, *args, **kwargs):
        serializer_context = {'author': request.user.profile}
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
