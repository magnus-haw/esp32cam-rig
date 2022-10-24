from PIL import Image
from PIL import ExifTags

filename = '/Users/mhaw/esp32cam-rig/DSC02285.JPG'
im = Image.open(filename)
im.load()  # Needed only for .png EXIF data (see citation above)
#print(im.info)

exif = im.getexif()

# exif[271]='OMNIVISION'
# exif[272]='OV5640'
edict = {
    ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS
}
#im.save("/Users/mhaw/esp32cam-rig/nasa22_calib/test.png",exif=exif)
print([(k,v) for k, v in ExifTags.TAGS.items()])