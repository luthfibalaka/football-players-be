from django.urls import path
from .views import get_player_detail, search_by_league

app_name = "account"

urlpatterns = [
    path("detail/<player_iri_suffix>", get_player_detail, name="getPlayerDetail"),
    path("search-by-id/", search_by_league, name="searchByLeague"),
]
