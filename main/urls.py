from django.urls import path
from .views.mainViews import get_player_detail
from .views.searchByLeagueViews import search_by_league
from .views.searchByPositionViews import search_by_position
from .views.searchByClubViews import search_by_club
from .views.searchByNameViews import search_by_name

app_name = "account"

urlpatterns = [
    path("detail/<player_iri_suffix>", get_player_detail, name="getPlayerDetail"),
    path("search-by-id/", search_by_league, name="searchByLeague"),
    path("search-by-position/", search_by_position, name="searchByPosition"),
    path("search-by-league/", search_by_league, name="searchByLeague"),
    path("search-by-club/", search_by_club, name="searchByClub"),
    path("search-by-name/", search_by_name, name="searchByName"),
]
