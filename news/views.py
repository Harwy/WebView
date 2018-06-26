from django.shortcuts import render_to_response, get_object_or_404, render
from .models import Blog, BlogType  # 引入models下Blog
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
# Create your views here.


def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()  # 全部博客
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):  # 传入blog的id
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):  # 传入blog_type_pk
    context = {}
    print('blog_type is:',blog_type_pk)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_types_id=blog_type)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)


clients = []


def index(request):
    return render(request, 'index.html')


def index2(request):
    return render(request, 'index2.html')


def modify_message(message):
    return message.lower()


@accept_websocket
def echo(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')
    else:
        for message in request.websocket:
            request.websocket.send(message)  # 发送消息到客户端


@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)
