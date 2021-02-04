from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .models import Profile
from .serializer import UserSerializer, TokenSerializer, UserDetailSerializer, ProfileSerializer, \
    ChangePasswordSerializer, ProfileListSerializer
from .permissions import SuperUserPermission, SignUpPermission, IsOwner


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [SuperUserPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        else:
            return self.serializer_class


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        pass

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [SuperUserPermission]

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'set_password':
            return ChangePasswordSerializer
        if self.action == 'list':
            return ProfileListSerializer
        return self.serializer_class

    @action(detail=True, methods=['post', 'get'])
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print(serializer.data)
            user.set_password(serializer.data['new_password'])

            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = TokenSerializer
    permission_classes = [SignUpPermission]
