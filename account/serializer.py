from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login

from account.models import Profile


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('unable to provide user with provided data', code='authentication')
        attrs['user'] = user
        login(self.context.get('request'), user)
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5,
                         'style': {'input_type': 'password'}, 'trim_whitespace': False
                         },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'url', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5,
                         'style': {'input_type': 'password'}, 'trim_whitespace': False
                         },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'password']
        read_only_fields = ['password']


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'url']


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source='owner.name')

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['is_supplier', 'is_active']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=5, style={'input_type': 'password'}, required=True,
                                         write_only=False)
    new_password = serializers.CharField(min_length=5, style={'input_type': 'password'}, required=True,
                                         write_only=False)
    confirm_password = serializers.CharField(min_length=5, style={'input_type': 'password'}, required=True,
                                             write_only=False)

    def validate(self, attrs, **kwargs):
        request = self.context.get('request')
        user = request.user
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password must match together')
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('old password is not correct')
        return attrs
