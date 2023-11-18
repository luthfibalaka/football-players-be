from rest_framework.decorators import api_view
from django.http.response import JsonResponse, HttpResponseBadRequest
from rdflib import Graph
from .utils import query_league_info_dbpedia, query_language_used_wikidata

import os


knowledge_graph = Graph()
knowledge_graph.parse(os.path.join(os.getcwd(), os.path.join("main", "top_5_league_player.ttl")))
iri_prefix = "http://127.0.0.1:3333#"


@api_view(["GET"])
def get_player_detail(request, player_iri_suffix: str):
    """
    Return details of a player given his IRI
    """
    try:
        query = f"""
            PREFIX : <{iri_prefix}>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT *
            WHERE {{
                :{player_iri_suffix} :name ?name;
                                    :age ?age;
                                    :nationality [rdfs:label ?nationality];
                                    :position [rdfs:label ?position];
                                    :shirt_num ?shirt_num;
                                    :club [rdfs:label ?club];
                                    :joined_club ?joined_club;
                                    :league [rdfs:label ?league] .
                OPTIONAL {{
                :{player_iri_suffix} :full_name ?full_name;
                                        :height ?height;
                                        :place_of_birth [rdfs:label ?place_of_birth];
                                        :price ?price;
                                        :max_price ?max_price;
                                        :contract_expires ?contract_expires;
                }}
            }}
        """

        player_detail = {}
        for result in knowledge_graph.query(query):
            player_detail["name"] = result["name"].strip()
            player_detail["age"] = result["age"]
            player_detail["nationality"] = result["nationality"]
            player_detail["position"] = result["position"]
            player_detail["shirt_num"] = result["shirt_num"]
            player_detail["club"] = result["club"]
            player_detail["joined_club"] = result["joined_club"]
            player_detail["league"] = result["league"].strip()
            player_detail["full_name"] = result["full_name"]
            player_detail["height"] = result["height"]
            player_detail["place_of_birth"] = result["place_of_birth"]
            player_detail["price"] = result["price"]
            player_detail["max_price"] = result["max_price"]
            player_detail["contract_expires"] = result["contract_expires"]

        # Add league information from DBPedia
        if player_detail["league"] != "Other":
            player_detail["league_description"] = query_league_info_dbpedia(
                player_detail["league"]
            )
        else:
            player_detail["league_description"] = "No information"

        # Add language used by player from Wikidata
        (
            player_detail["language_iri"],
            player_detail["languaged_used"],
        ) = query_language_used_wikidata(player_detail["name"])

        return JsonResponse(player_detail)
    except:
        return HttpResponseBadRequest("Please provide correct player's IRI suffix!")
