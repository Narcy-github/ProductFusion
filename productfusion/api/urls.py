from django.urls import path
from .views import SignInView, SignUpView, InviteMemberView, RoleWiseUsersView, SendInviteEmailView, ResetPasswordView, DeleteMemberView, UpdateMemberRoleView


urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('invite-member/', InviteMemberView.as_view(), name='invite_member'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('role-wise-users/', RoleWiseUsersView.as_view(), name='role_wise_users'),
    path('delete-member/<int:member_id>/', DeleteMemberView.as_view(), name='delete_member'),
    path('update-member-role/<int:member_id>/', UpdateMemberRoleView.as_view(), name='update_member_role'),
    path('send-invite-email/', SendInviteEmailView.as_view(), name='send_invite_email'),
]
