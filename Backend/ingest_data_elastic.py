import os
from elasticsearch import Elasticsearch
from feature_extractor import FeatureExtractor
from PIL import Image
import backend_config as config

index=config.index
fe=FeatureExtractor()

# Function to connect to Elasticsearch and create an index
def create_elastic_index(client, index_name):
    if client.indices.exists(index=index_name):
        print(f"Index {index_name} already exists. Skipping creation.")
    else:
        client.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "path": {"type": "keyword"},
                    "feature_vector": {"type": "dense_vector", "dims": 4096}
                }
            }
        })
        print(f"Index {index_name} created.")
        

# Function to index image data into Elasticsearch
def index_image_data(client, index_name, image_path, feature_vector):
    doc = {
        "path": image_path,
        "feature_vector": feature_vector.tolist()  
    }
    client.index(index=index_name, body=doc)
    print(f"Indexed {image_path}")
    

if __name__ == "__main__":
    
    es = Elasticsearch(config.elastic_url)
    create_elastic_index(es,index)
    images_path=config.dataPath
    for i in range(10):
        new_path=f"{images_path}/{i}"
        for img_file in os.listdir(new_path):
            img_path = os.path.join(new_path, img_file)
            img = Image.open(img_path)
            # Extract feature vector
            feature_vector = fe._extract(img)
            index_image_data(es, index, img_path, feature_vector)