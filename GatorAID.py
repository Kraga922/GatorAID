import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import math
from PIL import Image



image = Image.open("GatorAid.png")
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image, width = 230)


# Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background-color: #1f2937;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
    }
    </style>
    <div class="navbar">GatorAID</div>
    """,
    unsafe_allow_html=True,
)

# Divide the layout into two columns
col1, col2 = st.columns([2, 1])

# Left Column: Exercise Sections
with col1:
    # Shoulder Section with Description
    with st.expander("Shoulder"):
        st.markdown("### Arm Swing")
        st.write("Gently swing your arms forward and backward, keeping them straight to warm up your shoulders.")

        st.markdown("### Lateral Raises")
        st.write("Raise your arms out to the sides until they are at shoulder level, then slowly lower them.")

        st.markdown("### Shoulder Press")
        st.write("Press weights or resistance upwards above your head and lower them back to shoulder height.")

    # Knee Section with Description
    with st.expander("Knee"):
        st.markdown("### Quad Stretch")
        st.write("Stand on one leg and pull your opposite ankle towards your glutes to stretch your quadriceps.")

        st.markdown("### Squats")
        st.write("Lower your body by bending your knees and hips. Then, return to standing position.")

        st.markdown("### Hamstring Curl")
        st.write("Stand and curl your leg backwards, bringing your heel toward your glutes to engage your hamstring.")

    # Arms Section with Description
    with st.expander("Arms"):
        st.markdown("### Bicep Curl")
        st.write("Hold weights and curl your arms upwards, bringing your palms towards your shoulders to work your biceps.")

# Right Column: Camera Placeholder
with col2:
    # Create a placeholder for the camera feed
    camera_feed = st.image([])

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1f2937;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
    Copyright © 2024. Kiran Nadanam, Ryan Nadanam, Krishiv Agarwal, Kevin Duong. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)

# BEGINNING OF THE BEST THING EVER

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    # makes it easier to calculate angles and make it numpy arrays

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    # Calculates the radians for a particular angle

    if angle > 180.0:
        angle = 360 - angle
    # convert angle between zero and 180

    return angle

def are_hands_together(landmarks):
    left_pinky = landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value]
    right_pinky = landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value]
    # Calculate the distance between the wrists
    distance = np.linalg.norm(np.array([left_pinky.x - right_pinky.x, left_pinky.y - right_pinky.y]))
    return distance < 0.13  # Adjust the threshold as necessary

# Start the video capture
cap = cv2.VideoCapture(0)
mode = "arm-swing-left"
start = False
counter = 0
stage = None  # represents whether or not you are at the down or up part of the curl

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Camera not detected. Please ensure the camera is connected.")
            break

        # Recolor the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make Detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks and visualize if pose is detected
        try:
            landmarks = results.pose_landmarks.landmark
            if not are_hands_together(landmarks) and start == False:
                cv2.putText(image, 'PUT HANDS TOGETHER TO START', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                            cv2.LINE_AA)
            else:
                start = True
                overlay = image.copy()

                # Draw the filled rectangle on the overlay
                cv2.rectangle(overlay, (0, 0), (305, 73), (245, 117, 16), -1)  # Color: (B, G, R)

                # Set the transparency level (0.0 - completely transparent, 1.0 - completely opaque)
                alpha = 0.5  # Adjust this value for desired transparency

                # Blend the overlay with the original image
                cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

                # Now draw the text on the blended image
                cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, 'STAGE', (105, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(stage), (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, str(mode), (15, 87), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                # Rep data
                cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(image, 'STAGE', (105, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(stage), (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, str(mode), (15, 87), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                # Render detection
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

            match (mode):
                case "bicep-curl-left":
                    # get coordinates
                    pointA = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                case "bicep-curl-right":
                    pointA = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                case "arm-swing-left":
                    pointA = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                case "arm-swing-right":
                    pointA = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                case "lat-raise-left":
                    pointA = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                case "lat-raise-right":
                    pointA = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                case "shoulder-press-left":
                    pointA = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                case "shoulder-press-right":
                    pointA = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                case "quad-stretch-right" | "squats" | "hamstring-curl-left":
                    pointA = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                case "quad-stretch-left" | "hamstring-curl-right":
                    pointA = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    pointB = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    pointC = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # calculate angle
            angle = calculate_angle(pointA, pointB, pointC)
            # visualize
            cv2.putText(image, str(math.floor(angle)),
                        tuple(np.multiply(pointB, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )
            if start:
                if mode == "bicep-curl-left" or mode == "bicep-curl-right":
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage == "down":
                        stage = "up"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        if mode == "bicep-curl-left":
                            mode = "bicep-curl-right"
                        else:
                            mode = "lat-raise-left"
                elif mode == "lat-raise-left" or mode == "lat-raise-right":
                    if angle < 20:
                        stage = "down"
                    if angle > 80 and stage == "down":
                        stage = "up"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        if mode == "lat-raise-left":
                            mode = "lat-raise-right"
                        else:
                            mode = "shoulder-press-left"
                elif mode == "shoulder-press-left" or mode == "shoulder-press-right":
                    if angle < 90:
                        stage = "down"
                    if angle > 140 and stage == "down":
                        stage = "up"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        if mode == "shoulder-press-left":
                            mode = "shoulder-press-right"
                        else:
                            mode = "arm-swing-left"
                elif mode == "arm-swing-left" or mode == "arm-swing-right":
                    if angle < 20:
                        stage = "down"
                    if angle > 160 and stage == "down":
                        stage = "up"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        if mode == "arm-swing-left":
                            mode = "arm-swing-right"
                        else:
                            mode = "quad-stretch-left"
                elif mode == "quad-stretch-left" or mode == "quad-stretch-right" or mode == "hamstring-curl-left" or mode == "hamstring-curl-right":
                    if angle > 110:
                        stage = "down"
                    if angle < 20 and stage == "down":
                        stage = "up"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        if mode == "quad-stretch-left":
                            mode = "quad-stretch-right"
                        elif mode == "quad-stretch-right":
                            mode = "hamstring-curl-left"
                        elif mode == "hamstring-curl-left":
                            mode = "hamstring-curl-right"
                        elif mode == "hamstring-curl-right":
                            mode = "squats"
                elif mode == "squats":
                    if angle > 120:
                        stage = "up"
                    if angle < 80 and stage == "down":
                        stage = "down"
                        counter += 1
                    if counter >= 10:
                        counter = 0
                        mode = "bicep-curl-left"
        except:
            pass

        # Convert the BGR image to RGB and display it on the website
        camera_feed.image(image, channels="BGR")

        # Check for quit signal
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
