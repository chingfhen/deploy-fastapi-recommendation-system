
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

# read the configurations for the recommender algorithm
with open("/api/models/sar.yml", "r") as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

"""
The following function loads the trained SAR model
    args:
        model - SAR model instance from the recommenders library
        directory - directory containing the trained model parameters
"""
def sar_load(model, directory):
    model.user_affinity = load_npz(file = os.path.join(directory,"sar_user_affinity.npz"))
    model.item_similarity = load(file = os.path.join(directory,"sar_item_similarity.npy"))
    with open(os.path.join(directory,"sar_index2item.json"), "r") as f:
        tmp_dict =  json.load(f)
        model.index2item = {int(k):v for k,v in tmp_dict.items()}
    with open(os.path.join(directory,"sar_user2index.json"), "r") as f:
        model.user2index = json.load(f)
        
# load the trained SAR model
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





# from recommenders.datasets.python_splitters import python_stratified_split
# from recommenders.utils.constants import SEED as DEFAULT_SEED
# from recommenders.evaluation.python_evaluation import precision_at_k
# from recommenders.models.deeprec.DataModel.ImplicitCF import ImplicitCF
# from recommenders.models.deeprec.deeprec_utils import prepare_hparams
# from recommenders.models.deeprec.models.graphrec.lightgcn import LightGCN
# from recommenders.utils.timer import Timer

# import pandas as pd
# import os
# from fastapi import FastAPI
# from pydantic import BaseModel


# train_path = "./data/train.pkl"
# test_path = "./data/test.pkl"
# yaml_file = "./models/lightgcn.yml"
# train = pd.read_pickle(train_path)
# test = pd.read_pickle(test_path)

# COL_USER, COL_ITEM, COL_RATING = "user_id", "item_id", "rating"
# SEED = 0 
# TOP_K = 10
# BATCH_SIZE = 1024
# loss_type = "AmpBPR2"
# loss_neg_weight = 1.5
# log_wandb = False

# data = ImplicitCF(train = train, test=test, 
#                   adj_dir=None, 
#                   col_user=COL_USER, col_item=COL_ITEM, 
#                   col_rating = COL_RATING,
#                   seed=SEED)

# # for i in range(3):
# hparams = prepare_hparams(yaml_file,
#                               n_layers=2,
#                               loss_type = loss_type, 
#                               loss_neg_weight = loss_neg_weight, 
#                               log_wandb = log_wandb,
#                               batch_size=BATCH_SIZE,
#                               epochs=50,
#                               learning_rate=0.005,
#                               eval_epoch=1,
#                               top_k=TOP_K,
#                               COL_USER = COL_USER,
#                               COL_ITEM = COL_ITEM,
#                               COL_RATING = COL_RATING,

#                               )
# # initiate model
# model = LightGCN(hparams, data, seed=SEED)
    

# class Query(BaseModel):
#     user_id: str
#     top_k: int
    

# app = FastAPI()


# @app.post("/recommend")
# async def recommend(query: Query):
#     model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=query.top_k, remove_seen=True)
#     item_ids = model_output[COL_ITEM].tolist()
#     return {"recommendations": item_ids}


