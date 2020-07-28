import yaml

with open('../config/config.yml') as config_file:
    config_yaml = yaml.load(config_file, Loader=yaml.FullLoader)
    API_KEY = config_yaml['API_key']
    API_SECRET_KEY = config_yaml['API_secret_key']
    ACCESS_TOKEN = config_yaml['Access_token']
    ACCESS_TOKEN_SECRET = config_yaml['Access_token_secret']

if __name__ == '__main__':
    print(config_yaml)
