#!/usr/bin/env python3

# API libraries
import aioesphomeapi
import asyncio

# fileio imports
from pathlib import Path
from glob import glob
import yaml

# image processing imports
import numpy as np


CONFIGPATH = Path('/home/magnus/esp32home/config/')

def unknown(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        constructor = loader.__class__.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.__class__.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.__class__.construct_mapping

    data = constructor(loader, node)

    return data
yaml.add_multi_constructor('!secret', unknown)


async def esp32_lighton(id, pswd=None, enc_key=None):

    cli = aioesphomeapi.APIClient("nasa%02d.local"%id, 6053, password=pswd, noise_psk=enc_key)

    await cli.connect(login=True)
    entities = await cli.list_entities_services()
    light_on = await cli.light_command(key=entities[0][0].key, state=True)
    d = await cli.disconnect()

async def esp32_get_image(id, pswd=None, enc_key=None):

    cli = aioesphomeapi.APIClient("nasa%02d.local"%id, 6053, password=pswd, noise_psk=enc_key)

    await cli.connect(login=True)
    def cb(state):
        if type(state) == aioesphomeapi.CameraState:
            try:
                with open('out/x.jpg','wb') as out:
                    out.write(state.image)
                print("Image written")
            except Exception as e:
                print(e)

    await cli.subscribe_states(cb)

    l = await cli.list_entities_services()
    print(l)


async def esp32_lightoff(id, pswd=None, enc_key=None):

    cli = aioesphomeapi.APIClient("nasa%02d.local"%id, 6053, password=pswd, noise_psk=enc_key)

    await cli.connect(login=True)
    entities = await cli.list_entities_services()
    light_off = await cli.light_command(key=entities[0][0].key, state=False)
    d = await cli.disconnect()

def parse_config_files():
    outdict = {}
    paths = glob(str(CONFIGPATH / 'nasa*.yaml'))
    
    for path in paths:
        name = path.split('/')[-1].strip('.yaml')
        id = int(name[-2:])
        outdict[id] = {'name': name}
        with open(path, 'r') as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            outdict[id]['api'] = config['api']
        
    return outdict

async def download_imgs(outdict=None):
    if type(outdict) is dict:
        for key, value in outdict.items():
            i = int(key)
            await esp32_lighton(i, pswd= value['api']['password'], enc_key= value['api']['encryption']['key'])
        for key, value in outdict.items():
            i = int(key)
            await esp32_get_image(i, pswd= value['api']['password'], enc_key= value['api']['encryption']['key'])
        for key, value in outdict.items():
            i = int(key)
            await esp32_lightoff(i, pswd= value['api']['password'], enc_key= value['api']['encryption']['key'])

outdict = parse_config_files()
asyncio.run(download_imgs(outdict=outdict))