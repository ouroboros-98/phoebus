import json


class Config:
    
    @property
    def web_driver_path(self):
        return Config.cfg['web_driver_path']
    
    @property
    def main_url(self):
        return Config.cfg['huji_url']
    
    @property
    def relevant_faculties(self):
        return list(Config.cfg['relevant_faculties'].keys())
    
    @property
    def location_regex_list(self):
        return Config.cfg['location_regex']
    
    def x(self, *args):
        current = Config.cfg['xpaths']

        for arg in args:
            if arg not in current:
                return None
            current = current[arg]
            if type(current) == str:
                return current


    def __init__(self):
       with open('config.json', encoding='utf8') as f:
           Config.cfg = json.load(f)

CONFIG = Config()

if __name__ == '__module__':
    if CONFIG is None:
        CONFIG = Config()
