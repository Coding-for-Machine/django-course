from django.db import models
from lessons.models import Problem
from courses.models import Course
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class Grade(models.Model):
    student = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name="grades"
    )
    teacher = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="given_grades", limit_choices_to={'role': 'teacher'}
    )
    problems = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="grades"
    )
    score = models.PositiveIntegerField(verbose_name="Baho", default=1)
    comment = models.TextField(blank=True, null=True, verbose_name="Izoh")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'problems'], name='unique_student_problem_grade')
        ]
        permissions = [
            ("can_add_grade", "Baho qo‘yish"),
            ("can_view_grades", "Baholarni ko‘rish"),
        ]
        ordering = ['-created']

    def __str__(self):
        return f"{self.student.first_name} - {self.problems.lesson.title}: {self.score} ({self.teacher.first_name})"


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="owner_groups")
    students = models.ManyToManyField(
        MyUser, 
        blank=True, 
        related_name="student_groups"  # To‘g‘rilangan
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GroupInvite(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"

    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="sent_invites")
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="received_invites")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invites")
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"


class Resource(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="groups/resources/")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="resources")
    uploaded_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="uploaded_resources")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        MyUser, 
        on_delete=models.CASCADE, 
        related_name="user_comments"  # To‘g‘rilangan
    )
    lesson = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, related_name="comments")
    resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email}: {self.content[:30]}..."


class PermissionType(models.Model):
    class PermissionChoices(models.TextChoices):
        READ = "r", "Read"
        WRITE = "w", "Write"
        CREATE = "c", "Create"
        DELETE = "d", "Delete"
    code = models.CharField(max_length=1, choices=PermissionChoices.choices, unique=True)

    def __str__(self):
        return self.get_code_display() 
    
class Permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="permissions")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="permissions")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True, related_name="resource_permissions")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_permissions")
    
    permission_type = models.ManyToManyField(
        PermissionType,
        related_name="user_permissions"
    )

    class Meta:
        unique_together = ("group", "user", "resource", "comment")
        ordering = ["group", "user"]


    def __str__(self):
        return f"{self.user.email} - {self.group.name} - {', '.join(self.get_permissions())}"

    def get_permissions(self):
        return [perm.get_code_display() for perm in self.permission_type.all()]  # To'g'ri ishlaydi
