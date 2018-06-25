from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CourseSerializer(serializers.Serializer):

	code_course = serializers.CharField(max_length=50)
	name_course = serializers.CharField(max_length=50)
	credits_course = serializers.CharField(max_length=50)
	professor_course = serializers.CharField(max_length=50)
	group_course = serializers.CharField(max_length=50)
	period_course = serializers.CharField(max_length=50)
	year_course = serializers.CharField(max_length=50)
	programming_language = serializers.CharField(max_length=50)
	academic_period = serializers.CharField(max_length=50)


	
    