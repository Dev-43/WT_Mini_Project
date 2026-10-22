from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Role, Skill, RoleSkill, Profile, UserSkill, Resource, Progress
from .forms import RegisterForm, LoginForm, ProfileForm

def home(request):
    """Public landing page."""
    return render(request, 'core/home.html')

def register_view(request):
    """Student registration: creates User and Profile."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(
                user=user,
                college=form.cleaned_data.get('college') or 'AISSMS IOIT',
                year=form.cleaned_data.get('year') or 'Third Year'
            )
            login(request, user)
            messages.success(request, f"Welcome to SkillBridge, {user.username}! Your account has been created.")
            return redirect('role_list')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    """Student login view with session establishment."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Ensure profile exists
                Profile.objects.get_or_create(user=user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    """Student logout view (POST recommended, supports GET with message)."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def profile_view(request):
    """View and update profile information and target role."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            new_email = form.cleaned_data.get('email')
            if new_email and new_email != request.user.email:
                request.user.email = new_email
                request.user.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={'email': request.user.email})

    return render(request, 'core/profile.html', {'form': form, 'profile': profile})

# Placeholders for steps 6-12 (to be implemented next)
def role_list_view(request):
    return render(request, 'core/home.html')

def role_detail_view(request, role_id):
    return render(request, 'core/home.html')

@login_required
def assessment_view(request):
    return render(request, 'core/home.html')

@login_required
def result_view(request):
    return render(request, 'core/home.html')

@login_required
def tracker_view(request):
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'core/home.html')

@login_required
def export_xml_view(request):
    return HttpResponse("<report></report>", content_type="application/xml")

@login_required
def api_skills_view(request):
    return JsonResponse({"skills": []})

@login_required
def api_result_view(request):
    return JsonResponse({"results": []})
