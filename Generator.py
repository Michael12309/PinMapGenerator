
from Constants import *

image_location = "image.png"
# size of blocks to round, controls the detail of the final image
# lower block size = higher quality = more pins
block_size = 14
font_size = 9

weighted_algo = True

if len(sys.argv) <= 4 and len(sys.argv) != 1:
    # filename is required
    if not os.path.isfile(sys.argv[1]):
        print("Cannot find file: " + sys.argv[1])
        exit()
    image_location = sys.argv[1]

    # block size is optional
    if len(sys.argv) >= 3:
        print(sys.argv[2])
        block_size = int(sys.argv[2])

    # algorithm type is optional
    if len(sys.argv) == 4:
        if sys.argv[3] == '1':
            weighted_algo = False


else:
    print('Usage: ', end='')
    print('python Generator.py image [block size] [use unweighted algorithm?]')
    exit()

SOURCE_IMAGE = Image.open(image_location)
SOURCE_IMAGE = SOURCE_IMAGE.convert('RGB')


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
        color_diff = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def closest_pin_color_weighted(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in PIN_COLORS:
        cr, cg, cb = color
        color_diff = math.sqrt(((r - cr)*0.30)**2 + ((g - cg)*0.59)**2 + ((b - cb)*0.11)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]



total_pin_count = 0
all_colors = []
# get average rgb for every [block_size] pixels
for source_y in range(0, source_height, block_size):
    for source_x in range(0, source_width, block_size):
        block_rgb = average_rgb_area(source_x, source_y)
        if weighted_algo:
            block_pin_rgb = closest_pin_color_weighted(block_rgb)
        else:
            block_pin_rgb = closest_pin_color(block_rgb)
        fill_area(source_x, source_y, block_pin_rgb)
        demo_pixels[source_x, source_y] = block_rgb
        if block_pin_rgb != (255, 255, 255):
            total_pin_count = total_pin_count + 1
            all_colors.append(block_pin_rgb)
            number_draw.text((source_x + 20, source_y + 20),
                             str(PIN_COLORS.index(block_pin_rgb)),
                             font=number_font,
                             fill=(0, 0, 0))
    percent_num = int(source_y/source_height * PROGRESS_WIDTH)
    percent_text = ' Loading: {:<10}'.format(str(int(source_y/source_height * 100)) + " %")

    # draw the loading bar
    sys.stdout.write("[ " +
                     "#"*percent_num +
                     "-"*int(PROGRESS_WIDTH-percent_num) +
                     " ]")
    # write the percentage after loading bar
    sys.stdout.write(percent_text)

    # move cursor back required amout for the progress bar
    sys.stdout.write("\b" * (PROGRESS_WIDTH + 4)) # +4 because of chars: "[ " + " ]"
    # move cursor back required amount for percent text
    sys.stdout.write("\b"*len(percent_text))

    # send text to screen immediately
    sys.stdout.flush()

# print out 100% loading bar (sometimes it will end at ~99 or 98%)
percent_num = PROGRESS_WIDTH
percent_text = ' Loading: {:<10}'.format("100 %")
sys.stdout.write("[ " +
                 "#"*percent_num +
                 "-"*int(PROGRESS_WIDTH-percent_num) +
                 " ]")
sys.stdout.write(percent_text)
sys.stdout.write("\b" * (PROGRESS_WIDTH + 4))
sys.stdout.write("\b"*len(percent_text))
sys.stdout.flush()

print('\n\nTotal pin count: {}\n'.format(total_pin_count))
all_colors.sort()

# TODO: write the names of each color next to the rgb (maybe use webcolors library)?
print('{:<10}{:<20}'.format("# Pins", "Color (rgb)"))

for color in PIN_COLORS:
    print('{:<10}{:<20}'.format(all_colors.count(color), ', '.join([str(num) for num in color])))

demo_image.save('Preview.png', 'PNG')
number_image.save('Number map.png', 'PNG')

print("\nExample image saved as \"Preview.png\"")
print("Number map saved as \"Number map.png\"")