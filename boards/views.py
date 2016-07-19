from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hitcount.models import HitCount
from hitcount.views import HitCountDetailView

from .forms import (
    PostWriteForm,
)
from .models import (
    Board,
    Post,
)
from .serializers import (
    BoardSerializer,
    PostSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        pk = self.request.GET.get('pk', False)
        if pk:
            queryset = Board.objects.filter(pk=pk)
        else:
            queryset = Board.objects.all()
        return queryset

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@login_required
def post_write(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)

    if request.method == 'GET':
        form = PostWriteForm()
    elif request.method == 'POST':
        form = PostWriteForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.board = board
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('boards:post_view', kwargs={'board_pk': board.pk, 'post_pk': post.pk}))
    context_data = {'form': form, 'board': board}
    return render(request, 'board/write.html', context_data)

class PostView(HitCountDetailView):
    template_name = 'board/post.html'
    count_hit = True
    post = None
    def get(self, *args, **kwargs):
        board_pk = self.kwargs['board_pk']
        post_pk = self.kwargs['post_pk']
        board = get_object_or_404(Board, pk=board_pk)
        self.post = get_object_or_404(Post, pk=post_pk)
        self.object = self.post

        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = self.post
        return context

post_view = PostView.as_view()

def post_list(request, board_pk):
    if request.method == 'GET':
        page_idx = request.GET.get('page', 0)
        page_idx = int(page_idx)
        board = get_object_or_404(Board, pk=board_pk)
        posts = Post.objects.filter(board__pk=board_pk).order_by('-created_at')
        cnt = 2
        page_cnt = 5
        start_page_idx = int(page_idx/page_cnt)*page_cnt
        end_page_idx = start_page_idx + page_cnt
        start = cnt*page_idx
        end = cnt*(page_idx+1)
        posts = posts[start:end]
        context_data = {'posts': posts, 'board': board}
        pages = []

        for i in range(start_page_idx, end_page_idx):
            if i == page_idx:
                pages.append({'active':i})
            else:
                pages.append({'':i})
        print(pages)
        context_data['pages'] = pages
        context_data['page_idx'] = page_idx
        context_data['prev_page_btn'] = page_idx >= page_cnt
        context_data['next_page_btn'] = True
        context_data['prev_page_idx'] = start_page_idx-1
        context_data['next_page_idx'] = end_page_idx+1
        return render(request, 'board/list.html', context_data)
    else:
        return Http404

def board_list(request):
    boards = Board.objects.all()
    return render(request, 'board/boardlist.html', context={'boards': boards})
