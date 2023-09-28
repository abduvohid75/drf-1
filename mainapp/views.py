from datetime import timezone

import stripe
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Course, Lesson, Payments
from .serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, TokenObtainPairSerializer
from .pagination import Pagination

stripe.api_key = 'sk_test_51NsUWaA4lSUtlIxzuyu5leDc9krpOGPZkQFYboWy1bYcfpOcuuup640YC6UDyF2du4UlSLHAIIdmesrelmnVn95Y00HZCyI2PW'
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if 'sub' in request.data and request.data['sub'] == True:
            user_email = request.user.email
            if instance.subs is None:
                instance.subs = user_email
            instance.subs += ' ' + user_email

        self.perform_update(serializer)
        return Response(serializer.data)

class PaymentsCreateView(APIView):
    def post(self, request):
        serializer = PaymentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(payment.sum_pay * 100),
                currency='usd',
                metadata={
                    'payment_id': payment.id
                }
            )
            payment.payment_intent_id = payment_intent.id
            payment.save()
            return Response(data=payment_intent.client_secret, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class PaymentsRetrieveView(APIView):
    def get(self, request, payment_intent_id):
        try:
            payment = Payments.objects.get(payment_intent_id=payment_intent_id)
            serializer = PaymentsSerializer(payment)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Payments.DoesNotExist:
            return Response(data="Payment not found", status=status.HTTP_404_NOT_FOUND)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Обновляем дату последнего входа пользователя
        if response.status_code == 200:
            user = request.user
            user.last_login = timezone.now()
            user.save()

        return response
@permission_classes([IsAuthenticated])
def protected_home(request):
    context = {
    }
    return render(request, 'mainapp/base.html', context)