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

async def get_esp_connection(id, pswd=None, enc_key=None):
    cli = aioesphomeapi.APIClient("nasa%02d.local"%id, 6053, password=pswd, noise_psk=enc_key)
    await cli.connect(login=True)
    entities = await cli.list_entities_services()
    
    return cli, entities

async def disconnect(cli, entitites):
    await cli.disconnect()

async def esp32_lighton(cli, entities):
    light_on = await cli.light_command(key=entities[0][0].key, state=True)

async def esp32_lightoff(cli, entities):
    light_off = await cli.light_command(key=entities[0][0].key, state=False)

async def esp32_get_image(cli, entities):
    image = await cli.request_single_image()
    return image

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
        connections = [asyncio.create_task(get_esp_connection(int(key), pswd= value['api']['password'], 
                                                              enc_key= value['api']['encryption']['key'])) for key, value in outdict.items()]
        conns = await asyncio.gather(*connections)
        lighton = await asyncio.gather(*(esp32_lighton(cli, ents) for cli,ents in conns))
        imgs = await asyncio.gather(*(esp32_get_image(cli, ents) for cli,ents in conns))
        lightoff = await asyncio.gather(*(esp32_lightoff(cli, ents) for cli,ents in conns))
        disconn = await asyncio.gather(*(disconnect(cli, ents) for cli,ents in conns))

        return imgs

async def wait(a,b):
    print('waiting... ')
    await asyncio.sleep(2)
    print('done.')
    return a+b,b

async def loop():
    for i in range(0,5):
        await wait()

async def parallel_loop():
    res = await asyncio.gather(*(wait(n*1, n*2) for n in [0,1,2,3,4]))
    return res
#outdict = parse_config_files()
#asyncio.run(download_imgs(outdict=outdict))
ret = asyncio.run(parallel_loop())
print(type(ret),ret)