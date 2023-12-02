from django.urls import path
from .views.mainViews import get_player_detail
from .views.searchByLeagueViews import search_by_league
from .views.searchByClubViews import search_by_club

app_name = "account"

urlpatterns = [
    path("detail/<player_iri_suffix>", get_player_detail, name="getPlayerDetail"),
    path("search-by-league/", search_by_league, name="searchByLeague"),
    path("search-by-club/", search_by_club, name="searchByClub"),
]
