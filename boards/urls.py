from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from .models import Board, Post


class PostForm(ModelForm):
    class Meta:
        model = Post


def board_post(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)

    if request.method == 'GET':
        context_data = {'posts': board.posts.all()}
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.board = board
            post.save()
        context_data = {}
    return render(request, 'board/list.html', context_data)


def post_view(request, board_pk, post_pk):
    board = get_object_or_404(Board, pk=board_pk)
    post = get_object_or_404(Post, pk=post_pk)

    context_data = {'post': post}
    return render(request, 'board/post.html', context_data)
