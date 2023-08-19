import random
import uuid

import django.core.exceptions
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Device


class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # user, created = User.objects.get_or_create(phone_number=phone_number)
        try:
            user = User.objects.get(phone_number=phone_number)
            # return Response({'detail': 'User already registered!'},
            #                 status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)
        try:
            user.full_clean()
        except django.core.exceptions.ValidationError as e:
            if 'phone_number' in e.error_dict:
                print(e.error_dict['phone_number'])
                user.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # if not created:
        #     return Response({'detail': 'User already registered!'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        device = Device.objects.create(user=user)

        code = random.randint(10000, 99999)
        cache.set(str(phone_number), code, 2 * 60)
        return Response({'code': code})


class GetTokenView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = str(uuid.uuid4())
        return Response({'token': token})
