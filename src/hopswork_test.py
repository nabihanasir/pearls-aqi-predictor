# import hopsworks
from utils.config import HOPSWORKS_API_KEY, HOPSWORKS_PROJECT

# project = hopsworks.login(
#     project=HOPSWORKS_PROJECT,
#     api_key_value=HOPSWORKS_API_KEY
# )

# fs = project.get_feature_store()

# print("Connected to Hopsworks Feature Store")

import hopsworks

project = hopsworks.login(
    api_key_value=HOPSWORKS_API_KEY  # uses HOPSWORKS_API_KEY from env
)

fs = project.get_feature_store()

print("Connected to Hopsworks project:", project.name)
print("Feature store name:", fs.name)
