from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .models import Course, Lesson, Payments
from .serializers import CourseSerializer, LessonSerializer, PaymentsSerializer

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class PaymentsListView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'pay_met']
    ordering_fields = ['date']


def home(request):

    context = {

    }

    return render(request, 'mainapp/base.html', context)