from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_page(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])
def create_tweet(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def get_all_tweets(request, *args, **kwargs):
    tweetSet = Tweet.objects.all()
    serializer = TweetSerializer(tweetSet, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweetId, *args, **kwargs):
    tweet = Tweet.objects.filter(id=tweetId)

    if not tweet.exists():
        return Response({}, status=404)

    obj = tweet.first()
    serializer = TweetSerializer(obj)

    return Response(serializer.data, status=200)
    

# def create_tweet_django(request, *args, **kwargs):
#     user = request.user

#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status=401)

#         return redirect(settings.LOGIN_URL)

#     form = TweetForm(request.POST or None)
#     nextUrl = request.POST.get("next") or None

#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = user
#         obj.save()

#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201)

#         if nextUrl != None and is_safe_url(nextUrl, ALLOWED_HOSTS):
#             return redirect(nextUrl)

#         form = TweetForm()

#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status=400)

#     return render(request, 'components/form.html', context={"form": form})


# def get_all_tweets_django(request, *args, **kwargs):
#     tweetSet = Tweet.objects.all()
#     tweets = [x.serialize() for x in tweetSet]
#     data = {
#         "isUser": False,
#         "response": tweets
#     }
#     return JsonResponse(data)


# def tweet_detail_view_django(request, tweetId, *args, **kwargs):
#     data = {
#         "id": tweetId,
#     }
#     status=200
#     try:
#         obj = Tweet.objects.get(id=tweetId)
#         data['content'] = obj.content
#     except :
#         data['message'] = "Oops! Not Found..."
#         status=404
#     return JsonResponse(data, status=status)
