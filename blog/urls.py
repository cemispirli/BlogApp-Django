from django.urls import path
from .views import post_list_published, post_create, post_detail, post_update, post_delete, like,post_list_all, post_list_draft,PostList,PostRUD,comment,CommentRud,postCreate,CommentCreate
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "blog"

urlpatterns = [
    path('post/', PostList.as_view(), name='post_list'),
    path('post/create/', postCreate.as_view(), name='post_create'),
    path('post/<int:pk>', PostRUD.as_view(), name='post_rud'),
    path('post/comment/create/', CommentCreate.as_view(), name='comment_create'),
    path('post/comment/<int:pk>/', CommentRud.as_view(), name='comment_rud'), 
    


    path("",post_list_all, name="list_all"),
    path("published",post_list_published, name="list_published"),
    path("draft",post_list_draft, name="list_draft"),
    path("create/",post_create, name="create"),
    path("<str:slug>/",post_detail, name="detail"),
    path("<str:slug>/update/",post_update, name="update"),
    path("<str:slug>/delete/",post_delete, name="delete"),
    path("<str:slug>/like/",like, name="like"),
    path('<str:slug>/comment/', comment, name='comment'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
