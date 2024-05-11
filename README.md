# Streamlit-Liscence-Plate-Detection-YoloV8

This project aims to detect license plates in images or videos, check if the corresponding vehicles have valid insurance, and determine if they have pending traffic violations. It utilizes computer vision techniques for license plate detection and optical character recognition (OCR) to extract text from the detected plates. The system then cross-references this information with a database to identify any violations, such as lacking insurance coverage or having multiple pending challans.

## Features

- License plate detection using YOLO (You Only Look Once) object detection algorithm.
- Optical character recognition (OCR) using EasyOCR library to extract text from license plates.
- Checking insurance status and pending challans for vehicles based on license plate numbers.
- Sending SMS alerts using Twilio to notify vehicle owners of detected violations.

# Libraries Used

- **easyocr==1.7.1**
- **numpy==1.26.4**
- **opencv-python-headless**
- **openpyxl==3.1.2**
- **pandas==2.2.1**
- **Pillow==10.2.0**
- **st-annotated-text==4.0.1**
- **streamlit==1.33.0**
- **twilio==9.0.5**
- **ultralytics==8.1.42**

## Deployment

- The project is deployed on Streamlit Cloud and can be accessed using the following link:[
License Plate Detection and Violation Alert App](https://app-liscence-plate-detection-yolov8-eqtl8k3picneujgpsrbjxe.streamlit.app/)
- Use this link for Sample vedio for checking the app:[Sample Vedio](https://drive.google.com/file/d/1KymwidZCZNICjpI6ca7uNh7SuIQ_ncTC/view?usp=sharing)
## How to Use

To use the app locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Run the Streamlit app using the following command:
4. Access the app in your web browser at `http://localhost:8501`.
   
# Usage

Upload a video file containing vehicle footage.
Click on the "Start Detection" button to initiate the license plate detection and violation checking process.
The app will analyze each frame of the video, detect license plates, extract text, and check for violations.
If violations are detected (e.g., no insurance, pending challans), SMS alerts will be sent to the respective vehicle owners via Twilio.

## Contributors
- Ankush Kumar Shukla
- Feel free to contribute, report issues, or provide feedback to improve this project further!
