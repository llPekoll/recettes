from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# def delete_test_users(self, request, queryset):
#     prefix = "pw_test_"
#     users = queryset.filter(username__startswith=prefix)
#     count = users.count()
#     users.delete()
#     self.message_user(request, f"{count} users deleted.")

# short_description = "Delete users with prefix 'pw_test'"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    # actions = [delete_test_users]
