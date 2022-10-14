import asyncio
from utils import download_all_imgs
from utils import parse_config_files

### Get one image
outdict = parse_config_files()
print(outdict.keys())
#asyncio.run(download_all_imgs(outdict=outdict))
