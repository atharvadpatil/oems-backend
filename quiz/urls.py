from django.urls import path
from .views import (
    MakeQuizView,
    CreateQuestionView,
    GetTeachQuizView,
    GetStuQuizView
)

urlpatterns = [
    path('make-quiz/', MakeQuizView.as_view(), name="make-quiz"),
    path('make-question/', CreateQuestionView.as_view(), name="make-question"),
    path('quiz/<class_id>', GetTeachQuizView.as_view(), name="teach-quiz"),
    path('quiz/<class_id>/<student_id>', GetStuQuizView.as_view(), name="stu-quiz"),
    #path('questions/', GetQuestionView.as_view(), name="questions"),
]