from django.contrib import admin
from .models import Grade, Group, GroupInvite, PermissionType, Resource, Comment, Permission


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_email', 'teacher_email', 'lesson_title', 'score', 'comment', 'created']
    list_display_links = ['student_email']
    list_per_page = 10  
    list_select_related = ['student', 'teacher', 'problems', 'problems__lesson']
    search_fields = ['student__email', 'teacher__email', 'problems__lesson__title']
    list_filter = ['teacher', 'score', 'created']
    ordering = ['-created']
    autocomplete_fields = ['student', 'teacher', 'problems']

    @admin.display(description="Student Email")
    def student_email(self, obj):
        return obj.student.email if obj.student else None

    @admin.display(description="Teacher Email")
    def teacher_email(self, obj):
        return obj.teacher.email if obj.teacher else None

    @admin.display(description="Lesson Title")
    def lesson_title(self, obj):
        return obj.problems.lesson.title if obj.problems else None


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner_email', 'total_students']
    list_display_links = ['name']
    list_per_page = 10
    list_select_related = ['owner']
    search_fields = ['name', 'owner__email']
    ordering = ['name']
    autocomplete_fields = ['owner', 'students']

    @admin.display(description="Owner Email")
    def owner_email(self, obj):
        return obj.owner.email if obj.owner else None

    @admin.display(description="Total Students")
    def total_students(self, obj):
        return obj.students.count()


@admin.register(GroupInvite)
class GroupInviteAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender_email', 'receiver_email', 'group_name', 'status']
    list_display_links = ['sender_email']
    list_per_page = 10
    list_select_related = ['sender', 'receiver', 'group']
    search_fields = ['sender__email', 'receiver__email', 'group__name']
    list_filter = ['status']
    ordering = ['status']
    autocomplete_fields = ['sender', 'receiver', 'group']

    @admin.display(description="Sender Email")
    def sender_email(self, obj):
        return obj.sender.email if obj.sender else None

    @admin.display(description="Receiver Email")
    def receiver_email(self, obj):
        return obj.receiver.email if obj.receiver else None

    @admin.display(description="Group Name")
    def group_name(self, obj):
        return obj.group.name if obj.group else None


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group_name', 'uploaded_by_email']
    list_display_links = ['name']
    list_per_page = 10
    list_select_related = ['group', 'uploaded_by']
    search_fields = ['name', 'group__name', 'uploaded_by__email']
    ordering = ['name']
    autocomplete_fields = ['group', 'uploaded_by']

    @admin.display(description="Group Name")
    def group_name(self, obj):
        return obj.group.name if obj.group else None

    @admin.display(description="Uploaded By")
    def uploaded_by_email(self, obj):
        return obj.uploaded_by.email if obj.uploaded_by else None


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'content_preview', 'created_at']
    list_display_links = ['user_email']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['user__email', 'content']
    ordering = ['-created_at']
    autocomplete_fields = ['user', 'lesson', 'resource']

    @admin.display(description="User Email")
    def user_email(self, obj):
        return obj.user.email if obj.user else None

    @admin.display(description="Comment")
    def content_preview(self, obj):
        return obj.content[:50] + "..." if obj.content else None


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'group_name', 'get_permission_types']
    list_display_links = ['user_email']
    list_per_page = 10
    list_select_related = ['user', 'group']
    search_fields = ['user__email', 'group__name']
    list_filter = ['permission_type']
    ordering = ['group']
    autocomplete_fields = ['user', 'group', 'resource', 'comment']

    admin.display(description="User Email")
    def user_email(self, obj):
        return obj.user.email if obj.user else None

    @admin.display(description="Group Name")
    def group_name(self, obj):
        return obj.group.name if obj.group else None

    @admin.display(description="Permissions")
    def get_permission_types(self, obj):
        return ", ".join(obj.get_permissions())  # Listni stringga aylantiramiz

@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ["code"]