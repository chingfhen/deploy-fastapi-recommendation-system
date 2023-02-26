
# uvicorn recommender_api:app --host 0.0.0.0 --port 80 --reload

from recommenders.models.sar import SAR
# from recommenders.evaluation.python_evaluation import precision_at_k
import pandas as pd
import os
from scipy.sparse import save_npz, load_npz
from numpy import save, load 
import json
import yaml

from fastapi import FastAPI
from pydantic import BaseModel
from manychat import manychat_recommender
from  model_utils import *

# load the general model configurations
with open("/api/models/model-config.yml", "r") as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

# check if the model is supported
if config["MODEL_TYPE"] not in ["lightgcn","sar"]:
    raise ValueError("'MODEL' not recognized")
    

# load the specific model configurations
if config["MODEL_TYPE"]=="sar":
    model_config_path = "/api/models/sar-config.yml"
elif config["MODEL_TYPE"]=="lightgcn":
    model_config_path = "/api/models/lightgcn-config.yml"
with open(model_config_path, "r") as f:
    try:
        tmp_config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)
config.update(tmp_config)

# load the specific model
if config["MODEL_TYPE"]=="sar":
    model = SAR(
        col_user=config['COL_USER'],
        col_item=config['COL_ITEM'],
        col_rating=config['COL_RATING'],
        similarity_type=config['SIMILARITY_TYPE'], 
        time_decay_coefficient=30, 
        timedecay_formula=False,
        normalize=False
    )
    sar_load(model, config['MODEL_DIR'])

elif config["MODEL_TYPE"]=="lightgcn":
    raise ValueError("Oops Something went Wrong!")
    hparams = prepare_hparams(yaml_file,
                              n_layers=2,
                              loss_type = loss_type, 
                              loss_neg_weight = loss_neg_weight, 
                              log_wandb = log_wandb,
                              batch_size=BATCH_SIZE,
                              epochs=50,
                              learning_rate=0.01,
                              eval_epoch=1,
                              top_k=TOP_K,
                              COL_USER = USER_ID_COL,
                              COL_ITEM = ITEM_ID_COL,
                              COL_RATING = RATING_COL,
                              save_model = save_model,
                            save_epoch = save_epoch,
                            MODEL_DIR = MODEL_DIR
                              )
    # initiate model
    model = LightGCN(hparams, data, seed=SEED)
    model.load(config['MODEL_DIR'])



"""
The following class defines the arguments for the "recommend" endpoint
"""
class Query(BaseModel):
    user_id: str
    top_k: int
    

app = FastAPI()

"""
This endpoint makes top_k recommendations for user_id
user_id - id of user
top_k - number of recommendations to make
"""
# @app.post("/recommend")
@app.post("/recommend")
async def recommend(query: Query):
    model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=query.top_k, remove_seen=True)
    item_ids = model_output[config["COL_ITEM"]].tolist()
    return {"recommendations": item_ids}


app.include_router(manychat_recommender.manychat_router)


