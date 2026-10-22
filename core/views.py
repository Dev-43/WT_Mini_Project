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

def role_list_view(request):
    """Browse all available career roles."""
    roles = Role.objects.prefetch_related('role_skills__skill').all()
    current_target_role = None
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        current_target_role = profile.target_role

    return render(request, 'core/role_list.html', {
        'roles': roles,
        'current_target_role': current_target_role
    })

def role_detail_view(request, role_id):
    """View detailed competency benchmarks for a role."""
    role = get_object_or_404(Role, id=role_id)
    role_skills = role.role_skills.select_related('skill').prefetch_related('skill__resources').order_by('-required_level', 'skill__name')
    is_target = False
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        is_target = (profile.target_role_id == role.id)

    return render(request, 'core/role_detail.html', {
        'role': role,
        'role_skills': role_skills,
        'is_target': is_target
    })

@login_required
def role_select_view(request, role_id):
    """Set the specified role as the student's target role."""
    role = get_object_or_404(Role, id=role_id)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.target_role = role
    profile.save()
    messages.success(request, f"Target role set to '{role.name}'. Let's assess your skills!")
    return redirect('assessment')

@login_required
def assessment_view(request):
    """Rate skills for the student's target role."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not profile.target_role:
        messages.warning(request, "Please choose a target career role before taking your self-assessment.")
        return redirect('role_list')

    target_role = profile.target_role
    role_skills = target_role.role_skills.select_related('skill').all()

    if request.method == 'POST':
        # Process standard role skills
        skill_ids = request.POST.getlist('skill_id')
        for sid in skill_ids:
            try:
                rating = int(request.POST.get(f'rating_{sid}', 0))
                rating = max(0, min(5, rating))  # clamp between 0 and 5
                skill = Skill.objects.get(id=sid)
                UserSkill.objects.update_or_create(
                    user=request.user,
                    skill=skill,
                    defaults={'current_level': rating}
                )
            except (ValueError, Skill.DoesNotExist):
                continue

        # Process dynamic custom skills if added
        custom_skill_ids = request.POST.getlist('custom_skill_id')
        for idx, csid in enumerate(custom_skill_ids, start=1001):
            try:
                custom_rating = int(request.POST.get(f'custom_rating_{idx}', 1))
                custom_rating = max(0, min(5, custom_rating))
                skill = Skill.objects.get(id=csid)
                UserSkill.objects.update_or_create(
                    user=request.user,
                    skill=skill,
                    defaults={'current_level': custom_rating}
                )
            except (ValueError, Skill.DoesNotExist):
                continue

        messages.success(request, f"Your assessment for '{target_role.name}' has been saved successfully!")
        return redirect('result')

    # GET request
    user_skills_dict = {
        us.skill_id: us.current_level
        for us in UserSkill.objects.filter(user=request.user)
    }

    skill_items = []
    target_skill_ids = set()
    for rs in role_skills:
        target_skill_ids.add(rs.skill_id)
        skill_items.append({
            'skill': rs.skill,
            'required_level': rs.required_level,
            'current_level': user_skills_dict.get(rs.skill_id, 0),
        })

    all_other_skills = Skill.objects.exclude(id__in=target_skill_ids).order_by('category', 'name')

    return render(request, 'core/assessment.html', {
        'target_role': target_role,
        'skill_items': skill_items,
        'all_other_skills': all_other_skills,
    })

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
