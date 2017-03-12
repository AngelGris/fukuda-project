# Fukuda Project
## Mosaic images generator

Fukuda Project takes an image as input and recreates it using other small images as mosaics.

### Example
**Input**

![Input image](https://raw.githubusercontent.com/AngelGris/fukuda-project/master/images/examples/20160906_original.jpg)

**Output**

![Output image](https://raw.githubusercontent.com/AngelGris/fukuda-project/master/images/examples/20160906_output.jpg)

### Database
The script uses a one table MySQL database to store the mosaics information. The table structure is in *bd/fukuda.sql*.

Before creating a mosaic image you need to create the mosaics to use. To do so copy the images you want to use to create the small mosacis in *images/process* and run

    python generator.py

This process will create the small mosaics and store the information in the MySQL database. Depending on the number and size of the images this process may take a while.

The created mosaics will be 150px squares and stored in *images/finals*. Just copying images into this folder won't work since they need to processed and the infomation saved in the MySQL database. The size of the mosaics can be changed by editing the value of *final_size* variable:

    final_size = 150

### Creating mosaic image
Once you have a big enough database of mosaics images you can create your mosaic image by running

    python fukuda.py

By default it takes *test.jpg* image as input, but that can be changed in the line 41 of the code:

    img = cv2.imread('test.jpg', 1)

Also the *scale* variable can be changed to modify the size of the output image:

    scale = (30, 100)

In this case a 30px x 30px portion of the original image will be represented by 100px x 100px square in the final image. Making the output image more than 3 times bigger that the original. Input images with great details will require higher values in the output image, and images with low detail level can use smaller values.

The output image will be saved in *images/output*. The example image was generated using a database with more than 7k mosaics (not all of them were used in this particular image). The full size 14,400px x 10,800px image can be found in *images/output*.