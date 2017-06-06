import boto3
from picamera import PiCamera
from time import sleep
from PIL import Image

bucket='kavyash-raspberry'

def captureImage(image_path):
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture(image_path,format='png')
    camera.stop_preview()

def uploadImage(image_path):
    key=image_path.replace("/","_")
    image_file = open(image_path,"rb")
    client=boto3.client('s3')
    client.put_object(
     Bucket=bucket,
     ContentType='image/png',
     Body=image_file.read(),
     Key=key
     )
    image_file.close()

def compareImages(source, target):
    client=boto3.client('rekognition')
    result = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': source
                }
            },
        TargetImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': target
                }
            }
        )
    print (result)
    #for face in result.FaceMatches
     #   print face.Similarity
        
            
            
        
    
image_path='/home/pi/dev/aws/img/image1.png'
image_path2='/home/pi/dev/aws/img/image2.png'

#captureImage(image_path2)
#uploadImage(image_path2)
compareImages(image_path.replace("/","_"), image_path2.replace("/","_"))
