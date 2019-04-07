from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer
from .renderers import ArticleJsonRenderer


class ArticleViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializer


    def create(self, request, *args, **kwargs):
        serializer_context = {
            'author': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug):
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, context=serializer_context, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        serializer_context ={
            'request':request
        }
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        serializer = self.serializer_class(serializer_instance, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticlesFavoriteAPIView(APIView):
        permission_classes = (IsAuthenticated,)
        renderer_classes = ( ArticleJsonRenderer,)
        serializer_class = ArticleSerializer

        def delete(self, request, article_slug=None):
            profile = self.request.user.profile
            serializer_context = {'request': request}

            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                raise NotFound('An article with this slug was not found.')

            profile.unfavorite(article)

            serializer = self.serializer_class(article, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_200_OK)

        def post(self, request, article_slug=None):
            profile = self.request.user.profile
            serializer_context = {'request': request}

            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                raise NotFound('An article with this slug was not found.')

            profile.favorite(article)

            serializer = self.serializer_class(article, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

