# Generated by Django 5.1.4 on 2025-03-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grade", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="grade",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="group",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="groupinvite",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="permission",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="permissiontype",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="resource",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
