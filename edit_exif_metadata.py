from PIL import Image
from PIL import ExifTags

#filename = '/Users/mhaw/esp32cam-rig/DSC02285.JPG'
for id in range(0,24):
    filename = '/Users/mhaw/esp32cam-rig/nasa%02d_00.jpg'%id
    try:
        im = Image.open(filename)
        im.load()  # Needed only for .png EXIF data (see citation above)
        #print(im.info)

        exif = im.getexif()
        exif[256] = 1600
        exif[257] = 1200
        exif[271]='OMNIVISION' 
        exif[272]='OV5640'
        exif[50735]= "%i"%id#SN
        exif[42033]= "%i"%id#SN
        exif[37386]="3.4 mm"

        calfilename = '_nasa%02d_00.jpg'%id
        im.save("/Users/mhaw/esp32cam-rig/%s"%calfilename,exif=exif)
    except:
        print(filename,' error')
edict = {
    ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS
}
print([(k,v) for k, v in ExifTags.TAGS.items()])