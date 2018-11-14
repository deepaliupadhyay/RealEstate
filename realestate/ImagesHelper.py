from PIL import Image

import os
import random


class ImageHelper:
    images_directory = ""

    def __init__(self):
        image_source_directory = os.getcwd()
        global images_directory
        images_directory = os.path.join(image_source_directory, "images")

    # Property ID will be provided as the parameter
    def get_images_list(self, property_id=123):
        # Fetch property category from DB

        property_category = "Condo"
        global images_directory
        image_directory_path = os.path.join(images_directory, property_category)
        folders = []
        for files in os.listdir(image_directory_path):
            if not files.startswith("."):
                folders.append(files)

        selected_property_directory = random.choice(folders)

        current_property_images = os.path.join(image_directory_path, selected_property_directory)
        print current_property_images

        list_of_images = []
        for images_name in os.listdir(current_property_images):
            if not images_name.startswith("."):
                list_of_images.append(images_name)
        print list_of_images
        return list_of_images, selected_property_directory

    def stitch_images(self, property_category="Condo"):
        global images_directory
        image_directory_path = os.path.join(images_directory, property_category)

        list_of_images, selected_property_directory = self.get_images_list()
        open_images = {}
        total_width = 0
        max_height = 0

        idx = 0
        for image in list_of_images:
            image_path = os.path.join(image_directory_path, selected_property_directory, image)
            open_image = Image.open(image_path)
            (width, height) = open_image.size
            open_images[(idx, width, height)] = open_image
            idx += 1
            total_width += width
            max_height = max(max_height, height)
        print("Total width {0} and height {1}".format(total_width, max_height))

        result = Image.new('RGB', (total_width, max_height))
        start_idx = 0
        for k, v in open_images.items():
            result.paste(im=v, box=(start_idx, 0))
            start_idx += k[1]
        return result, len(list_of_images)


if __name__ == "__main__":
    img_helper = ImageHelper()
    new_image, no_of_images = img_helper.stitch_images()
    new_image.save('./images/merge.jpg')
    print no_of_images