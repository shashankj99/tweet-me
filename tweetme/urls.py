from django.contrib import admin
from django.urls import path
from tweets.views import home_page, tweet_detail_view, get_all_tweets, create_tweet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('create-tweet', create_tweet),
    path('tweets', get_all_tweets),
    path('tweet/<int:tweetId>', tweet_detail_view)
]
