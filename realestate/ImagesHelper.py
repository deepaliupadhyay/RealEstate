from PIL import Image

import os



file1= os.path.join('./images/Condo/house1/1.jpg')  # type: Union[Union[str, unicode], Any]
file2= os.path.join('./images/Condo/house1/2.jpg')
file3= os.path.join('./images/Condo/house1/3.jpg')
file4= os.path.join('./images/Condo/house1/4.jpg')
file5= os.path.join('./images/Condo/house1/5.jpg')

def merge_images(file1, file2) :


    image1 = Image.open(file1)
    image2 = Image.open(file2)
    image3 = Image.open(file3)
    image4 = Image.open(file4)
    image5 = Image.open(file5)

    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    (width5, height5) = image5.size

    result_width = width1 + width2 + width3 + width4 + width5
    result_height = max(height1, height2, height3, height4, height5)

    print ("width {0} height {1}".format(width1, height1))
    print ("width {0} height {1}".format(width2, height2))
    print ("width {0} height {1}".format(width3, height3))
    print ("width {0} height {1}".format(width4, height4))
    print ("width {0} height {1}".format(width5, height5))


    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.paste(im=image3, box=(width1 + width2, 0))
    result.paste(im=image4, box=(width1 + width2 + width3, 0))
    result.paste(im=image5, box=(width1 + width2 + width3 + width4, 0))
    return result


if __name__ == "__main__":
    print (__name__)
    # file_dir = os.path.join(os.getcwd(), "")
    new_image = merge_images(file1, file2)
    new_image.save('./images/merge.jpg')
    image1 = new_image.crop(box=(0,0,1000,662))
    image2 = new_image.crop(box=(1000, 0, 1000*2, 662))
    image3 = new_image.crop(box=(1000*2, 0, 1000 * 3, 662))
    image4 = new_image.crop(box=(1000*3, 0, 1000 * 4, 662))
    image5 = new_image.crop(box=(1000*4, 0, 1000 * 5, 662))
    image1.save('./images/crop1.jpg')
    image2.save('./images/crop2.jpg')
    image3.save('./images/crop3.jpg')
    image4.save('./images/crop4.jpg')
    image5.save('./images/crop5.jpg')