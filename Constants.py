from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from math import sqrt

SOURCE_IMAGE = real_image = Image.open('camp2.png')
SOURCE_IMAGE = SOURCE_IMAGE.convert('RGB')

PIN_COLORS = [

    (255, 255, 255),  # 0 White (no pins)

    # Rainbow colored

#    (28, 128, 24),    # 1  Light green
#    (18, 128, 62),      # 2  Dark green
#    (133, 211, 214),   # 3  Light blue
#    (26, 41, 153),     # 4  Dark blue
#    (194, 47, 49),   # 5  Red
#    (227, 154, 7),  # 6  Orange
#    (227, 215, 50),    # 7  Yellow
#    (255, 133, 133),    # 8  Pink
#    #(147, 42, 150),   # 9  Purple
#    (224, 224, 224),  # 9 White
#    (26, 26, 26),  # 10 Black

    # Metallic colored
    (111, 70, 26),    # Brown   1
    (247, 208, 128),   # Gold   2
    (104, 104, 104),    # Dark silver   3
    (180, 180, 180),    # Light silver   4
    (194, 133, 110),    # Copper   5
    (199, 172, 94),     # Gold   6

]
