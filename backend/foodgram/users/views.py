from django.contrib.auth.models import User
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import FollowSerializer, UserSerializer
from .models import Follow, User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer

    @action(detail=False,
            methods=['get'])
    def subscriptions(self, request):
        followings = User.objects.filter(following__user=request.user)
        serializer = UserSerializer(
            followings,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['get', 'delete'])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'GET':
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author)
            return Response(serializer.data)
        get_object_or_404(Follow, user=user, author=author).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
