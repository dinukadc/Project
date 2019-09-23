#! python
'''
This demo extracts all images of a PDF as PNG files, whether they are
referenced by pages or not.
It scans through all objects and selects /Type/XObject with /Subtype/Image.
So runtime is determined by number of objects and image volume.
Usage:
extract_img2.py input.pdf
'''

from __future__ import print_function

import fitz
import cv2
import os
import glob
from keras.models import load_model
import numpy as np
from keras.preprocessing import image


from tkinter import *
from tkinter import ttk


from tkinter import filedialog

from numpy.distutils.system_info import p


def ExImages():
    result = filedialog.askopenfilename(initialdir = "C:/Users/Administrator/PycharmProjects/fypchange1", title="Select file",filetypes=(("pdf file", "*.pdf"), ("all files", "*.*")))
    checkXO = r"/Type(?= */XObject)"  # finds "/Type/XObject"
    checkIM = r"/Subtype(?= */Image)"  # finds "/Subtype/Image"



    doc = fitz.open(result)

    imgcount = 0
    lenXREF = doc._getXrefLength()  # number of objects - do not use entry 0!

    # display some file info
    print("file: %s, pages: %s, objects: %s" % (result, len(doc), lenXREF - 1))



    for i in range(1, lenXREF):  # scan through all objects
            text = doc._getXrefString(i)  # string defining the object
            isXObject = re.search(checkXO, text)  # tests for XObject
            isImage = re.search(checkIM, text) # tests for Image
            if not isXObject or not isImage:  # not an image object if not both True
                continue
            imgcount += 1
            pix = fitz.Pixmap(doc, i)  # make pixmap from image
            if pix.n < 5: # can be saved as PNG
               pix.writePNG("../pdf/img-%s.png" % (i,))


            else:  # must convert the CMYK first
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG("../pdf/img-%s.png" % (i,))
                pix0 = None  # free Pixmap resources
                pix = None  # free Pixmap resources




    print("run time")
    print("extracted images", imgcount)


root = Tk()
root.title = "Browser"
btn = ttk.Button(root, text="Browse", command=ExImages)
btn.pack()
root.geometry("640x480")
root.mainloop()

### Training data model


classifier = load_model("../Graph/classifier.model")

img_dir = "../pdf"
data_path = os.path.join(img_dir,'*g')
files = glob.glob(data_path)
data = []
for f1 in files:

 path = p + '/'
 test_image = cv2.imread(f1)
 test_image = np.expand_dims(test_image, axis=0)
 result = classifier.predict(test_image)
 # training_set.class_indices

 if result[0][0] >= 0.5:
    prediction = 'Linear Graph'

 else:
    prediction = 'Curve Graph'

print(prediction)
