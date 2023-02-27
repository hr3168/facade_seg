from PIL import Image, ImageColor, ImageDraw
from PIL import UnidentifiedImageError
import requests
import json
import argparse
import pathlib
import os.path


def manual_classes():
    """
    Change your preferenced color-coding below. 
    If you want to use manual coloring, you also need to change the Label-Classes (Title)
    """
    manual_dict = {
        'Tree': 255,
        'Flower': 85,

    }
    return manual_dict


def open_img(url):
    try:
        return Image.open(requests.get(url, stream=True).raw)
    except UnidentifiedImageError:
        return None


def open_json(path):
    with open(path) as file:
        return json.load(file)


def color_extractor(data, color_coding):
    """takes the given dictionary part and extracts all needed information. returns also colors for 3 different types"""

    if color_coding == 'auto':
        color = ImageColor.getcolor(data['color'], 'RGBA')
    elif color_coding == 'manual':
        color = (manual_classes()[data['title']],manual_classes()[data['title']],manual_classes()[data['title']],255)
    elif color_coding == 'binar':
        color = (255,255,255,255)
    else:
        print('no valid color-code detected - continue with binarized Labels.')
        color = (255,255,255,255)
    return color


def img_color(img, color):
    """change color of label accordingly"""
    if color == (255,255,255,255):
        return img
    img = img.convert('RGBA')
    width, height = img.size
    for x in range(width):
        for y in range(height):
            if img.getpixel((x,y)) == (255,255,255,255):
                img.putpixel((x,y), color)
    return img


def img_draw_polygon(size, polygon, color):
    """draw polygons on image"""
    img = Image.new('RGBA', size, (0,0,0,0))
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    # read points
    points = []
    for i in range(len(polygon)):
        points.append((int(polygon[i]['x']),int(polygon[i]['y'])))
    draw.polygon(points, fill = (color))
    return img


def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')


def main(input_dir, output_dir, color_type='auto'):

    if os.path.exists(input_dir) and os.path.exists(output_dir) and color_type in ['auto', 'manual', 'binar']:
        input_path = pathlib.Path(input_dir)
        label_paths_sorted = sorted(list(input_path.glob("*.json")))

        for image_path in label_paths_sorted:
            print('converting: {}'.format(os.path.basename(image_path)))
            # open json file
            data = open_json(image_path)

            # create image list for Labels
            img_list = []

            # read original image
            original_img = open_img(data[0]['Labeled Data'])
            try:
                width, height = original_img.size
            except Exception:
                print('Original image data not callable. Please provide image width and height.')

            for i in range(len(data[0]['Label']['objects'])):
                # read path and open image
                img = open_img(data[0]['Label']['objects'][i]['instanceURI'])

                # if path is not readable try to read polygon-data-points
                if not img is None:
                    img = img_color(img, color_extractor(data[0]['Label']['objects'][i], color_type))
                    img_list.append(img)
                else:
                    try:
                        # img = img_draw_polygon(img, data[0]['Label']['objects'][i]['polygon'], data[0]['Label']['objects'][i]['title'])
                        img = img_draw_polygon((width,height), data[0]['Label']['objects'][i]['polygon'], color_extractor(data[0]['Label']['objects'][i], color_type))

                        img_list.append(img)
                    except Exception:
                        print('Note: There are no available polygon-data-points & web-data-information for Label #{}.'.format(i))

                # print current progress status
                progressBar(i, len(data[0]['Label']['objects']))


            img = img_list[0]
            for i in range(1, len(img_list)):
                img.paste(img_list[i], (0,0), mask= img_list[i])
            img.save(output_dir + os.path.basename(image_path).replace('.json', '.png'))
    else:
        print('One of your given inputs is incorrect - please try again.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="convert annotations from labelbox2png")
    parser.add_argument("--input", help="input-directory")
    parser.add_argument("--output", help="output-directory")
    parser.add_argument("--color", help="binar, auto or manual")
    args = parser.parse_args()
    main(args.input, args.output, args.color)