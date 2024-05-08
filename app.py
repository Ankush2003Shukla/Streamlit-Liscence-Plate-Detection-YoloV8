import streamlit as st
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO
import easyocr
import pandas as pd
from twilio.rest import Client
import openpyxl
import tempfile
from annotated_text import annotated_text
# App title
st.set_page_config(page_title="LCR APP")
def get_car(license_plate, detection):
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(detection)):
        xcar1, ycar1, xcar2, ycar2, car_id = detection[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return detection[car_indx]

    return -1, -1, -1, -1, -1

def number_checking9(text): #1-i , 5-s ,0-o
    text = text.upper()
    x = ""
    for i in range(0,len(text)):
      if (i==2 or i==5 or i==6 or i==7 or i==8):
        if text[i]=='S':
          x=x+'5'
        elif(text[i]=='I'):
          x=x+'1'
        elif(text[i]=='Z'):
          x=x+'2'
        elif(text[i]=='O' or text[i]=='Q'):
          x=x+'0'
        elif(text[i]=='J'):
          x=x+'3'
        else:
          x=x+text[i]
      else:
        if text[i]=='5':
          x=x+'S'
        elif text[i]=='1':
          x=x+'I'
        elif text[i]=='2':
          x=x+'Z'
        elif text[i]=='0':
          x=x+'O'
        else:
          x=x+text[i]


    return x
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    return None
# Function to read license plate and detect violations
def detect_violations(cap_user):

    annotated_text(("Processing video...",""))
    coco_model = YOLO('yolov8n.pt')
    license_plate_detector = YOLO('Liscence.pt')
    data = pd.read_excel('Car_Details.xlsx')
    reader = easyocr.Reader(['en'])
    vehicles = [2, 3, 5, 7]
    # read frames
    frame_nmr = -1
    ret = True
    results = []
    while ret:
        frame_nmr += 1
        ret, frame = cap_user.read()
        if ret:
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

        # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

            # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, detections_)

                if car_id != -1:

                # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

                    resault = reader.readtext(license_plate_crop_gray)
                    text = ""
                    for res in resault:
                        if len(resault) == 1 or (len(res[1]) > 6 and res[2] > 0.2):
                            text = res[1]
                    Mtext = str(text)
                    if len(Mtext)==9:
                        Ankush = number_checking9(Mtext)
                        results.append(Ankush)

    print(results)
    a,b = data.shape
    print(a)
    details = list(set(results))
    print(details)
    success = False
    account_sid = 'AC35f32a82092a6cce9e93dbe254a2216d'
    auth_token = '7a671e826cdfe24482b2dc6d33ef3583'
    for i in range(0,len(details)):
        for j in range(0,a):
            if(data['Plate_Number'][j]==details[i]):
                if(data['Insurance'][j]=='NO'):
                    if(data['Pending_Chalan'][j]>2):

                        to_number = data['Phone_Number'][j]
                        client = Client(account_sid, auth_token)
                        name = data['Owner_Name'][j]
                        message = client.messages.create(
                        from_='+12513063133',
                        to = f"+91{to_number}",
                        body = f"Dear {name}, \nTraffic Alert: Failure to carry car insurance is a serious violation of traffic laws. Protect yourself and others on the road by obtaining proper coverage immediately. Ignoring this requirement can lead to hefty fines, license suspension, and legal consequences and More than 2 penalties is pending. Your violation penalty has been issued. Don't put yourself at risk – get insured now."
                        )
                        print(message.sid)
                        p = data['Plate_Number'][j]
                        annotated_text(("Traffic Violation Detected : NO INSURANCE & MORE THAN 2 CHALLAN PENDING : CAR NUMBER : ",p))
                        success = True
                    else:

                        to_number = data['Phone_Number'][j]
                        name = data['Owner_Name'][j]
                        client = Client(account_sid, auth_token)

                        message = client.messages.create(
                        from_='+12513063133',
                        to= f"+91{to_number}",
                        body = f"Dear {name}, \nTraffic Alert: Failure to carry car insurance is a serious violation of traffic laws. Protect yourself and others on the road by obtaining proper coverage immediately. Ignoring this requirement can lead to hefty fines, license suspension, and legal consequences. Your violation penalty has been issued. Don't put yourself at risk – get insured now."
                                    )
                        print(message.sid)
                        p = data['Plate_Number'][j]
                        annotated_text(("Traffic Violation Detected : NO INSURANCE : CAR NUMBER : ",p))
                        success = True
    # Display success message
    if success:
      annotated_text(("Violation Detected",""))
    else:
      annotated_text((" NO Violation Detected",""))

# Streamlit app
def main():
    st.title("License Plate Detection and Violation Alert")
    annotated_text(("Developed By","Ankush Shukla"))
    # File uploader for video
    st.sidebar.header("Upload Video")
    video_file = st.sidebar.file_uploader("Upload Video File", type=["mp4", "avi", "mov"])
    temp_file_path_user = save_uploaded_file(video_file)
    cap_user = cv2.VideoCapture(temp_file_path_user)
    video_file2 = open('Vedio1234.mp4', 'rb')
    video_bytes2 = video_file2.read()
    annotated_text(("Processing can take a few minutes so please wait......"," Click the vedio below to enjoy the song"))
    st.video(video_bytes2,loop=True)
    if video_file is not None:
        # Display uploaded video
        video_bytes = video_file.read()
        st.sidebar.video(video_bytes)
        
        # Button to start detection
        if st.sidebar.button("Start Detection"):
            detect_violations(cap_user)
            
if __name__ == "__main__":
    main()
