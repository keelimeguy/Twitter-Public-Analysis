import yaml

try:
    with open('config/config.yml') as config_file:
        config_yaml = yaml.load(config_file, Loader=yaml.FullLoader)
        API_KEY = config_yaml['API_key']
        API_SECRET_KEY = config_yaml['API_secret_key']
        ACCESS_TOKEN = config_yaml['Access_token']
        ACCESS_TOKEN_SECRET = config_yaml['Access_token_secret']

        assert API_KEY
        assert API_SECRET_KEY
        assert ACCESS_TOKEN
        assert ACCESS_TOKEN_SECRET

except AssertionError:
    raise ValueError('Configuration file has not been set')

if __name__ == '__main__':
    print(config_yaml)
