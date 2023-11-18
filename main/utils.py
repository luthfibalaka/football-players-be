from SPARQLWrapper import SPARQLWrapper, JSON
import sys


def query_league_info_dbpedia(league_name: str) -> str:
    """
    Return abstract of league_name of the player
    """
    try:
        league_suffix = ""
        if league_name == "EPL":
            league_suffix += "Premier_League"
        elif league_name == "SerieA":
            league_suffix += "Serie_A"
        elif league_name == "Bundesliga":
            league_suffix += league_name
        elif league_name == "LaLiga":
            league_suffix += "La_Liga"
        else:
            league_suffix += "Ligue_1"

        query = f"""
            SELECT ?description
            WHERE {{
                dbr:{league_suffix} dbo:abstract ?description .
                FILTER(LANG(?description) = "en")
            }}
        """

        sparql_wrapper = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql_wrapper.setQuery(query)
        sparql_wrapper.setReturnFormat(JSON)
        return sparql_wrapper.query().convert()["results"]["bindings"][0][
            "description"
        ]["value"]
    except:
        return "No league details found!"


def query_language_used_wikidata(name: str) -> tuple[str, str]:
    """
    Return language used by the player, return IRI & label of the language
    """
    try:
        query = f"""
            SELECT *
            WHERE {{
            ?player rdfs:label "{name}"@en .
            ?player wdt:P1412 ?languageIRI .
            ?languageIRI wdt:P1705 ?languageUsed .
            }}
            LIMIT 1
        """
        user_agent = "WDQS-example Python/%s.%s" % (
            sys.version_info[0],
            sys.version_info[1],
        )
        endpoint_url = "https://query.wikidata.org/sparql"
        sparql_wrapper = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql_wrapper.setQuery(query)
        sparql_wrapper.setReturnFormat(JSON)
        results = sparql_wrapper.query().convert()["results"]["bindings"][0]
        return (results["languageIRI"]["value"], results["languageUsed"]["value"])
    except:
        return "No language information found!"
