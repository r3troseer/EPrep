from django.urls import path, include
from . import views
from .views import(SendOrResendSMSAPIView, VerifyPhoneNumberAPIView, UserRegisterationView, UserLoginAPIView, Profile, ChildView,)

urlpatterns = [
    path('subject/', views.getSubjects),
    path('topic/create/', views.createTopic),
    path('topics/', views.getTopics),
    path('lesson/<str:pk>/', views.getLesson),
    path('sms/', SendOrResendSMSAPIView.as_view()),
    path('verify/', VerifyPhoneNumberAPIView.as_view()),
    path('register/', UserRegisterationView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('profile/', Profile.as_view()),
    path('child/', ChildView.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

]
