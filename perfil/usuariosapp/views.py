from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            profile = request.user.userprofile
            profile.profile_picture = profile_picture
            profile.save()
            messages.success(request, 'La imagen se ha cargado con éxito.')
        else:
            messages.error(request, 'No se pudo cargar la imagen.')
        return redirect('profile_success')

    return render(request, 'profile.html')


@login_required
def profile_success(request):
    return render(request, 'profile_success.html')

@login_required
def home(request):
    return render(request, 'home.html')
