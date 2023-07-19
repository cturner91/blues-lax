"""blues_lax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from info.views import home, articles_list, article, player_profile, bluesfest, find_us, contact, team_info, privacy_policy, fixtures_results, player_profiles, gallery, fixtures_results_data, player_profile_ajax, player_profiles_with_id
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('bluesfest/', bluesfest),
    path('team-info/', team_info),
    path('find-us/', find_us),
    path('contact/', contact),
    path('privacy-policy/', privacy_policy),

    path('gallery/', gallery),

    path('articles/', articles_list),
    path('articles/<int:id>/', article),

    path('player-profiles/', player_profiles),
    path('player-profiles/<int:id>', player_profiles_with_id),
    path('player-profiles-ajax/<int:id>', player_profile_ajax),

    path('fixtures-results/', fixtures_results),
    path('fixtures-results/<str:team>/', fixtures_results_data),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
