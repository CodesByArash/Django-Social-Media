from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from account.models import *


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # check old password
        if not check_password(data.get('old_password'), user.password):
            raise serializers.ValidationError('Invalid password')

        # new password should not be the same as old password
        if check_password(data.get('new_password'), user.password):
            raise serializers.ValidationError('New password must be different from old password')

        # validate new password
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("The new password and confirmation do not match.")

        return data.get('new_password')