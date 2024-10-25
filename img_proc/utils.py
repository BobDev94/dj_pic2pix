from PIL import Image, ImageEnhance
import numpy as np
import time

def convert(img, palette=None, img_name=''):
    '''
    Main conversion function

    img: A PIL Image object from the uploaded file
    palette: An optional color palette to be applied to the image

    returns: A filtered image
    '''

    w, h = img.size

    # TURN IMAGE INTO A SQUARE BY CROPPING OUT SIDES
    if w > h:
        bdr = (w - h) // 2
        img = img.crop((bdr, 0, w - bdr, h))
        w = h

    # REDUCE RESOLUTION
    while w > 1000 or h > 1000:
        w, h = w // 2, h // 2
        img = img.resize((w, h))

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    np_img = np.array(img)

    TOLERANCE = 40
    SAMPLER = 25
    COLOR = 1.1
    SHARP = 2

    # SAMPLE 4 CORNERS OF THE IMAGE
    sample = [
        np.array(img.crop((0, 0, SAMPLER, SAMPLER))),
        np.array(img.crop((w - SAMPLER, 0, w, SAMPLER))),
        np.array(img.crop((0, h - SAMPLER, SAMPLER, h))),
        np.array(img.crop((w - SAMPLER, h - SAMPLER, w, h)))
    ]
    comp = [np.mean(i, axis=(0, 1)) for i in sample]
    low = [np.maximum(i - TOLERANCE, 0) for i in comp]
    high = [np.minimum(i + TOLERANCE, 255) for i in comp]

    for row in np_img:
        for pixel in row:
            for i in range(4):
                if (low[i][0] <= pixel[0] <= high[i][0]) and (low[i][1] <= pixel[1] <= high[i][1]) and (low[i][2] <= pixel[2] <= high[i][2]):
                    pixel[3] = 0  # Turn pixel transparent
                    break
                else:
                    pixel[3] = 255

    trp_img = Image.fromarray(np_img)

    if 'pencil' in img_name:
        trp_img.show()
        return trp_img

    # TIME TO PIXELLATE
    rdc_img = trp_img.resize((128, 128), Image.BILINEAR)
    rsz_img = rdc_img.resize(trp_img.size, Image.NEAREST)
    rsz_img = np.array(rsz_img)

    for row in rsz_img:
        for pixel in row:
            if pixel[3] < 255:
                pixel[0], pixel[1], pixel[2] = 0, 0, 0

    cor_img = Image.fromarray(rsz_img)

    col_plus = ImageEnhance.Color(cor_img)
    col_fin = col_plus.enhance(COLOR)

    shp_plus = ImageEnhance.Sharpness(col_fin)
    fin = shp_plus.enhance(SHARP)

    if palette:
        apply_palette(fin, palette)

    return fin 

def apply_palette(img, palette):
    '''
    This function applies a color palette, if one is provided. A default palette, fantasy24 is embedded in the code.
    img: A filtered image produced by the convert function
    palette: An optional color palette to be applied to the image

    returns: The image output from convert function with an applied color palette
    '''
    
    np_img_array = np.array(img)
    np_copy_array = np.array(img)
    np_palette = np.array(palette)

    alpha_mask = np_img_array[:, :, 3] != 0 

    img_rgb = np_img_array[:, :, :3]

    img_rgb_opaque = img_rgb[alpha_mask]

    # Compute all pairwise distances between image RGB values and palette RGB values
    img_rgb_opaque_modded = img_rgb_opaque[:, np.newaxis, :]

    palette_expanded = np_palette[np.newaxis, :, :]

    distances = np.sqrt(np.sum((img_rgb_opaque_modded - palette_expanded) ** 2, axis=-1))  

    min_indices = np.argmin(distances, axis=-1)  
    # Map the closest palette colors to the image
    np_copy_array[alpha_mask, :3] = np_palette[min_indices] 
    # Convert back to an image
    recolored_img = Image.fromarray(np_copy_array)
    recolored_img.show()



def main():

    palette = [
    [31, 36, 10],
    [57, 87, 28],
    [165, 140, 39],
    [239, 172, 40],
    [239, 216, 161],
    [171, 92, 28],
    [24, 63, 57],
    [239, 105, 47],
    [239, 183, 117],
    [165, 98, 67],
    [119, 52, 33],
    [114, 65, 19],
    [42, 29, 13],
    [57, 42, 28],
    [104, 76, 60],
    [146, 126, 106],
    [39, 100, 104],
    [239, 58, 12],
    [60, 159, 156],
    [155, 26, 10],
    [54, 23, 12],
    [85, 15, 10],
    [48, 15, 10]
]
    source = input('Enter source image path: ')

    start = time.time()
    img_name = ''
    convert(source,palette, img_name)
    end = time.time()
    print(f'Time taken to pixellate: {end - start}')

    pass



if __name__ == "__main__":
    main()
    print('Cleared!')