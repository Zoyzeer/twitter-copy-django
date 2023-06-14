from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView,UserProfileUpdateView,
                    UserFollowersView, UserFollowingView, UserTweetsView)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('users/<str:username>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<str:username>/following/', UserFollowingView.as_view(), name='user-following'),
    path('users/<str:username>/tweets/', UserTweetsView.as_view(), name='user-tweets'),
]
