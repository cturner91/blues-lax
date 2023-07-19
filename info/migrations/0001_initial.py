# Generated by Django 3.2.2 on 2023-07-19 20:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[("Men's Match", "Men's Match"), ("Women's 1s Match", "Women's 1s Match"), ("Women's 2s Match", "Women's 2s Match"), ('General', 'General')], max_length=50)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('preview', models.TextField(blank=True, max_length=300, null=True)),
                ('goals_for', models.IntegerField(blank=True, null=True)),
                ('goals_against', models.IntegerField(blank=True, null=True)),
                ('referees', models.CharField(blank=True, max_length=200, null=True)),
                ('stats_link', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['-last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='gallery/')),
                ('order', models.IntegerField()),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=False)),
                ('type', models.CharField(blank=True, choices=[('Mens', 'Mens'), ('Womens', 'Womens')], max_length=20, null=True)),
                ('name', models.CharField(max_length=100)),
                ('nicknames', models.CharField(blank=True, max_length=200, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('clubs_played_for', models.CharField(blank=True, max_length=200, null=True)),
                ('current_international', models.BooleanField(default=False)),
                ('former_international', models.BooleanField(default=False)),
                ('favourite_lax_moment', models.TextField(blank=True, null=True)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('started_playing', models.CharField(blank=True, max_length=100, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('one_truth_one_lie', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MatchPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True)),
                ('goals', models.IntegerField(blank=True, default=0, null=True)),
                ('assists', models.IntegerField(blank=True, default=0, null=True)),
                ('mom_votes', models.IntegerField(blank=True, default=0, null=True)),
                ('mom_reason', models.CharField(blank=True, max_length=200, null=True)),
                ('dod_votes', models.IntegerField(blank=True, default=0, null=True)),
                ('dod_reason', models.CharField(blank=True, max_length=200, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.article')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.player')),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True)),
                ('opposition', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, choices=[('Home', 'Home'), ('Away', 'Away'), ('Neutral', 'Neutral')], max_length=20, null=True)),
                ('type', models.CharField(blank=True, choices=[("Men's", "Men's"), ("Women's 1s", "Women's 1s"), ("Women's 2s", "Women's 2s")], max_length=20, null=True)),
                ('competition', models.CharField(blank=True, choices=[('League', 'League'), ('Local', 'Local'), ('Cup', 'Cup'), ('Other', 'Other')], max_length=20, null=True)),
                ('report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info.article')),
            ],
        ),
    ]