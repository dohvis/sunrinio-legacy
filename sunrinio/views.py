from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from boards.models import Board, Post


def index(request):
    news_board = Board.objects.filter(name='공지사항')

    current = timezone.now()
    last_day = current - timedelta(days=1)
    hot_posts = Post.objects.filter(comments__created_at__range=(last_day, current)) \
        .annotate(comment_count=Count('comments'))\
        .order_by('-comment_count')[:3]
    # TODO: 히트 게시물 판별 알고리즘 수정
    try:
        news = news_board[0].posts.order_by('-created_at')[:3]
    except IndexError:
        news = []

    return render(request, 'index.html', context={'newses': news, 'hot_posts': hot_posts})
