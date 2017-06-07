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
        VoiceId='Gwyneth'
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
image_path2='/home/pi/dev/aws/img/image2.png'


collectionID="yashraspberrypi"
#setupCollection(collectionID)
#captureImage(image_path)
#addImagetoCollection(image_path,collectionID,"yash")
captureImage(image_path2)
detectFace(image_path2, collectionID)

#uploadImage(image_path)
#compareImages(image_path.replace("/","_"), image_path2.replace("/","_"))
