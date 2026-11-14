from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from apps.user.models import User
from .models import Mechanic, JobMechanic, Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        existing = Specialization.objects.filter(name__iexact = value)
        if self.instance:
            existing = existing.exclude(id = self.instance.id)
        if existing.exists():
            raise serializers.ValidationError("Specialization already exists.")
        return value


class MechanicCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True, validators = [validate_password])
    user_email = serializers.EmailField(source = 'user.email', read_only = True)

    class Meta:
        model = Mechanic
        fields = ['id', 'user', 'user_email', 'username', 'email', 'password', 'specialization', 'name', 'experience_level', 'hourly_rate', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'user_email', 'created_at', 'updated_at']

    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_specialization(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This specialization is inactive.")
        return value

    def validate_hourly_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("Hourly rate cannot be negative.")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        with transaction.atomic():
            user = User.objects.create_user(username = username, email = email, password = password, role = 'mechanic')
            mechanic = Mechanic.objects.create(user = user, **validated_data)
        return mechanic


class MechanicSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source = 'user.email', read_only = True)

    class Meta:
        model = Mechanic
        fields = ['id', 'user', 'user_email', 'specialization', 'name', 'experience_level', 'hourly_rate', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'user_email', 'created_at', 'updated_at']

    def validate_specialization(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This specialization is inactive.")
        return value

    def validate_hourly_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("Hourly rate cannot be negative.")
        return value


class JobMechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMechanic
        fields = ['id', 'job', 'mechanic', 'working_hours', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']

    def validate_working_hours(self, value):
        if value < 0:
            raise serializers.ValidationError("Working hours cannot be negative.")
        return value

    def validate_mechanic(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This mechanic is inactive.")
        return value

    def validate(self, attrs):
        job = attrs.get('job')
        mechanic = attrs.get('mechanic')
        if self.instance:
            job = self.instance.job
            mechanic = self.instance.mechanic
            if 'job' in attrs and attrs['job'] != job:
                raise serializers.ValidationError("You cannot change the assigned job.")
            if 'mechanic' in attrs and attrs['mechanic'] != mechanic:
                raise serializers.ValidationError("You cannot change the assigned mechanic.")
        if not self.instance and JobMechanic.objects.filter(job = job, mechanic = mechanic).exists():
            raise serializers.ValidationError("This mechanic is already assigned to this job.")
        return attrs
