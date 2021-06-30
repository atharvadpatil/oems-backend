from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .permissions import IsTeacher, IsStudent
from .models import Classes, Study
from .serializers import (
    HandleClassSerializer,
    ClassMemberSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

# Create your views here.

class HandleClassView(generics.GenericAPIView):
    serializer_class = HandleClassSerializer

    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def post(self, request):
        print(type(request.user.user_type))
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        class_data = serializer.data
        return Response(class_data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        class_id = request.data.get('class_id')
        try:
            c = Classes.objects.get(pk = class_id)
            c.delete()
        except ObjectDoesNotExist:
            return Response({'response':'Invalid class ID'})
        return Response({'response':'class deleted'})



class ClassMembershipView(generics.GenericAPIView):
    serializer_class = ClassMemberSerializer

    permission_classes = (permissions.IsAuthenticated, IsStudent)

    def post(self, request):

        joining_code = request.data.get('joining_code')
        student_id = request.data.get('student_id')
        c = Classes.objects.filter(joining_code = joining_code)
        
        if not c:
            return Response({'response':'Invalid joining code'})
            
        timestamp = c[0].joining_code_expiry_date
        current = date.today()
        
        print(timestamp)
        print(current)

        if timestamp < current :
            return Response({'response':'Joining code has expired'})

        serializer = self.serializer_class(data={'class_id': c[0].pk, 'student_id': student_id})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        join_data = serializer.data
        return Response(join_data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        class_id = request.data.get('class_id')
        student_id = request.data.get('student_id')
        try:
            s = Study.objects.get(class_id = class_id, student_id = student_id)
            s.delete()
        except ObjectDoesNotExist:
            return Response({'response':'Invalid request data'})
        return Response({'response':'Student left the class'})