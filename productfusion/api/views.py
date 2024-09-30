from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import jwt
from django.conf import settings
from .models import User, Organisation, Member, Role
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

class SignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                access_token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')
                refresh_token = jwt.encode({'user_id': user.id, 'type': 'refresh'}, settings.SECRET_KEY, algorithm='HS256')
                return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create(
            email=data['email'],
            password=data['password'],  # Ideally, hash the password here
            profile=data.get('profile', {}),
            status=0
        )
        organisation = Organisation.objects.create(
            name=data['organisation_name'],
            status=0,
            personal=False,
            settings=data.get('settings', {})
        )
        role = Role.objects.create(name='owner', description='Owner role', org_id=organisation)
        Member.objects.create(org_id=organisation, user_id=user, role_id=role)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class InviteMemberView(APIView):
    def post(self, request):
        data = request.data
        organisation = Organisation.objects.get(id=data['organisation_id'])
        user = User.objects.get(email=data['email'])
        role = Role.objects.get(name=data['role'], org_id=organisation)
        Member.objects.create(org_id=organisation, user_id=user, role_id=role)
        return Response({'message': 'Member invited successfully'}, status=status.HTTP_201_CREATED)


class RoleWiseUsersView(APIView):
    def get(self, request):
        stats = Member.objects.values('role_id__name').annotate(user_count=Count('user_id'))
        return Response(stats, status=status.HTTP_200_OK)
    
class SendInviteEmailView(APIView):
    def post(self, request):
        data = request.data
        send_mail(
            'You are invited!',
            'Please join our platform by following the link.',
            'from@example.com',
            [data['email']],
            fail_silently=False,
        )
        return Response({'message': 'Invite sent successfully'}, status=status.HTTP_200_OK)



class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteMemberView(APIView):
    def delete(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)
            member.delete()
            return Response({'message': 'Member deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Member.DoesNotExist:
            return Response({'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)



class UpdateMemberRoleView(APIView):
    def patch(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)
            new_role_id = request.data.get('role_id')
            member.role_id = Role.objects.get(id=new_role_id)
            member.save()
            return Response({'message': 'Member role updated successfully'}, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

