from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

from user.wallet import validate_wallet, get_balance


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "wallet", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def validate(self, data):
        wallet = data.get("wallet")
        if wallet:
            try:
                validate_wallet(wallet)
            except:
                raise serializers.ValidationError('invalid_wallet')
        return data

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            wallet=self.validated_data["wallet"]
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "wallet", "first_name", "last_name")

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        balance = 0
        try:
            validate_wallet(instance.wallet)
            balance = get_balance(instance.wallet)
        except:
            pass
        representation['balance'] = balance
        return representation