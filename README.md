# ImageViewer
The GUI application will allow to view the images along with there ground truth so that the annotations can be modified easily.

A sample images and labels folder is provided in the repository. You can try on them first to see how the application works. 

**Clone the Repository**

Now clone the repository to your machine. Go to your terminal and the type:
```
git clone https://github.com/VipulRamtekkar/ImageViewer
```
```
cd ImageViewer
```

Paste the images file and labels file in the same folder.

Install the dependencies required for the application to run

```
sudo pip install -r requirements.txt
```

or install them separately

```
sudo pip install Cython
sudo pip install kivy
sudo pip install pygame
```

Instructions for Usage

1. Once the application loads check the image and its corresponding ground truth, if you find that the lanes are marked correctly then click Correct. <br>

**Correct lanes** <br>
-The ones that are visible on the screen and are marked in the ground truth <br>
-Dashed lanes should not be interpolated <br>

**Incorrect Lanes** <br>
-Interpolation done on the lanes <br>
-Lanes are marked in the groundtruth that are not visible <br>

2. Correcting the annotation; at times some regions will be marked as lanes which are not visible in the image, click on them and that annotation will vanish. 
```
If you incorrectly click on any lane that is present you can revert your action by clicking on the Undo
```

3. The images that are correct go in the final_images folder and same for the labels which go to the final_labels folder
the incorrect images and the corresponding labels are deleted. 

4. You can exit the application and it will continue from the last image that you left it with.

5. Once all the images are completed you will be automatically exited from the application.
