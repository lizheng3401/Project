from django.shortcuts import render,get_object_or_404
from .models import GameCategory, Game
from comment.forms import GameCommentForm,SubGCommentForm
from comment.models import SubGComment
from django.http import StreamingHttpResponse

import os, tempfile, zipfile

# Create your views here.


def portfllio(request):
    categories = GameCategory.objects.all().order_by("name")
    gameList = []
    for cate in categories:
        games = Game.objects.filter(category = cate.pk).order_by("-createTime")
        temp = (cate,games)
        gameList.append(temp)

    return render(request, 'home/portfolio.html', context = {'gameList':gameList})


def gameInfo(request,pk):
    game = get_object_or_404(Game, pk=pk)
    form = GameCommentForm()
    subForm = SubGCommentForm()
    c = game.gamecomment_set.all()
    comments = []
    for comment in c:
        subComment = SubGComment.objects.filter(parentComment=comment.pk).order_by("createTime")
        temp = (comment,subComment)
        comments.append(temp)

    context = {
        'game': game,
        'form': form,
        'subForm': subForm,
        'comments': comments,
    }
    return render(request, 'game/game.html', context=context)



def downloadGame(request, pk):
    gameObj = get_object_or_404(Game, pk=pk)

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    url = str(gameObj.game.url)
    name = str(gameObj.game)
    response = StreamingHttpResponse(file_iterator(url))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)

    gameObj.increase_times()
    return response


def uploadGame(request):
    pass



