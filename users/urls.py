from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import register, profile, user_list, ProfileList, ProfileRUD, profileCreate




urlpatterns = [
    path("users/",user_list, name="user_list"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),    
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    
    path('profiles/', ProfileList.as_view(), name='profiles'),
    path('profiles/<int:pk>', ProfileRUD.as_view(), name='profileRUD'),
    path('profiles/create/', profileCreate.as_view(), name='profileCreate'),

]

