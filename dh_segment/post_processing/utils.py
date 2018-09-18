import numpy as np

def img2uint8(img):
    # convert & scale an image for imageio output (uint8)
    img = 255 * img
    return img.astype(np.uint8)


def imgInfo(img, name='img'):

    if len(img.shape) > 2:
        nc = img.shape[2]
    else:
        nc = 1

    print(name + ":")
    print("  %d x %d channels: %d" %
          (img.shape[1], img.shape[0], nc))
    print("  [%d %d]" % (np.min(img), np.max(img)))

def normalize(img):

    min = np.min(img)
    max = np.max(img)

    imgN = (img-min)/(max-min)

    return imgN

