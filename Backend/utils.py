import backend_config as config
from elasticsearch import Elasticsearch
from feature_extractor import FeatureExtractor


client = Elasticsearch(
    [config.elastic_url], basic_auth=(config.elastic_usr, config.elastic_pass)
)
fe = FeatureExtractor()
similarity_threshold = config.threshold

#=====================================================================

def get_results_search_by_text(query, search_type):
    getreq = {
            search_type: {"tags":query}
    }
    results = client.search(index=config.index_text, query=getreq)
    #print(results)
    return {"resulttype": results}


#=====================================================================

def get_results_search_by_image(img, show_result):
    feature_vector = fe.get_from_image(img)
    # print(feature_vector)
    body = {
        "size": show_result,  
        "min_score": similarity_threshold + 1.0,  
        "_source": ["path"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": """
                        cosineSimilarity(params.query_vector, 'feature_vector') + 1.0
                    """,
                    "params": {
                        "query_vector": feature_vector.tolist()
                    }
                }
            }
        }
    }    
    try:
        results = client.search(
            index=config.index, body=body
        )
        print(results)
        return {"resulttype": results}
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
        return None 



#=======================================================================



def get_results_search_by_url(url, show_result):
    feature_vector = fe.get_from_link(url)
    print(feature_vector)
    body = {
        "size": show_result,  
        "min_score": similarity_threshold + 1.0,  
        "_source": ["path"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": """
                        cosineSimilarity(params.query_vector, 'feature_vector') + 1.0
                    """,
                    "params": {
                        "query_vector": feature_vector.tolist()
                    }
                }
            }
        }
    }    

    try:
        results = client.search(
            index=config.index, body=body
        )
        print(results)
        return {"resulttype": results}
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
        return None 
    



#=====================================================================

