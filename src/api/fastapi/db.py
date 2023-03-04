import mysql.connector
import os
import yaml
from classes import Product

# load configurations
local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\config\database-config.yaml"
volume_path = "/config/database-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        database_config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

# establish database connection
database_connection = mysql.connector.connect(
    user=database_config['DATABASE_USER'], password=database_config['DATABASE_PASSWORD'],
    host=database_config['DATABASE_HOST'],
    database=database_config['DATABASE_NAME'], port = 3306
    )
database_cursor = database_connection.cursor()

"""
Get info of 1 item 
"""
def get_product_info(cur, item_id):
    cur.execute(f"select * from {database_config['TABLE_NAME']} where product_id={item_id};")
    item = next(cur)
    return Product(product_id = item[0], product_name = item[1], categories = item[2], image_url = item[3])

if __name__ == "__main__":
    # product_id, product_name, categories, image_url = get_product_info(database_cursor, 23821143235)
    # print(product_id, product_name, categories, image_url )
    print("Done")


# cnx.close()