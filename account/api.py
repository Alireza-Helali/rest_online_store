from django.http import HttpResponse
from rest_framework import generics, status, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .models import Profile
from .serializer import UserSerializer, TokenSerializer, UserDetailSerializer, ProfileSerializer, \
    ChangePasswordSerializer, ProfileListSerializer, SignUpSerializer
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


class ProfileView(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [SuperUserPermission]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return ChangePasswordSerializer
        elif self.action == 'list':
            return ProfileListSerializer
        else:
            return ProfileSerializer

    @action(detail=True, methods=['post', 'get'])
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.data['new_password'])

            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# class TokenApiView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
#     serializer_class = TokenSerializer
#     permission_classes = [SignUpPermission]
#

class RegisterView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [SignUpPermission]
