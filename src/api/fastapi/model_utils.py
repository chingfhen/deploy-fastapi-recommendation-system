from scipy.sparse import save_npz, load_npz
from numpy import save, load 
import json
import os


"""
Load SAR model
"""
def sar_load(model, directory):
    model.user_affinity = load_npz(file = os.path.join(directory,"sar_user_affinity.npz"))
    model.item_similarity = load(file = os.path.join(directory,"sar_item_similarity.npy"))
    with open(os.path.join(directory,"sar_user2index.json"), "r") as f:
        tmp_dict = json.load(f)
        model.user2index = tmp_dict
    with open(os.path.join(directory,"sar_index2item.json"), "r") as f:
        tmp_dict =  json.load(f)
        model.index2item = {int(k):v for k,v in tmp_dict.items()}
   
"""
Save SAR model
"""
def save_sar(model, directory, model_name):
    model_directory = os.path.join(directory, model_name)
    os.makedirs(model_directory, exist_ok=True)
    save_npz(file = os.path.join(model_directory, "sar_user_affinity.npz"), 
             matrix = model.user_affinity, 
             compressed=True)
    save(file = os.path.join(model_directory, "sar_item_similarity.npy"),
         arr = model.item_similarity)
    with open(os.path.join(model_directory, "sar_user2index.json"), "w") as f:
        json.dump(model.user2index, f)
    with open(os.path.join(model_directory, "sar_index2item.json"), "w") as f:
        json.dump(convert_numpy_keys_to_raw(model.index2item), f)
        
   
"""
Helper function to convert numpy keys in a dictionary to raw values
"""
def convert_numpy_keys_to_raw(d):
    non_numpy_keys = list(map(int,d.keys()))
    non_numpy_values = list(map(int,d.values()))
    return dict(zip(non_numpy_keys,non_numpy_values))  