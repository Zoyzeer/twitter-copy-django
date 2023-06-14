from typing import Any, Dict
from django.http import HttpResponse, Http404
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer, TweetSerializer
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .models import Сomments, Post, Tweet


def index(request):
    #latest_comments_list = Сomments.objects.order_by("-pub_date")[:5]
    #context = {"latest_comments_list": latest_comments_list}
    return render(request, "index.html")


def detail(request, comments_id):
    try:
        comments = Сomments.objects.get(pk=comments_id)
    except Сomments.DoesNotExist:
        raise Http404("Comments does not exist")
    return render(request, "detail.html", {"comments": comments})

#def detail(request, comments_id):
    #comments = get_object_or_404(Comments, pk=comments_id)
    #return render(request, "twit/detail.html", {"comments": comments})

class HomeView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titel"] = "Home"
        return context
    

class CreatePost(CreateView):
    template_name = "createpost.html"
    model = Post
    fields = ["post_text", "image"]


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({'message': 'Пользователь успешно зарегистрирован'})
        else:
            return Response(serializer.errors, status=400)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Неверные учетные данные'}, status=401)


class UserLogoutView(APIView):
    def post(self, request):
        token_key = request.data.get('token')
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            logout(request)
            token.delete()
            return Response({'message': 'Пользователь успешно вышел'})
        except Token.DoesNotExist:
            return Response({'error': 'Недействительный токен'}, status=401)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserFollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            followers = user.profile.followers.all()
            serializer = UserSerializer(followers, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)
        

class UserFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            following = user.profile.following.all()
            serializer = UserSerializer(following, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)
        

class UserTweetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            tweets = Tweet.objects.filter(user=user)
            serializer = TweetSerializer(tweets, many=True)
            return Response(serializer.data)
        except Tweet.DoesNotExist or User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)