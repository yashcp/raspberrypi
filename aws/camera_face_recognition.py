import boto3
from picamera import PiCamera
from time import sleep
import webbrowser

bucket='kavyash-raspberry'

def setupCollection(collectionID):
    client=boto3.client('rekognition')
    client.create_collection(
        CollectionId=collectionID)
    

def addImagetoCollection(image_path, collectionID, imageID):
    image_file = open(image_path,"rb")
    client=boto3.client('rekognition')
    client.index_faces(
        CollectionId=collectionID,
        Image={
            'Bytes': image_file.read()
            },
        ExternalImageId=imageID
        )
    
        

def speakName(name):
    client=boto3.client("polly")
    response=client.synthesize_speech(
        OutputFormat='mp3',
        Text="Hello "+name+". How are you?",
        VoiceId='Joanna'
        )
    if "AudioStream" in response:
        with open('pollysample.mp3', 'wb') as f:
            f.write(response['AudioStream'].read())
        webbrowser.open("pollysample.mp3")
    
    
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

def detectFace(image_path, collectionID):
    image_file = open(image_path,"rb")
    client=boto3.client('rekognition')
    response = client.search_faces_by_image(
        CollectionId=collectionID,
        Image={
            'Bytes': image_file.read()
            },
        )
    print(response)
    for face in response["FaceMatches"]:
         print(face["Face"]["Confidence"])
         print(face["Face"]["ExternalImageId"])
         speakName(face["Face"]["ExternalImageId"])

 

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
collectionID="yashraspberrypi"
print ("Select a choice",end='\n')
print ("1. Add a user",end='\n')
print ("2. Recognize a user",end='\n')
choice = input()
if int(choice) == 1:
    print("You selected 1. Add a user",end='\n')
    print ("When the camera activates, make sure only the user's face is in the image",end='\n')
    username=input ('Enter user name (one word)')
    print ("Wait for camera....",end='\n')
    sleep(3)
    captureImage(image_path)    
    addImagetoCollection(image_path,collectionID,str(username)) 
elif int(choice) == 2:
    print("You selected 2. Recognize a user",end='\n')
    print ("When the camera activates, make sure only the user's face is in the image",end='\n')
    print ("Wait for camera....",end='\n')
    sleep(3)
    captureImage(image_path)    
    detectFace(image_path, collectionID)

#setupCollection(collectionID)
#uploadImage(image_path)
#compareImages(image_path.replace("/","_"), image_path2.replace("/","_"))
#image_path2='/home/pi/dev/aws/img/image2.png'
