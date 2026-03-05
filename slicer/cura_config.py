import configparser
import json


def update_config():
    cfgp = configparser.ConfigParser()

    cfgp.read('config/easys4.ini')
    with open('config/core.def.json', 'r') as jfh:
        slicer_config = json.load(jfh)

    curr_layer_height = slicer_config['settings']['global']['all']['layer_height']
    layer_height = cfgp['SLICER']['LayerHeight']
    if curr_layer_height != layer_height:
        slicer_config['settings']['global']['all']['layer_height'] = layer_height

    with open('config/core.def.json', 'w') as jfh:
        json.dump(slicer_config, jfh, indent=4)

def get_config():
    cfgp = configparser.ConfigParser()
    cfgp.read('config/easys4.ini')
    cura_path = cfgp['PATHS']['curaengine']
    return cura_path

def update_cura_config(src):
    with open(src, 'r') as jfh:
        slicer_config = json.load(jfh)

    cfgp = configparser.ConfigParser()
    cfgp.read('config/easys4.ini')

    for setting_name, data in slicer_config['settings']['global']['all'].items():
        if isinstance(data, dict):
            val = data.get('value') or data.get('default_value')
        else:
            val = data
        
        cfgp['SLICER'][str(setting_name)] = str(val)
    
    with open('config/easys4.ini', 'w') as cfgh:
        cfgp.write(cfgh)

def update_layer_height(layer_height):
    cfgp = configparser.ConfigParser()
    cfgp.read('config/easys4.ini')

    cfgp['SLICER']['layer_height'] = layer_height
    
    with open('config/easys4.ini', 'w') as cfgh:
        cfgp.write(cfgh)

def get_slicer_settings(command):
    cfgp = configparser.ConfigParser()
    cfgp.read('config/easys4.ini')
    for setting_name in cfgp['SLICER']:
        value = cfgp['SLICER'][setting_name]
        command.extend(["-s", f'{setting_name}={value}'])
    
    return command