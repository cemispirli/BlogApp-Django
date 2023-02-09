from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Post, Like, PostView, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, PostCreateSerializer, CommentCreateSerializer, PostUpdateSerializer, CommentUpdateSerializer
from django.http import JsonResponse




class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # def get (self, request):
    #     qs = Post.objects.all()
    #     serializer = PostSerializer(qs, many=True)
    #     return JsonResponse(serializer.data, safe=False)


class postCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=201, headers=headers)  

class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=201, headers=headers)

class CommentRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer


class PostRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer

class like (generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=201, headers=headers)









def post_list_all(request):
    qs = Post.objects.all()
    context = {
        'object_list' : qs
    }
    return render (request, "blog/post_list.html", context )

def post_list_published(request):
    qs = Post.objects.filter(status='p')
    context = {
        'object_list' : qs
    }
    return render (request, "blog/post_list.html", context )

def post_list_draft(request):
    qs = Post.objects.filter(status='d')
    context = {
        'object_list' : qs
    }
    return render (request, "blog/post_list.html", context )

@login_required()
def post_create(request):
    # form = PostForm(request.POST or None, request.FILES or None)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # print(request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blog:list_all")
    context = {
        'form' : form
    }
    return render (request, "blog/post_create.html", context)

def post_detail(request, slug):
    # comment = Comment.objects.all( )
    # kim = request.user
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug)
    # like_qs = Like.objects.filter(user=request.user, post=obj)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()
            return redirect("blog:detail", slug=slug)
            # return redirect(request.path)
    context = {
        'object' : obj,
        "form" : form,
        # "like_qs" : like_qs,
        # 'kitap' : comment,
        # 'kim': kim
    }
    return render(request, "blog/post_detail.html", context)

@login_required()
def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.user.username != obj.author and not request.user.is_superuser:
        # return HttpResponse("You are not authorized!")
        messages.warning(request, "You are not a writer of this post !")
        return redirect("blog:list_all")
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated !!")
        return redirect("blog:list_all")
    context = {
        "object" : obj,
        "form" : form
    }
    return render(request, "blog/post_update.html", context)

@login_required()
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.user.username != obj.author and not request.user.is_superuser:
        # return HttpResponse("You are not authorized!")
        messages.warning(request, "You are not a writer of this post !")
        return redirect("blog:list_all")
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Post deleted !!")
        return redirect("blog:list_all")    
    context = {
        "object" : obj
    }
    return render(request, "blog/post_delete.html", context)

@login_required()
def like(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs.exists():
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect("blog:detail", slug=slug)
    return redirect("blog:detail", slug=slug)

@login_required()
def comment(request, slug):
    obj = get_object_or_404(Comment, slug=slug)
    if request.user.id != obj.user.id and not request.user.is_superuser:
        # return HttpResponse("You are not authorized!")
        messages.warning(request, "You are not a writer of this post !")
        return redirect("blog:list_all")
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Comment deleted !!")
        return redirect("blog:detail", slug=obj.post.slug)
    return redirect("blog:detail", slug=slug)

