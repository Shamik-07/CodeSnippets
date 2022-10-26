# Object Detection with YOLOV3-tiny

import os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
# from IPython.display import Image, display # enable this for jupyter lab
import io
import uvicorn
import numpy as np
# import nest_asyncio # enable this for jupyter lab
from enum import Enum
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

parent_dir = os.path.abspath(os.pardir)
images_dir = os.path.join(parent_dir, "images/object_detection/example_images")
# creating the necessary directories
dir_names = ["images_with_boxes", "images_uploaded"]
for each_dir in dir_names:
	if not os.path.exists(each_dir):
		os.mkdir(each_dir)


def detect_and_draw_box(filename, model="yolov3-tiny", confidence=0.5):
    """Detects common objects on an image and creates a new image with bounding boxes.

    Args:
        filename (str): Filename of the image.
        model (str): Either "yolov3" or "yolov3-tiny". Defaults to "yolov3-tiny".
        confidence (float, optional): Desired confidence level. Defaults to 0.5.
    """
    
    # Images are stored under the images/ directory
    img_filepath = f'{images_dir}/{filename}'
    
    # Read the image into a numpy array
    img = cv2.imread(img_filepath)
    
    # Perform the object detection
    bbox, label, conf = cv.detect_common_objects(img, confidence=confidence, model=model)
    
    # Print current image's filename
    print(f"========================\nImage processed: {filename}\n")
    
    # Print detected objects with confidence level
    for l, c in zip(label, conf):
        print(f"Detected object: {l} with confidence level of {c}\n")
    
    # Create a new image that includes the bounding boxes
    output_image = draw_bbox(img, bbox, label, conf)
    
    # Save the image in the directory images_with_boxes
    cv2.imwrite(f'images_with_boxes/{filename}', output_image)
    
    # # Display the image with bounding boxes
    # this can only be done through iPython
    # display(Image(f'images_with_boxes/{filename}'))

# Assign an instance of the FastAPI class to the variable "app".
app = FastAPI(title='Deploying a ML Model with FastAPI')

# List available models using Enum for convenience. This is useful when the options are pre-defined.
class Model(str, Enum):
    yolov3tiny = "yolov3-tiny"
    yolov3 = "yolov3"


# By using @app.get("/") you are allowing the GET method to work for the / endpoint.
@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. Now head over to http://localhost:8000/docs."

# By using @app.get("/info") you are allowing the GET method to work for the /info endpoint.
@app.get("/info")
def server_information():
    return "This server is for detecting common objects in images. Enjoy!"

# This endpoint handles all the logic necessary for the object detection to work.
# It requires the desired model and the image in which to perform object detection.
@app.post("/predict") 
def prediction(model: Model, file: UploadFile = File(...)):

    # 1. VALIDATE INPUT FILE
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    # 2. TRANSFORM RAW IMAGE INTO CV2 image
    
    # Read image as a stream of bytes
    image_stream = io.BytesIO(file.file.read())
    
    # Start the stream from the beginning (position zero)
    image_stream.seek(0)
    
    # Write the stream of bytes into a numpy array
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    
    # Decode the numpy array as an image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    
    # 3. RUN OBJECT DETECTION MODEL
    
    # Run object detection
    bbox, label, conf = cv.detect_common_objects(image, model=model)
    
    # Create image that includes bounding boxes and labels
    output_image = draw_bbox(image, bbox, label, conf)
    
    # Save it in a folder within the server
    cv2.imwrite(f'images_uploaded/{filename}', output_image)
    
    
    # 4. STREAM THE RESPONSE BACK TO THE CLIENT
    
    # Open the saved image for reading in binary mode
    file_image = open(f'images_uploaded/{filename}', mode="rb")
    
    # Return the image as a stream specifying media type
    return StreamingResponse(file_image, media_type="image/jpeg")

# for jupyter
# # Allows the server to be run in this interactive environment
# nest_asyncio.apply()
# # Spin up the server!    
# uvicorn.run(app, host=host, port=8000)


if __name__ == '__main__':
	image_files = [
	"apple.jpg", "car1.jpg", "car3.jpg", "clock2.jpg", "clock.jpg", "oranges.jpg",
	"apples.jpg", "car2.jpg", "car.jpg", "clock3.jpg", "fruits.jpg"]
	for image_file in image_files:
		detect_and_draw_box(image_file)

	host = "127.0.0.1"
	uvicorn.run("deploying_object_classification_model_w_FastAPI:app", host=host, port=8000,reload=True)


