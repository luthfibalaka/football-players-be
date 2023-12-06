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
def search_by_name(request):
    """
    Return IRI and name of players given league
    - Sample usage: http://127.0.0.1:8000/search-by-id/?name=Jordan_Ferri
    """
    name = request.GET.get("name", "Other")
    print(name)
    query = f"""
        PREFIX : <{iri_prefix}>

        SELECT *
        WHERE {{
            ?player_iri a :FootballPlayer;
                            :name ?name;
            FILTER(REGEX(?name, "^.*{name}", "i")).
        }}
    """
    players = {}
    # print(query)
    for result in knowledge_graph.query(query):
        print(result)
        players[result["player_iri"].strip()] = result["name"].strip()
    return JsonResponse(players)