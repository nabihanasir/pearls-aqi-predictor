from utils.config import HOPSWORKS_API_KEY, HOPSWORKS_PROJECT, FEATURE_GROUP_NAME, FEATURE_GROUP_VERSION

try:
    import hopsworks
except Exception as e:
    hopsworks = None


def _login_project():
    if hopsworks is None:
        raise ImportError("hopsworks package not available. Install hopsworks to use Feature Store integrations.")
    return hopsworks.login(api_key_value=HOPSWORKS_API_KEY)


def get_feature_store():
    project = _login_project()
    return project.get_feature_store()


def get_model_registry():
    project = _login_project()
    return project.get_model_registry()


def get_feature_group_name():
    return FEATURE_GROUP_NAME, FEATURE_GROUP_VERSION
