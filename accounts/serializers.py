from rest_framework import serializers

from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from accounts.models import User
from teams.models import Team


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    grade = serializers.IntegerField(required=True, write_only=True)
    klass = serializers.IntegerField(required=True, write_only=True)
    number = serializers.IntegerField(required=True, write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("이미 등록된 메일입니다.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_grade(self, grade):
        if not 1 <= grade <= 3:
            raise serializers.ValidationError("올바른 정보를 입력해 주세요.")
        return grade

    def validate_klass(self, klass):
        if not 1 <= klass <= 12:
            raise serializers.ValidationError("올바른 정보를 입력해 주세요.")
        return klass

    def validate_number(self, number):
        if not 1 <= number <= 40:
            raise serializers.ValidationError("올바른 정보를 입력해 주세요.")
        return number

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def custom_signup(self, user, data):
        grade = data.get('grade', '')
        klass = data.get('klass', '')
        number = data.get('number', '')
        user.grade = grade
        user.klass = klass
        user.number = number
        user.save()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'grade': self.validated_data.get('grade', ''),
            'klass': self.validated_data.get('klass', ''),
            'number': self.validated_data.get('number', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(user, self.cleaned_data)
        setup_user_email(request, user, [])
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    teams = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='team-detail', many=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'url', 'username', 'name', 'grade', 'klass',
            'number', 'tags', 'teams', 'introduction', 'profile_image',
        )
