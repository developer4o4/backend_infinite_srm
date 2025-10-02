from rest_framework import serializers
from .models import Admin_users


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin_users
        fields = ["id", "username", "phone_number", "password", "first_name", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Admin_users(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance






