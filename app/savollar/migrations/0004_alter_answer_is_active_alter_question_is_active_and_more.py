# Generated by Django 5.1.4 on 2025-03-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("savollar", "0003_rename_mymodules_quiz_modules"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
