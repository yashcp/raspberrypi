import io
import os
import sys

from google.cloud import vision
vision_client = vision.Client()
file_name=sys.argv[1]
print(file_name)
with io.open(file_name,'rb') as image_file:
     image = vision_client.image(content=image_file.read())

labels = image.detect_labels()
print('Labels:')
for label in labels:
    print(label.description)

faces=image.detect_faces()
for face in faces:
    print (face.emotions.joy)
    print (face.emotions.anger)
    print (face.emotions.sorrow)
    print (face.emotions.surprise)
    



