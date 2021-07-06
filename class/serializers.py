from rest_framework import serializers
from .models import Classes, Study
from authentication.models import Teacher, Student

class HandleClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classes
        fields = '__all__'

    def validate(self, attrs):
        teacher_id = attrs.get('teacher_id', '')
        print(teacher_id)
        try:
            teacher = Teacher.objects.get(pk=teacher_id.pk)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError('Invalid teacher ID')
        return attrs


class ClassMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'


class StudentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'