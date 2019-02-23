import os
from PIL import Image


SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'
SCALE_BOTH = 'crop'

def crop(img, x, y):
    img_x, img_y = img.size
    img_ratio = img_x/float(img_y)
    crop_ratio = x/float(y)
    if crop_ratio == img_ratio:
        img.thumbnail([x,y], Image.ANTIALIAS)
        return img

    if crop_ratio < img_ratio:
        scale_factor = img_y/float(y)
        img.thumbnail([int(img_x/scale_factor)+1, y], Image.ANTIALIAS)
        img_x, img_y = img.size
        x_offset = (img_x-x)/2
        return img.crop([x_offset, 0, x_offset+x, y])

    if crop_ratio > img_ratio:
        scale_factor = img_x/float(x)
        img.thumbnail([x, int(img_y/scale_factor)+1], Image.ANTIALIAS)
        img_x, img_y = img.size
        y_offset = (img_y-y)/2
        return img.crop([0, y_offset, x, y_offset+y])

def scale(max_x, pair):
    x, y = pair
    new_y = (float(max_x) / x) * y
    return (int(max_x), int(new_y))

def thumbnail(file, size='200w'):
    # defining the size
    if (size.lower().endswith('h')):
        mode = 'h'
        size = size[:-1]
        max_size = int(size.strip())
    elif (size.lower().endswith('w')):
        mode = 'w'
        size = size[:-1]
        max_size = int(size.strip())
    else:
        mode = 'crop'
        
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image_x, image_y = image.size  
        
        if mode == SCALE_HEIGHT:
            image_y, image_x = scale(max_size, (image_y, image_x))
            image.thumbnail([image_x, image_y], Image.ANTIALIAS)
        elif mode == SCALE_WIDTH:
            image_x, image_y = scale(max_size, (image_x, image_y))
            image.thumbnail([image_x, image_y], Image.ANTIALIAS)
        elif mode == SCALE_BOTH:
            x, y = [ int(i) for i in size.split('x')]
            image = crop(image, x, y)
        else:
            raise Exception("Thumbnail size must be in ##w, ##h, or ##x## format.")
            
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url
