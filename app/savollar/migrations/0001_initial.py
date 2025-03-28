# Generated by Django 5.1.4 on 2025-03-11 18:10

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="Savol"),
                ),
                ("is_correct", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "User-Javob",
                "verbose_name_plural": "User-Javoblari",
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="Savol"),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="Savol"),
                ),
                ("time_limit", models.PositiveIntegerField(default=600)),
            ],
            options={
                "verbose_name": "Quiz",
                "verbose_name_plural": "Quizzes",
                "ordering": ["-created_at"],
            },
        ),
    ]
