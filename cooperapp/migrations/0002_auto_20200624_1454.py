# Generated by Django 3.0.5 on 2020-06-24 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooperapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooperativeprojectcontributors',
            name='project_name',
        ),
        migrations.AddField(
            model_name='cooperativeprojectcontributors',
            name='cooperative_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cooperapp.UserProfile'),
        ),
    ]
