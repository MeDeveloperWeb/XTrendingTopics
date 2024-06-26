# Generated by Django 4.1.13 on 2024-06-05 07:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('ip', models.CharField(max_length=50)),
                ('dateTime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=128)),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='whatsTrending.ip')),
            ],
        ),
    ]
