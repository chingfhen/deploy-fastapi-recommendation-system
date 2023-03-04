# sar
from recommenders.models.sar import SAR
# lightgcn
# from recommenders.models.deeprec.models.graphrec.lightgcn import LightGCN
# from recommenders.models.deeprec.deeprec_utils import prepare_hparams
# general
import yaml
import os

from model_utils import sar_load


"""
MODEL
"""
# load configurations
local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\config\model-config.yaml"
volume_path = "/config/model-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        model_config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

# check if the model is supported
if model_config["MODEL_TYPE"] not in model_config["MODEL_SUPPORTED_TYPES"]:
    raise ValueError("'MODEL' not recognized")
    
# load specific model configurations
if model_config["MODEL_TYPE"]=="sar":
    local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\config\sar-config.yaml"
    volume_path = "/config/sar-config.yaml"
    config_path = local_path if os.path.exists(local_path) else volume_path
elif model_config["MODEL_TYPE"]=="lightgcn":
    local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\config\lightgcn-config.yaml"
    volume_path = "/config/lightgcn-config.yaml"
    config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        model_config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)

# load the specific model
if model_config["MODEL_TYPE"]=="sar":
    local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\api\models\arietes-sar"
    model_path = local_path if os.path.exists(local_path) else model_config['MODEL_DIR']
    model = SAR(
        col_user=model_config['COL_USER'],
        col_item=model_config['COL_ITEM'],
        col_rating=model_config['COL_RATING'],
        similarity_type=model_config['SIMILARITY_TYPE'], 
        time_decay_coefficient=30, 
        timedecay_formula=False,
        normalize=False
    )
    sar_load(model, model_path)

elif model_config["MODEL_TYPE"]=="lightgcn":
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
    model.load(model_config['MODEL_DIR'])

if __name__ == "__main__":
    print("Done")
    