import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime

from django.conf import settings
from .models import Article, MatchPoints, Player, Fixture, GalleryPhoto, Committee


BASE_URL = 'http://localhost:8000' if settings.DEBUG else 'https://www.ctsoftware.co.uk/blues-lax'


def home(req):
  articles = Article.objects.filter(show=True).order_by('-date')[:5]
  for i in range(len(articles)):
    # articles[i] = add_datestr_to_article(articles[i])  # not sure wy this doesn't work?!
    setattr(articles[i], 'datestr', f"{datetime.strftime(articles[i].date, '%-d %b %Y')}" )

  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'articles': articles
  }
  return render(req, 'home.html', context)


def team_info(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
  }
  return render(req, 'team-info.html', context)


def bluesfest(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
  }
  return render(req, 'bluesfest.html', context)

def find_us(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
  }
  return render(req, 'find-us.html', context)

def contact(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'committees': Committee.objects.filter(show=True)
  }
  return render(req, 'contact.html', context)


def privacy_policy(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
  }
  return render(req, 'privacy-policy.html', context)
  

def articles_list(req):
  articles = Article.objects.filter(show=True).order_by('-date')
  for i in range(len(articles)):
    # articles[i] = add_datestr_to_article(articles[i])  # not sure wy this doesn't work?!
    setattr(articles[i], 'datestr', f"{datetime.strftime(articles[i].date, '%-d %b %Y')}" )
    
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'articles': articles,
  }
  return render(req, 'articles.html', context)



def article(req, id):
  article = Article.objects.filter(show=True, id=id)
  if not article:
    context = {
      'LINK': req.build_absolute_uri(),
      'BASE_URL': BASE_URL,
    }
    return render(req, '404.html', context)
  else:
    article = article[0]
    setattr(article, 'datestr', f"{datetime.strftime(article.date, '%-d %b %Y')}" )  

  # need to set referee para. If it exists, it will be overwritten
  setattr(article, 'referee_para', '')

  # if it's a match, calculate the result
  is_match, goals, assists, mom, dod = False, {}, {}, {}, {}
  if article.type[-5:].lower() == 'match' and article.goals_for and article.goals_against:
    is_match = True
    goals_for = article.goals_for
    goals_against = article.goals_against
    if goals_for > goals_against:
      result, bigger, smaller = 'Win', goals_for, goals_against
    elif goals_for < goals_against:
      result, bigger, smaller = 'Loss', goals_against, goals_for
    else: 
      result, bigger, smaller = 'Draw', goals_against, goals_for

    setattr(article, 'result', f"<p class='result'>{bigger} - {smaller} {result}</p>" )  

    # add a paragraph about thanks to the referres
    if article.referees:
      setattr(article, 'referee_para', f"<p class='referee'>With thanks to {article.referees} for refereeing.</p>" )  


    # find any related points
    points = MatchPoints.objects.filter(match__id=id)    
    goals = points.filter(goals__gt=0).order_by('-goals')
    assists = points.filter(assists__gt=0).order_by('-assists')
    mom = points.filter(mom_votes__gt=0).order_by('-mom_votes')
    dod = points.filter(dod_votes__gt=0).order_by('-dod_votes')

  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'article': article,
    'paras': article.content.split('\n'),
    
    'is_match': is_match,
    'referee_para': article.referee_para,
    'goals': goals,
    'assists': assists,
    'moms': mom,
    'dods': dod,
  }
  return render(req, 'article.html', context)



def fixtures_results(req):
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
  }
  return render(req, 'fixtures-and-results.html', context)


def fixtures_results_data(req, team):
  
  if team == 'mens':
    mens = True
    fixtures = Fixture.objects.filter(show=True, type='Men\'s').order_by('date')
  elif team == 'womens1':
    mens = False
    fixtures = Fixture.objects.filter(show=True, type='Women\'s 1s').order_by('date')
  elif team == 'womens2':
    mens = False
    fixtures = Fixture.objects.filter(show=True, type='Women\'s 2s').order_by('date')

  # split into separate results and fixtures variables
  results = fixtures.filter(date__lt=datetime.now())
  fixtures = fixtures.filter(date__gt=datetime.now())
  for i in range(len(fixtures)):
    setattr(fixtures[i], 'datestr', f"{datetime.strftime(fixtures[i].date, '%-d %b %Y')}" )
  for i in range(len(results)):
    setattr(results[i], 'datestr', f"{datetime.strftime(results[i].date, '%-d %b %Y')}" )


  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'mens': mens,  # whether or not ot show the SEMLA table
    'team': team,
    'fixtures': fixtures,
    'results': results,
  }
  return render(req, 'fixtures-and-results-data.html', context)


def gallery(req):
  
  # Not sure where to put this routine. Settling for every time someone looks at the gallery page.
  # can't put in the model.save() method because of recursion. Didn't like having a separate API endpoint
  photos = GalleryPhoto.objects.all().order_by('order')
  for i in range(len(photos)):
    setattr(photos[i],'order',i+1)
    photos[i].save()
  
  # filter photos to only those that should be shown
  photos = photos.filter(show=True)

  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'photos': photos
  }
  return render(req, 'gallery.html', context)



def player_profiles(req):
  players = Player.objects.filter(show=True)
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'players_mens': players.filter(type='Mens').order_by('name'),
    'players_womens': players.filter(type='Womens').order_by('name'),
  }
  return render(req, 'player-profiles.html', context)

def player_profiles_with_id(req, id):
  players = Player.objects.filter(show=True)
  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'players_mens': players.filter(type='Mens').order_by('name'),
    'players_womens': players.filter(type='Womens').order_by('name'),
  }
  return render(req, 'player-profiles.html', context)


def player_profile(req, id):
  player = Player.objects.filter(show=True, id=id)
  if not player:
    context = {
      'LINK': req.build_absolute_uri(),
      'BASE_URL': BASE_URL,
    }
    return render(req, '404.html', context)
  else:
    player = player[0]

  about = player.about.split('\n')

  otol = player.one_truth_one_lie
  if otol:
    otol = otol.split('\n')
    otol = f"<ul><li>{otol[0]}</li><li>{otol[1]}</li></ul>"


  # select a profile at random for the 'random next profile' feature
  players = Player.objects.filter(show=True)
  random_profile = int(random.random() * len(players))
  random_profile = players[random_profile].id
  print('random profile = ', random_profile)

  # calculate age
  if player.dob:
    dob = datetime(player.dob.year, player.dob.month, player.dob.day)
    age = int((datetime.now() - dob).days / 365.25)
  else:
    age = ''

  context = {
    'LINK': req.build_absolute_uri(),
    'BASE_URL': BASE_URL,
    'player': player,
    'about': about,
    'otol': otol,
    'age': age,
    'MEDIA_URL': settings.MEDIA_URL,
    'random_profile': random_profile,
  }
  return render(req, 'player-profile.html', context)


def player_profile_ajax(req, id):
  if req.method == 'GET':
    player = Player.objects.filter(show=True, id=id)
    if not player:
      return JsonResponse({'error': True, 'message': 'Player with that Id does not exist'})
    else:
      player = player[0]

    # calculate age
    if player.dob:
      dob = datetime(player.dob.year, player.dob.month, player.dob.day)
      age = int((datetime.now() - dob).days / 365.25)
    else:
      age = ''
    
    try:
      photo_url = player.photo.url
    except:
      # photo_url = '/static/logo-blue-white.png'
      photo_url = ''


    return JsonResponse({
      'error': False,
      'player': {
        'id': player.id,
        'type': player.type,
        'image': photo_url,
        'name': player.name,
        'nicknames': player.nicknames,
        'clubs_played_for': player.clubs_played_for,
        'current_international': player.current_international,
        'former_international': player.former_international,
        'favourite_lax_moment': player.favourite_lax_moment,
        'position': player.position,
        'started_playing': player.started_playing,
        'about': player.about,
        'one_truth_one_lie': player.one_truth_one_lie,
        'age': age,
      }
      })
  else:
    return JsonResponse({'error': True, 'message': 'Method not recognised'})

