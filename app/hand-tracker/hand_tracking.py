import cv2
import mediapipe as mp
import numpy as np
import gestures
import time
import threading
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pythonosc.udp_client import SimpleUDPClient
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

latest_frame = None
frame_lock = threading.Lock()

client = SimpleUDPClient("127.0.0.1", 7000)

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (255, 186, 22)

custom_landmark_style = mp_drawing_styles.get_default_hand_landmarks_style()
custom_connection_style = mp_drawing_styles.get_default_hand_connections_style()
for i in custom_landmark_style:
    custom_landmark_style[i].color = (232, 237, 237)
for i in custom_connection_style:
    custom_connection_style[i].color = (232, 237, 237)
    custom_connection_style[i].thickness = 2


def draw_landmarks_on_image(rgb_image, detection_result, pinch_values=None, parallel_palms=False):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]
        hand_label = handedness[0].category_name

        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            custom_landmark_style,
            custom_connection_style
        )
        
        height, width, _ = annotated_image.shape

        if pinch_values and pinch_values[hand_label] is not None:
            thumb_tip = hand_landmarks[4]
            index_tip = hand_landmarks[8]
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)
            cv2.line(annotated_image, (thumb_x, thumb_y), (index_x, index_y), (101, 242, 91), 2)

        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        cv2.putText(
            annotated_image,
            f"{handedness[0].category_name}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA
        )
        
    if parallel_palms and len(detection_result.hand_landmarks) >= 2:
        lm1_palm = detection_result.hand_landmarks[0][9]
        lm2_palm = detection_result.hand_landmarks[1][9]
        height, width, _ = annotated_image.shape

        lm1_x, lm1_y = int(lm1_palm.x * width), int(lm1_palm.y * height)
        lm2_x, lm2_y = int(lm2_palm.x * width), int(lm2_palm.y * height)

        cv2.line(annotated_image, (lm1_x, lm1_y), (lm2_x, lm2_y), (101, 242, 91), 2)

    return annotated_image


# Initialize MediaPipe for Video Mode
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)


def generate_frames():
    global latest_frame
    while True:
        with frame_lock:
            if latest_frame is None:
                continue
            frame_bytes = latest_frame

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )
        time.sleep(0.03)  # Throttle stream yield slightly to prevent high CPU load


def camera_loop():
    global latest_frame
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Get current frame timestamp in milliseconds
        frame_timestamp_ms = int(time.time() * 1000)
        detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)

        is_fist = False
        is_horns = False
        is_shaka = False
        is_peace = False
        pinch_values = {"Right": None, "Left": None}
        hand_openness_values = {"Right": None, "Left": None}
        parallel_palms = False
        distance = 0.0

        if detection_result.hand_landmarks:
            for i, hand in enumerate(detection_result.hand_landmarks):
                hand_label = detection_result.handedness[i][0].category_name

                if not is_fist:
                    is_fist = gestures.is_fist(hand)
                if gestures.is_pinch_gesture(hand):
                    if hand_label == "Right":
                        pinch_values["Right"] = gestures.pinch_value(hand)
                    elif hand_label == "Left":
                        pinch_values["Left"] = gestures.pinch_value(hand)
                if gestures.is_hand_openness_gesture(hand):
                    if hand_label == "Right":
                        hand_openness_values["Right"] = gestures.hand_openness_value(hand)
                    elif hand_label == "Left":
                        hand_openness_values["Left"] = gestures.hand_openness_value(hand)
                if not is_horns:
                    is_horns = gestures.is_horns_gesture(hand)
                if not is_shaka:
                    is_shaka = gestures.is_shaka_gesture(hand)
                if not is_peace:
                    is_peace = gestures.is_peace_sign(hand)

            if len(detection_result.hand_landmarks) == 2:
                hand1 = detection_result.hand_landmarks[0]
                hand2 = detection_result.hand_landmarks[1]
                if gestures.open_palms_parallel(hand1, hand2):
                    parallel_palms = True
                    is_open_hand_gradient = False
                    distance = gestures.hands_distance(hand1, hand2)

            # OSC Telemetry
            if is_fist:
                client.send_message("/is_fist", int(is_fist))
            if pinch_values["Right"] is not None:
                client.send_message("/pinch_value_right", float(pinch_values["Right"]))
            if pinch_values["Left"] is not None:
                client.send_message("/pinch_value_left", float(pinch_values["Left"]))
            if hand_openness_values["Right"] is not None:
                client.send_message("/hand_openness_value_right", float(hand_openness_values["Right"]))
            if hand_openness_values["Left"] is not None:
                client.send_message("/hand_openness_value_left", float(hand_openness_values["Left"]))
            if is_horns:
                client.send_message("/is_horns", int(is_horns))
            if is_shaka:
                client.send_message("/is_shaka", int(is_shaka))
            if parallel_palms:
                client.send_message("/parallel_palms_distance", float(distance))
            if is_peace:
                client.send_message("/is_peace", int(is_peace))

        annotated = draw_landmarks_on_image(rgb_frame, detection_result, pinch_values, parallel_palms)
        annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)

        success_encode, buffer = cv2.imencode(".jpg", annotated_bgr)
        if success_encode:
            with frame_lock:
                latest_frame = buffer.tobytes()

    cap.release()


@app.get("/video")
def video():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    threading.Thread(
        target=camera_loop,
        daemon=True
    ).start()

    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )