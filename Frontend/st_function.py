import requests
import streamlit as st
import base64
import os

base_url = "http://localhost:8000"

# Display result search 
def display_image(response):
    cols = st.columns(2)
    col_heights = [0, 0]
    if response.status_code == 200:
        data = response.json()
        # print("this is data : ", data)
        if data ["resulttype"]["hits"]["total"]["value"] == 0:
            st.warning("No results found")
        for hit in data["resulttype"]["hits"]["hits"]:
            image = hit["_source"]["path"]
            # print("image name is : ",image)
            col_id = 0 if col_heights[0] <= col_heights[1] else 1
            with st.spinner("Loading Image"):
                cols[col_id].image(image)
                col_heights[col_id] += 1

def display_results(response, cols):
    cols = st.columns(4)
    col_heights = [0, 0 , 0 , 0 ]
    displayed_images = 0
    data= response.json()
    #print(data)
    for hit in data["resulttype"]['hits']['hits']:
        if displayed_images >= 10:
            break
        image_data = hit["_source"]
        image= "http://farm"+image_data['flickr_farm']+".staticflickr.com/"+image_data['flickr_server']+"/"+image_data["id"]+"_"+image_data['flickr_secret']+".jpg"
        col_id = col_heights.index(min(col_heights))
        with cols[col_id]:  # Utilisez la colonne identifiée
            with st.spinner("Loading Image"):
                response = requests.get(image)
                if response.status_code == 200:
                    st.image(image)
                    col_heights[col_id] += 1  # Augmentez la hauteur de la colonne
                    displayed_images += 1     


#This Function allow us to search images by Text
def search_by_text(query, search_type, show_result, cols):
    url = base_url + "/search_by_text/"
    json = {"tags": query, "type": search_type, "number": show_result}
    response = requests.post(url, json=json)
    display_results(response, cols)

#This Function allow us to search images by image  

# def search_by_url(link, show_result):
#     url = base_url + "/search_by_url/"
#     link = base64encode(requests.get(url).content)
#     json = {"url": link, "number": show_result}
#     response = requests.post(url, json=json)
#     display_image(response)


def search_by_upload_image(uploaded, show_result):
    url = base_url + "/search_by_image"
    image_base64 = base64.b64encode(uploaded).decode("utf-8")
    json = {"img": image_base64, "number": show_result}
    response = requests.post(url, json=json)
    print(response)
    display_image(response)
# This Function allow us to search booth with image and text 

# def search_by_image_and_text(query, uploaded, search_type, show_result):
#     url = base_url + "/search_by_image_and_text/"
#     image_base64 = base64.b64encode(uploaded).decode("utf-8")
#     json = {
#         "img": image_base64,
#         "query": query,
#         "type": search_type,
#         "number": show_result,
#     }
#     response = requests.post(url, json=json)
#     display_image(response)
