

import pandas as pd
import json
from fastapi import FastAPI
from pydantic import BaseModel
import yaml
import os
from db import database_config, database_connection, database_cursor, get_product_info
from model import model_config, model


# load config
config = {}
config.update(database_config)
config.update(model_config)


local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\config\seller-config.yaml"
volume_path = "/config/seller-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)

"""
Input for "recommend" endpoint
"""
class Query(BaseModel):
    user_id: str
    top_k: int

"""
FASTAPI
"""
app = FastAPI()
"""
Standard Recommendation
Input: Query
Output: {"recommendations": [item123,item321]}
"""
# @app.post("/recommend")
@app.post("/recommend")
async def recommend(query: Query):
    model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=min(query.top_k, config["TOP_K"]), remove_seen=True)
    item_ids = model_output[config["COL_ITEM"]].tolist()
    return {"recommendations": item_ids}
"""
ManyChat Response
Input: Query
Output: 
    - 1 item recommendation
    - item details e.g. title, product url, image url
"""
@app.post("/manychat/recommend")
async def manychat_recommend(query: Query):
    # make recommendation
    model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=min(query.top_k, 1), remove_seen=True)
    item_ids = model_output[config["COL_ITEM"]].tolist()  
    item_id = int(item_ids[0])

    # retrieve product info
    print(item_id, type(item_id))
    product_id, product_name, categories, image_url = get_product_info(database_cursor, item_id)
    product_url = f"https://shopee.sg/product/{config['SELLER_ID']}/{product_id}"

    
    return {
        "version": "v2",
        "content": {
            "messages": [
                {
                    "type": "image",
                    "url": image_url,
                    # "buttons": [
                    #     {
                    #         "type": "url",
                    #         "caption": "Product Link",
                    #         "url": product_url,
                    #         "webview_size": "full"
                    #     },
                    #     {
                    #         "type": "url",
                    #         "caption": config['SHOP_NAME'],
                    #         "url": config['SHOP_URL'],
                    #         "webview_size": "full"
                    #     }
                    # ]
                },
                # {
                #     "type": "text",
                #     "text": product_name
                # }
                ],
            # "actions": [],
            # "quick_replies": []
        }
    }

if __name__=="__main__":
    # product_id, product_name, categories, image_url = get_product_info(database_cursor, 23821143235)
    # print(product_id, product_name, categories, image_url )
    print("recommender_apy.py done")



# read environment variables
# DATABASE_FOLDER = os.environ.get('DATABASE_FOLDER')
# DATABASE_NAME = os.environ.get('DATABASE_NAME')

# # establish database connection
# database_connection = sqlite3.connect(f"{DATABASE_DIR}/{DATABASE_NAME}.db" if DATABASE_FOLDER is not None else "/database/sqlite3/arietes_product_info.db")
# database_cursor = database_connection.cursor()

# manychat endpoints
# manychat_router = APIRouter()
# app.include_router(manychat_recommender.manychat_router)





