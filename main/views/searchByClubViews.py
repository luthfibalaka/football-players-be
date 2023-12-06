from rest_framework.decorators import api_view
from django.http.response import JsonResponse, HttpResponseBadRequest
from rdflib import Graph

import os


knowledge_graph = Graph()
knowledge_graph.parse(
    os.path.join(os.getcwd(), os.path.join("main", "top_5_league_player.ttl"))
)
iri_prefix = "http://127.0.0.1:3333#"

@api_view(["GET"])
def search_by_club(request):
    """
    Return IRI and name of players given league
    - Sample usage: http://127.0.0.1:8000/search-by-id/?club=AJAuxerre
    """
    club = request.GET.get("club", "Other")
    query = f"""
        PREFIX : <{iri_prefix}>

        SELECT *
        WHERE {{
            ?player_iri a :FootballPlayer;
                            :name ?name;
                            :club :{club} .
        }}
    """
    players = {}
    for result in knowledge_graph.query(query):
        players[result["player_iri"].strip()] = result["name"].strip()
    return JsonResponse(players)