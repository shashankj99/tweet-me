from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

# from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer

import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_page(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_tweet(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def get_all_tweets(request, *args, **kwargs):
    tweet_set = Tweet.objects.all()
    serializer = TweetSerializer(tweet_set, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)

    if not tweet.exists():
        return Response({}, status=404)

    obj = tweet.first()
    serializer = TweetSerializer(obj)

    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_tweet(request, tweet_id, *args, **kwargs):
    # get the tweet based on tweet id
    tweet = Tweet.objects.filter(id=tweet_id)

    # return error if tweet doesn't exist
    if not tweet.exists():
        return Response({}, status=404)

    # filter the tweet based on user
    tweet = tweet.filter(user=request.user)

    # return authentication error if tweet doesn't belong to the respective user
    if not tweet.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)

    # get the first object from the query set
    obj = tweet.first()

    # delete the object
    obj.delete()

    return Response({"message": "Tweet Removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_actions(request, *args, **kwargs):
    # instantiate the TweetActionSerializer class
    serializer = TweetActionSerializer(request.POST)

    # check if serializer is valid
    if serializer.is_valid(raise_exception=True):
        # get tweet id and action from the serializer
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')

        # filter the tweet based on tweet id
        tweet = Tweet.objects.filter(id=tweet_id)
        
        # check for tweet existence
        if not tweet.exists():
            return Response({}, status=404)

        # get the first object from the query set
        obj = tweet.first()

        # check for action types
        if action == 'like':
            # add user to the tweet
            obj.likes.add(request.user)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            # todo retweet
            pass
    return Response({}, status=200)


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
#     tweet_set = Tweet.objects.all()
#     tweets = [x.serialize() for x in tweet_set]
#     data = {
#         "isUser": False,
#         "response": tweets
#     }
#     return JsonResponse(data)


# def tweet_detail_view_django(request, tweet_id, *args, **kwargs):
#     data = {
#         "id": tweet_id,
#     }
#     status=200
#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data['content'] = obj.content
#     except :
#         data['message'] = "Oops! Not Found..."
#         status=404
#     return JsonResponse(data, status=status)
