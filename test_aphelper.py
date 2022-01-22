import aphelper.image as image

img = image.fits_image("moon_final.fit")
img.info()
img.save("Moon.jpg", brightness=0.8)