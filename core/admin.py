from django.contrib import admin
from .models import Role, Skill, RoleSkill, Profile, UserSkill, Resource, Progress

class RoleSkillInline(admin.TabularInline):
    model = RoleSkill
    extra = 1
    min_num = 1

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'skills_count', 'description')
    search_fields = ('name', 'description')
    inlines = [RoleSkillInline]

    def skills_count(self, obj):
        return obj.role_skills.count()
    skills_count.short_description = 'Mapped Skills'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')

@admin.register(RoleSkill)
class RoleSkillAdmin(admin.ModelAdmin):
    list_display = ('role', 'skill', 'required_level')
    list_filter = ('role', 'required_level')
    search_fields = ('role__name', 'skill__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'year', 'target_role')
    list_filter = ('year', 'target_role')
    search_fields = ('user__username', 'college')

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'current_level', 'updated_at')
    list_filter = ('current_level', 'skill')
    search_fields = ('user__username', 'skill__name')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'type', 'link')
    list_filter = ('type', 'skill__category')
    search_fields = ('title', 'skill__name', 'link')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'status', 'resource', 'date')
    list_filter = ('status', 'skill')
    search_fields = ('user__username', 'skill__name', 'notes')
