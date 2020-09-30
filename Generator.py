from Constants import *


# size of blocks to round, controls the detail of the final image
# lower block size = higher quality = more pins
block_size = 9
font_size = 8

source_width, source_height = SOURCE_IMAGE.size
demo_image = Image.new('RGB', (source_width, source_height))
demo_pixels = demo_image.load()
number_image = Image.new('RGB', (source_width, source_height), color=(255, 255, 255))
number_draw = ImageDraw.Draw(number_image)
number_font = ImageFont.truetype('/Windows/Fonts/Arial.ttf', font_size)


def average_rgb_area(x, y):
    # uses block_size for size
    total_r, total_g, total_b = (0, 0, 0)
    for area_y in range(y, y + block_size):
        for area_x in range(x, x + block_size):
            r, g, b = (SOURCE_IMAGE.getpixel((x, y)))
            total_r = total_r + r
            total_g = total_g + g
            total_b = total_b + b
    area = block_size * block_size
    final_rgb = (int(total_r / area), int(total_g / area), int(total_b / area))
    return final_rgb

def fill_area(x, y, color):
    # uses block_size for size
    """:parameter color: rgb tuple"""
    for area_y in range(y, y + block_size):
        for area_x in range(x, x + block_size):
            try:
                demo_pixels[area_x, area_y] = color
            except IndexError:
                pass


def closest_pin_color(rgb):
    # not mine, stolen from https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors?noredirect=1&lq=1
    r, g, b = rgb
    color_diffs = []
    for color in PIN_COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def closest_pin_color_weighted(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in PIN_COLORS:
        cr, cg, cb = color
        color_diff = sqrt(((r - cr)*0.30)**2 + ((g - cg)*0.59)**2 + ((b - cb)*0.11)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


total_pin_count = 0
all_colors = []
# get average rgb for every [block_size] pixels
for source_y in range(0, source_height, block_size):
    for source_x in range(0, source_width, block_size):
        block_rgb = average_rgb_area(source_x, source_y)
        block_pin_rgb = closest_pin_color(block_rgb)
        #print(block_rgb)
        #print(block_pin_rgb)
        fill_area(source_x, source_y, block_pin_rgb)
        demo_pixels[source_x, source_y] = block_rgb
        if block_pin_rgb != (255, 255, 255):
            total_pin_count = total_pin_count + 1
            all_colors.append(block_pin_rgb)
            number_draw.text((source_x + 20, source_y + 20),
                             str(PIN_COLORS.index(block_pin_rgb)),
                             font=number_font,
                             fill=(0, 0, 0))
    print('Loading: {}%'.format(int(source_y/source_height * 100)))
print('Total pin count: {}'.format(total_pin_count))
all_colors.sort()

for color in PIN_COLORS:
    print(all_colors.count(color), '   \t', color)

demo_image.save('Preview.png', 'PNG')
number_image.save('Number map.png', 'PNG')