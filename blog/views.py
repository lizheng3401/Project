from django.shortcuts import render,get_object_or_404, redirect
from .models import Category, Tag, Post
from game.models import GameCategory, Game
from comment.forms import BlogCommentForm,SubBCommentForm
from comment.models import BlogComment,SubBComment
from .forms import PostForm
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image




def index(request):
    posts = Post.objects.all().order_by("-createTime")[:5]
    games = Game.objects.all().order_by("-createTime")[:3]
    context = {
        'posts':posts,
        'games':games,
    }
    return render(request, 'home/index.html', context = context)

def blog(request):
    categories = Category.objects.all().order_by("name")
    postList = []
    for cate in categories:
        posts = Post.objects.filter(category=cate.pk).order_by("-createTime")
        temp = (cate,posts)
        postList.append(temp)
    context = {
        "categories": categories,
        "postList": postList,
    }
    return render(request, 'home/blog.html', context = context)

def about(request):
    return render(request, 'home/about.html', context = None)

def contact(request):
    return render(request, 'home/contact.html', context = None)

def detail(request,pk):

    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    form = BlogCommentForm()
    subForm = SubBCommentForm()
    c = post.blogcomment_set.all()
    comments = []

    for comment in c:
        subComment = SubBComment.objects.filter(parentComment=comment.pk).order_by("createTime")
        temp = (comment,subComment)
        comments.append(temp)

    context = {
        'post': post,
        'form':form,
        'subForm':subForm,
        'comments': comments,
    }

    return render(request, 'blog/detail.html', context=context)


def write(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, 'blog/write.html', context={'form': form, 'categories': categories, 'tags': tags})


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#文件名合法性验证
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# def get_thumbnail(orig, width=200, height=200):
#     """get the thumbnail of orig
#     @return: InMemoryUploadedFile which can be assigned to ImageField
#     """
#     quality = "keep"
#     file_suffix = orig.name.split(".")[-1]
#     filename = orig.name
#     if file_suffix not in ["jpg", "jpeg"]:
#         filename = "%s.jpg" % orig.name[:-(len(file_suffix)+1)]
#         quality = 95
#     im = Image.open(orig)
#     size = (width, height)
#     thumb = im
#     thumb.thumbnail(size, Image.ANTIALIAS)
#     thumb_io = StringIO.StringIO()
#     thumb.save(thumb_io, format="JPEG", quality=quality)
#     thumb_file = InMemoryUploadedFile(thumb_io, None, filename, 'image/jpeg',
#                                       thumb_io.len, None)
#     return thumb_file
#

@csrf_exempt
def uploadImage(request):

    if request.method == "POST":
        file = request.FILES.get('wangEditorH5File', None)
        fileName =  str(file)

        if file == None:
            result = r"error|未成功获取文件，上传失败"
            res = HttpResponse(result)
            return res
        else:
            if file and allowed_file(fileName):
                path = default_storage.save('upload/'+fileName, ContentFile(file.read()))
                imgUrl = "http://localhost:8000/media/" + path
                res = HttpResponse(imgUrl)
                return res



def get_thumbnail(file, width=200, height=200):
    size = (width, height)
    print("this thumbnail")
    im = Image.open(file)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(str(file) + ".jpeg",'JPEG')
    return str(file)+".jpeg"

