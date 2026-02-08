# views.py

from api.models import User, Appointment, Date
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    AppointmentSerializer
)
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes

# ----------------------
# USER APIs
# ----------------------

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
                'username': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                if not user.is_active:
                    return Response({'error': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'refresh': str(refresh), 'access': str(access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ----------------------
# APPOINTMENT APIs
# ----------------------

class AppointmentPagination(PageNumberPagination):
    page_size = 10


@api_view(['GET', 'POST'])
def appointments_list_create(request):
    if request.method == 'GET':
        status_filter = request.GET.get('status')
        search = request.GET.get('search')

        appointments = Appointment.objects.all().order_by('-created_at')

        if status_filter:
            appointments = appointments.filter(status=status_filter)
        if search:
            appointments = appointments.filter(name__icontains=search)

        paginator = AppointmentPagination()
        result_page = paginator.paginate_queryset(appointments, request)
        serializer = AppointmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save(status='pending')

            send_mail(
                "Appointment Received",
                "Your appointment request has been received. We will contact you soon.",
                None,
                [appointment.email],
                fail_silently=True
            )

            return Response({
                "success": True,
                "message": "Appointment created",
                "data": AppointmentSerializer(appointment).data
            }, status=201)

        return Response(serializer.errors, status=400)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'approved'
    appointment.save()

    send_mail(
        "Appointment Approved",
        "Your appointment has been approved.",
        None,
        [appointment.email],
        fail_silently=True
    )

    return Response(status=204)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'rejected'
    appointment.save()

    send_mail(
        "Appointment Rejected",
        "Sorry, your appointment has been rejected.",
        None,
        [appointment.email],
        fail_silently=True
    )

    return Response(status=204)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return Response(status=204)
