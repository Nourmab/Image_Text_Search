import backend_config
from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request
import utils 

app = FastAPI()
client = Elasticsearch([backend_config.elastic_url])


def check_server(client):
    if client.ping() is False:
        print("Elastic Search Server Is Not Running!")

@app.get("/")
async def root():
    return {"it is working"}

# Search by text 
@app.post("/search_by_text")
async def search_by_text(request: Request):
    content = await request.json()
    text = content["tags"]
    search_type = content["type"]
    show_result = int(content["number"])
    return utils.get_results_search_by_text(text, search_type,show_result)
#------------------------------------------------------------------------

# Search by image
@app.post("/search_by_image")
async def get_feature_from_image(request: Request):
    content = await request.json()
    # print(content)
    img = content["img"]
    show_result = int(content["number"])
    return utils.get_results_search_by_image(img, show_result)

#--------------------------------------------------------------------------

# #Search by url
# @app.post("/search_by_url/")
# async def get_feature_from_url(request: Request):
#     content = await request.json()
#     url = content["url"]
#     show_result = int(content["number"])
#     return utils.get_results_search_by_url(url, show_result)

#-------------------------------------------------------------------

# #Search by both by image & Text
# @app.post("/search_by_image_and_text") 
# async def search_by_image_and_text(request : Request) :
#     content = await request.json()
#     # print("this is a content for text and image search " , content)
#     image = content["img"]
#     question = content["query"]
#     search_type = content["type"]
#     show_result = int(content["number"])    
#     return utils.get_results_search_by_image_and_text(image,question,search_type,show_result)

