# Generated by Django 3.1.2 on 2020-11-05 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.course'),
        ),
    ]