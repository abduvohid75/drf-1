from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Course, Lesson, Payments, Subs
from .serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, TokenObtainPairSerializer
from .pagination import Pagination


class UserPermissionEditLesson(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модераторы').exists() or obj.author == request.user:
            return True
        else:
            return False
class CanCreateLessonOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        return False
class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = Pagination
    permission_classes = [permissions.IsAuthenticated, ]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            if user.groups.filter(name='Модераторы').exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(author=user)
        else:
            return Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class LessonRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Pagination
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            sub = self.request.data.get('sub')
            queryset = super().get_queryset()
            obj = get_object_or_404(queryset, id=self.kwargs['pk'])
            if obj.subs == None:
                subs = Subs.objects.create()
                obj.subs = subs
            if sub == 'true':
                obj.subs.users.add(self.request.user)
                obj.subs.save()
                obj.save()
            if sub == 'false':
                obj.subs.users.remove(self.request.user)
                obj.subs.save()
                obj.save()
        else:
            queryset = super().get_queryset()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PaymentsListView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'pay_met']
    ordering_fields = ['date']

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
@permission_classes([IsAuthenticated])
def protected_home(request):
    context = {
    }
    return render(request, 'mainapp/base.html', context)