import sys
import numpy as np
import cv2
import mysql.connector
import time
import datetime

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '*' * filledLength + '-' * (barLength - filledLength)
    s               = time.time() - start_time
    if iteration > 0:
        left_time       = (total * s / iteration) - s
    else:
        left_time = 0
    m, s            = divmod(s, 60)
    h, m            = divmod(m, 60)
    total_time      = '%d:%02d:%02d' % (h, m, s)
    m, s            = divmod(left_time, 60)
    h, m            = divmod(m, 60)
    left_time       = '%d:%02d:%02d' % (h, m, s)
    sys.stdout.write('\r%s (%s left) - %s |%s| %s%s %s (%d of %d)' % (total_time, left_time, prefix, bar, percents, '%', suffix, iteration, total)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

# MySQL connection
cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='fukuda')
cursor = cnx.cursor()

# MySQL queries
mysqlSelectImage = ("SELECT `id`, (ABS(CAST(red AS signed) - %s) + ABS(CAST(green AS signed) - %s) + ABS(CAST(blue as signed) - %s)) AS `distance` FROM `images` HAVING `distance` <= 90 ORDER BY `used`, `distance` LIMIT 1")

# Reset used counter in DB
cursor.execute("UPDATE `images` SET `used` = 0")
cnx.commit()

img = cv2.imread('test.jpg', 1)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

scale = (30, 100)
img_size = img.shape
output_cols = (int)(img.shape[1] / scale[0]);
output_rows = (int)(img.shape[0] / scale[0]);
output = np.zeros((output_rows * scale[1], output_cols * scale[1], 3), np.uint8)
total_iterations  = output_cols * output_rows
count_iterations = 0
max_distance = 0
start_time = time.time()

printProgress(count_iterations, total_iterations, 'Progress:', 'Complete', 2, 50)
for col in xrange(output_cols):
    for row in xrange(output_rows):
        count_iterations += 1
        color_b = []
        color_g = []
        color_r = []
        for x in xrange(scale[0]):
            for y in xrange(scale[0]):
                col_x = (scale[0] * col) + x
                row_y = (scale[0] * row) + y
                color_b.append(img.item(row_y, col_x, 0))
                color_g.append(img.item(row_y, col_x, 1))
                color_r.append(img.item(row_y, col_x, 2))

        avg_b = (int)(sum(color_b) / len(color_b))
        avg_g = (int)(sum(color_g) / len(color_g))
        avg_r = (int)(sum(color_r) / len(color_r))

        cursor.execute(mysqlSelectImage, (avg_r, avg_g, avg_b))
        for (img_id, distance) in cursor:
            tale = cv2.imread('images/finals/' + str(img_id)  + '.jpg', 1)
            tale = cv2.resize(tale, (scale[1],scale[1]))

            output[row * scale[1]:(row * scale[1]) + scale[1], col * scale[1]:(col * scale[1]) + scale[1]] = tale

            cursor.execute("UPDATE `images` SET `used` = `used` + 1 WHERE `id` = " + str(img_id))
            cnx.commit()

            if (distance > max_distance):
                max_distance = distance

        printProgress(count_iterations, total_iterations, 'Progress:', 'Complete', 2, 50)

cv2.imwrite('images/output/' + time.strftime('%Y%m%d%H%M%S') + '.jpg', output)
s = time.time() - start_time
m, s = divmod(s, 60)
h, m = divmod(m, 60)
total_time = '%d:%02d:%02d' % (h, m, s)
print 'Total time:', total_time , '- Max distance:', max_distance