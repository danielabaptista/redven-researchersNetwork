from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, ResearcherProfile
from .utils import export_users_to_json

# CustomUser Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'user_type', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_approved', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_approved', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_approved', 'is_staff', 'is_superuser')}
        ),
    )

    actions = ["approve_users"]

    def approve_users(self, request, queryset):
       for user in queryset:
           user.is_approved = True
           user.save()  
       self.message_user(request, "Selected users approved.")


    approve_users.short_description = "Approve selected users"


# StudentProfile Admin
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "approval_status")
    readonly_fields = ("approval_status", "full_name", "user", "city", "country","longitude","latitude","university", "bachelor_degree")
    exclude = ("approved",)
    search_fields = ("full_name", "user__email")

    def approval_status(self, obj):
        return "Approved" if obj.user.is_approved else "Not approved yet"
    approval_status.short_description = "Profile Status"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        export_users_to_json()


# ResearcherProfile Admin
@admin.register(ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "role", "approval_status")
    readonly_fields = ("approval_status","full_name","user","city","country","longitude","latitude","alma_mater","current_university","bachelor_degree","role",)
    exclude = ("approved",)
    search_fields = ("full_name", "user__email")

    def approval_status(self, obj):
        return "Approved" if obj.user.is_approved else "Not approved yet"
    approval_status.short_description = "Profile Status"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        export_users_to_json()


# Register CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
