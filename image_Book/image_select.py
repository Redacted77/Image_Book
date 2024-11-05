import os
from PySide6.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt

image_starting_path = r"image_set/0 Default.jpg"
current_image_path = image_starting_path
content = os.listdir('image_set/')

# makes sure that the system path exists 
def get_folder(folder):
    if os.path.exists(folder):
        return folder
    else:
        return False
    
# sets the new path for images
def set_paths(folder):
    global image_starting_path
    global content
    temp_content = []
    for file in os.listdir(folder):
        filename, extension = os.path.splitext(file)
        if extension in ['.png', '.jpg']:
            temp_content.append(file)
    if len(temp_content) <= 0:
        return False
    content = temp_content
    image_starting_path = folder + '/' + content[0]
    return image_starting_path

# turns an image into a pixmap (used alot)
def map(starting_path = image_starting_path):
    pil_image = Image.open(starting_path)
    qt_image = ImageQt(pil_image)
    pixmap = QPixmap.fromImage(qt_image)
    global current_image_path
    current_image_path = starting_path
    return pixmap

# Next and previous functionality
def current_file_path(forward = True):
    global image_starting_path
    global current_image_path
    global content
    list_images = content
    name_image = image_starting_path.split('/')
    current_name = current_image_path.split('/')
    for index, image in enumerate(list_images):
        if name_image[1] == image:
            try:
                if index-1 < 0 and forward == False:
                    raise IndexError
                current_name = list_images[index+1] if forward else list_images[index-1]
                current_image_path = name_image[0] + '/' + current_name
                image_starting_path = current_image_path
                return current_image_path  
            except IndexError:
                current_name = image
                current_image_path = name_image[0] + '/' + current_name
                return current_image_path
            
# saves a copy of the image with the new name, then deletes the original
def save_and_delete(new_name: str):
    global current_image_path
    image = Image.open(current_image_path)
    copy = image
    current_name = current_image_path.split('/')
    filename, extension = os.path.splitext(current_name[1])
    if current_name[1] == "0 Default.jpg":
        return False
    filename = new_name
    new_path = current_name[0] + '/' + os.path.join(filename + extension)
    copy.save(new_path)
    os.remove(current_image_path)
    current_image_path = new_path
    return current_image_path

# returns current image's name for the status bar
def whats_the_name():
    global current_image_path
    current_name = current_image_path.split('/')
    filename, extension = os.path.splitext(current_name[1])
    name = filename
    return name