
from rest_framework import serializers
from .models import User, Permission, Role
# Clases para serializar nuestras entradas y respuestas para las vistas
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['__all__']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs={
            'password':{'write_only':True}
        }


    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self,value):
        return PermissionSerializer(value).data

    def to_internal_value(self, data):
        return data

    def create(self,validated_data):
        permissions = validated_data.pop('permissions',None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissions.add(*permission)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)
    class Meta:
        model = Role
        fields = ['__all__']
