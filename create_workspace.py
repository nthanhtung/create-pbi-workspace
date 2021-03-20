import requests
import yaml

# read yml content
def read_yml_to_dict(config_yaml_filepath):
    with open(config_yaml_filepath, "r") as f:
        raw_config = f.read()
        config = yaml.safe_load(raw_config)
    return config


############
def get_access_token(credential):
    url = 'https://login.microsoftonline.com/common/oauth2/token'
    body = """grant_type=password
    &username={v1}
    &password={v2}
    &client_id={v3}
    &resource=https://analysis.windows.net/powerbi/api""".format(v1 = credential["username"], v2 = credential["password"], v3 = credential["client_id"])
    response = requests.post(url, body)
    access_token = response.json()["access_token"]
    return access_token

##########
def create_workspace(access_token, list_of_workspace_to_create):
    l = list_of_workspace_to_create["l"]
    for i in range(len(l)):
        url = 'https://api.powerbi.com/v1.0/myorg/groups'
        body = {
        "name": "{v1}".format(v1 = l[i])
        }
        headers = {"Authorization": "Bearer {v1}".format(v1 = access_token)}
        response = requests.post(url, headers = headers, data = body)
    return response.json()


####
credential = read_yml_to_dict("./credential.yml")
access_token = get_access_token(credential)
list_of_workspace_to_create = read_yml_to_dict("./list_of_workspace_to_create.yml")
result = create_workspace(access_token, list_of_workspace_to_create)
print(result)