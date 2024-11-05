Image Book
is a Gallery with minimal functionality has a Default image set, but the user can change it to a different folder form the menu bar, open folder.
it uses pyside6 for the GUI and PIL for image process.
it is separated into 3 files first is main.py, zoom_on_image.py and image_select.py.

-main.py
this is where the application is initialized and where you can run it.

-zoom_on_image.py
all the GUI elements are here: menu bar, status bar, next, previous buttons and the center image
-note worthy function

*update_image
it creates a new pixmap, that is scaled to the originals image size, while keeping the Aspect Ratio the same, the making the transition smooth.
it calls 'whats the name' function and tells the status bar to update it based on that.
it also prompts the application to change the displayed pixmap after using the 'current_file_path' function.

-image_select.py
all the important functions are here like:

*get folder
-makes sure the folder exists

*set paths
-checks the folder for images, and if there is any, it put them in a list, if there is none in it, it returns False (witch raises an error)
-then sets the image starting path to the first image in the folder

*map
-uses PIL to open the image then turns it into a Qpixmap so the application can use it.

*Current File Path
-The functionality for the "Next" and "Previous" buttons, has a Boolean argument 'forward', which defaults to True.
1- The function separates the starting image path and the current one using '/', extracting the image name from the path.
2- It then starts a for loop over the images in the image list (created earlier) while keeping track of the index.
3- The loop continues until it finds an image name in the list that matches the extracted image name from the image starting path.
4- The function tries to modify the index based on the 'forward' argument:
	*If forward is True, it adds one to the index to move to the next image.
	*If forward is False, it subtracts one to move to the previous image.
5- If changing the index would cause an IndexError (like moving beyond the start or end of the list), the index is left unchanged(the image stays the same). Additionally, if subtracting one results in a negative index, an IndexError is also raised.
6- Finally, the function reconstructs the path using the updated image name and returns it.

*save and delete
-used to rename the current image by saving a copy with the new name, then deleting the original.

*what's the name
returns the name of current image for the status bar.


 