from logging import RootLogger
from django.db import models
from datetime import datetime


class Article(models.Model):
  show = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)

  class Type(models.TextChoices):
    MENS_MATCH = 'Men\'s Match', 'Men\'s Match'
    WOMENS1_MATCH = 'Women\'s 1s Match', 'Women\'s 1s Match'
    WOMENS2_MATCH = 'Women\'s 2s Match', 'Women\'s 2s Match'
    GENERAL_ANNOUNCEMENT = 'General', 'General'

  type = models.CharField(max_length=50, choices=Type.choices, null=False, blank=False)

  date = models.DateField(null=False, blank=False, default=datetime.now)
  title = models.CharField(max_length=100, null=False, blank=False)
  content = models.TextField(blank=False, null=False)
  preview = models.TextField(blank=True, null=True, max_length=300)

  # match-report-specific info
  goals_for = models.IntegerField(null=True, blank=True)
  goals_against = models.IntegerField(null=True, blank=True)
  referees = models.CharField(blank=True, null=True, max_length=200)
  stats_link = models.CharField(blank=True, null=True, max_length=200)

  class Meta:
    ordering = ['-last_updated']

  def __str__(self):
    return f"{self.date} - {self.type} - {self.title}"



class Player(models.Model):
  show = models.BooleanField(default=False)

  class Type(models.TextChoices):
    MENS = 'Mens', 'Mens'
    WOMENS = 'Womens', 'Womens'

  type = models.CharField(max_length=20, choices=Type.choices, null=True, blank=True)

  name = models.CharField(max_length=100)
  nicknames = models.CharField(max_length=200, null=True, blank=True)
  dob = models.DateField(null=True, blank=True)

  clubs_played_for = models.CharField(max_length=200, null=True, blank=True)
  current_international = models.BooleanField(default=False)
  former_international = models.BooleanField(default=False)
  favourite_lax_moment = models.TextField(null=True, blank=True)

  position = models.CharField(max_length=100, null=True, blank=True)
  photo = models.ImageField(upload_to='profiles/',null=True, blank=True)
  started_playing = models.CharField(max_length=100, null=True, blank=True)
  about = models.TextField(null=True, blank=True)
  one_truth_one_lie = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['name']



class MatchPoints(models.Model):
  show = models.BooleanField(default=True)
  match = models.ForeignKey(Article, on_delete=models.CASCADE)
  player = models.ForeignKey(Player, on_delete=models.CASCADE)

  goals = models.IntegerField(default=0, null=True, blank=True)
  assists = models.IntegerField(default=0, null=True, blank=True)
  mom_votes = models.IntegerField(default=0, null=True, blank=True)
  mom_reason = models.CharField(max_length=200, blank=True, null=True)
  dod_votes = models.IntegerField(default=0, null=True, blank=True)
  dod_reason = models.CharField(max_length=200, blank=True, null=True)


  def __str__(self):
    return f"{self.player} - {self.match}"


class Fixture(models.Model):
  show = models.BooleanField(default=True)
  opposition = models.CharField(max_length=100, null=False, blank=False)
  date = models.DateField(null=True, blank=True)

  class LocationChoices(models.TextChoices):
    HOME = 'Home', 'Home'
    AWAY = 'Away', 'Away'
    NEUTRAL = 'Neutral', 'Neutral'
  location = models.CharField(max_length=20, null=True, blank=True, choices=LocationChoices.choices)

  class TypeChoices(models.TextChoices):
    MENS = 'Men\'s', 'Men\'s'
    WOMENS_1s = 'Women\'s 1s', 'Women\'s 1s'
    WOMENS_2s = 'Women\'s 2s', 'Women\'s 2s'
  type = models.CharField(max_length=20, null=True, blank=True, choices=TypeChoices.choices)

  class CompetitionChoices(models.TextChoices):
    LEAGUE = 'League', 'League'
    LOCAL = 'Local', 'Local'
    CUP = 'Cup', 'Cup'
    OTHER = 'Other', 'Other'
  competition = models.CharField(max_length=20, null=True, blank=True, choices=CompetitionChoices.choices)

  report = models.OneToOneField(Article, null=True, blank=True, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.date} - {self.opposition}"



class GalleryPhoto(models.Model):
  show = models.BooleanField(default=True)
  image = models.ImageField(upload_to='gallery/',null=False, blank=False)
  order = models.IntegerField(null=False, blank=False)
  caption = models.CharField(max_length=100, null=True, blank=True)
  datetime_created = models.DateTimeField(auto_now_add=True)
  # landscape = models.BooleanField(default=False)

  def __str__(self):
    return self.caption

class Committee(models.Model):

  show = models.BooleanField(default=True)
  name = models.CharField(max_length=100, null=True, blank=True)
  role = models.CharField(max_length=100, null=True, blank=True)
  email = models.CharField(max_length=100, null=True, blank=True)
  phone = models.CharField(max_length=100, null=True, blank=True)


  def __str__(self):
    return f"{self.name} ({self.role})"
