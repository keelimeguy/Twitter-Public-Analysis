import yaml


def _get_config(_config_file):
    _config_yaml = yaml.load(_config_file, Loader=yaml.FullLoader)
    _API_KEY = _config_yaml['API_key']
    _API_SECRET_KEY = _config_yaml['API_secret_key']
    _ACCESS_TOKEN = _config_yaml['Access_token']
    _ACCESS_TOKEN_SECRET = _config_yaml['Access_token_secret']

    return _API_KEY, _API_SECRET_KEY, _ACCESS_TOKEN, _ACCESS_TOKEN_SECRET


try:
    with open('config/config.yml') as config_file:
        API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = _get_config(config_file)
        assert API_KEY
        assert API_SECRET_KEY
        assert ACCESS_TOKEN
        assert ACCESS_TOKEN_SECRET

except FileNotFoundError:
    with open('../config/config.yml') as config_file:
        config_yaml = yaml.load(config_file, Loader=yaml.FullLoader)
        API_KEY = config_yaml['API_key']
        API_SECRET_KEY = config_yaml['API_secret_key']
        ACCESS_TOKEN = config_yaml['Access_token']
        ACCESS_TOKEN_SECRET = config_yaml['Access_token_secret']

except AssertionError:
    raise ValueError('Configuration file has not been set')

if __name__ == '__main__':
    print(config_yaml)
