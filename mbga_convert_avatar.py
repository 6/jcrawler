"""
Convert MBGA avatars from GIF -> PNG format so OpenCV can load them.
Requires ImageMagick to be installed (www.imagemagick.org)
"""
import os
import glob

def convert():
  gifs = glob.glob(os.path.join("data/mbga/avatar/", "*.gif"))
  for gif in gifs:
    png = gif.replace(".gif", ".png")
    # only save the first frame of the animated GIF
    os.system("convert {0}[0] {1}".format(gif, png))
    os.remove(gif)
  
if __name__=="__main__":
  convert()
