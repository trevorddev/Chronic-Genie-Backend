from django.urls import path
from user.api.views import(
	registration_view,
	ObtainAuthTokenView,
	Logout,
    SetNewPasswordAPIView, 
    # VerifyEmail, 
    PasswordTokenCheckAPI, 
    RequestPasswordResetEmail,
    passwordResetView

)

from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'account'

urlpatterns = [
	path('register', registration_view, name="register"),
    path('login', ObtainAuthTokenView.as_view(), name="login"), # -> see user/api/views.py for response and url info
	path('logout', Logout.as_view(), name="logout"),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('reset/', passwordResetView,
         name='password-reset'),

]