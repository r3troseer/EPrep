from django.urls import path, include
from . import views
from .views import(PhoneNumberView, SendOrResendSMSAPIView, VerifyPhoneNumberAPIView, UserRegisterationView, UserLoginAPIView, Profile)

urlpatterns = [
    path('subject/', views.getSubjects),
    path('topic/create/', views.createTopic),
    path('topics/', views.getTopics),
    path('lesson/<str:pk>/', views.getLesson),
    path('user/', views.getUser),
    path('phone/', PhoneNumberView.as_view()),
    path('sms/', SendOrResendSMSAPIView.as_view()),
    path('verify/', VerifyPhoneNumberAPIView.as_view()),
    path('register/', UserRegisterationView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('profile/', Profile.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

]
