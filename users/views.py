from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm, PasswordResetEmailCheck
from django.contrib import messages
from .serializers import ProfileSerializer, ProfileCreateSerializer, ProfileRUDSerializer, UserRUDSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from collections import namedtuple
from .models import Profile, User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


from django.urls import reverse_lazy


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def get(self, request):
    #     profiles = Profile.objects.all()
    #     serializer = ProfileSerializer(profiles, many=True)
    #     return JsonResponse(serializer.data, safe=False)

    

class profileCreate(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=201, headers=headers)

   



class ProfileRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileRUDSerializer
    queryset = Profile.objects.all()


    


    


 

    
     
     



    


    
            





def user_list(request):
    qs = User.objects.all()
    context = {
        'object_list' : qs
    }
    return render (request, "users/user_list.html", context )

def register(request):
    form = RegistrationForm(request.POST or None) 
    if request.user.is_authenticated:
        messages.warning(request, "You are already have an account!")
        return redirect("blog:list")
    if form.is_valid():
        form.save()
        name = form.cleaned_data["username"]
        messages.success(request, f"Account created for {name}")
        return redirect("login")  
                
    context = {
        "form" : form
    }
    return render(request, "users/register.html", context)

def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile, files=request.FILES or None)
    
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")
        return redirect(request.path)
    
    context = {
        "u_form" : u_form,
        "p_form" : p_form    
    }
    return render(request, "users/profile.html", context)

