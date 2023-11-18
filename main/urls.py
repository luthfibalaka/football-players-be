from django.urls import path
from .views import get_player_detail

app_name = "account"

urlpatterns = [
    path("detail/<player_iri_suffix>", get_player_detail, name="getPlayerDetail"),
]
