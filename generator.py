import numpy as np
import cv2
import os
import mysql.connector

def toHex(dec):
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    rest = dec / 16
    if (rest == 0):
        return digits[x]
    return toHex(rest) + digits[x]

# MySQL connection
cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='fukuda')
cursor = cnx.cursor()

# MySQL queries
mysqlInsert = ("INSERT INTO `images` (`hexa`, `red`, `green`, `blue`, `priority`) VALUES (%s, %s, %s, %s, %s)")

img_originals = 'images/process'
img_finals = 'images/finals'
final_size = 150
images = os.listdir(img_originals)
count = 0

for image_file in images:
    count += 1
    print count, '-', image_file
    image = cv2.imread(img_originals + '/' + image_file, 1)
    image_size = image.shape
    original_size = min(image_size[0], image_size[1])

    for priority in range(1,4):
        if priority == 1:
            # Centered image (Priority 1)
            from_y = int((image_size[0] - original_size) / 2)
            from_x = int((image_size[1] - original_size) / 2)
        elif priority == 2:
            # Top left image (Priority 2)
            from_y = 0
            from_x = 0
        else:
            # Bottom right image (Priority 3)
            from_y = image_size[0] - original_size
            from_x = image_size[1] - original_size

        crop_img = image[from_y:from_y + original_size, from_x:from_x + original_size]
        thumbnail = cv2.resize(crop_img, (final_size,final_size))

        color_b = []
        color_g = []
        color_r = []
        for col_x in xrange(final_size):
            for row_y in xrange(final_size):
                color_b.append(thumbnail.item(row_y, col_x, 0))
                color_g.append(thumbnail.item(row_y, col_x, 1))
                color_r.append(thumbnail.item(row_y, col_x, 2))

        avg_b = sum(color_b) / len(color_b)
        avg_g = sum(color_g) / len(color_g)
        avg_r = sum(color_r) / len(color_r)

        hex_r = toHex(avg_r)
        if len(hex_r) < 2:
            hex_r = '0' + hex_r
        hex_g = toHex(avg_g)
        if len(hex_g) < 2:
            hex_g = '0' + hex_g
        hex_b = toHex(avg_b)
        if len(hex_b) < 2:
            hex_b = '0' + hex_b

        data = (hex_r + hex_g + hex_b, avg_r, avg_g, avg_b, priority)
        cursor.execute(mysqlInsert, data)
        cnx.commit()

        cv2.imwrite(img_finals + '/' + str(cursor.lastrowid) + '_o.jpg', crop_img)
        cv2.imwrite(img_finals + '/' + str(cursor.lastrowid) + '.jpg', thumbnail)

    image = os.remove(img_originals + '/' + image_file)