from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.paginators import RecipePagination
from .serializers import FollowSerializer
from .models import Follow, User


class UserViewSet(UserViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = RecipePagination

    @action(detail=False,
            methods=['get'])
    def subscriptions(self, request):
        followings = self.paginate_queryset(
            User.objects.filter(
                following__user=request.user
                )
        )
        serializer = FollowSerializer(
            followings,
            context={'request': request},
            many=True
        )
        if followings is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True,
            methods=['get', 'delete'])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'GET':
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data)
        get_object_or_404(Follow, user=user, author=author).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
