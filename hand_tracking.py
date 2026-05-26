import cv2
import mediapipe as mp
import numpy as np
import gestures
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("127.0.0.1", 9000)  # IP and port of the receiver

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

MARGIN = 10  # pixels
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

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    mp_drawing.draw_landmarks(
      annotated_image,
      hand_landmarks,
      mp_hands.HAND_CONNECTIONS,
      custom_landmark_style,
      custom_connection_style)
    
    height, width, _ = annotated_image.shape

    # Thumb tip and Index finger tip
    thumb_tip = hand_landmarks[4]; index_tip = hand_landmarks[8]

    thumb_x = int(thumb_tip.x * width); thumb_y = int(thumb_tip.y * height)
    index_x = int(index_tip.x * width); index_y = int(index_tip.y * height)

    # Draw line between thumb and index finger
    cv2.line(annotated_image, (thumb_x, thumb_y), (index_x, index_y), (101, 242, 91), 2)

    # Get the top left corner of the detected hand's bounding box.
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

def image_tutorial(): 
  # Load the input image.
  img = cv2.imread(r"C:\Users\Giannis Boufidis\Desktop\woman_hands.jpg")
  image = mp.Image.create_from_file(r"C:\Users\Giannis Boufidis\Desktop\woman_hands.jpg")
  cv2.imshow("Input Image", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  # Create an HandLandmarker object.
  base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
  options = vision.HandLandmarkerOptions(base_options=base_options,
                                        num_hands=2)
  detector = vision.HandLandmarker.create_from_options(options)

  # Detect hand landmarks from the input image.
  detection_result = detector.detect(image)
  print(detection_result)

  # Process the classification result. In this case, visualize it.
  annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
  cv2.imshow("Annotated Image", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
  cv2.waitKey(0)
  cv2.destroyAllWindows()

# Create detector once
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.resize(frame, (640, 480))

    # Convert OpenCV frame (BGR) → MediaPipe Image (RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect hands
    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
      is_open_hand = False; is_pinching = False; is_open_hand_gradient = False
      is_horns = False; is_shaka = False
      for hand in detection_result.hand_landmarks:

        if not is_open_hand:
          is_open_hand = gestures.is_open_hand(hand)
        if not is_pinching:
          is_pinching = gestures.is_pinch_gesture(hand)
          pinch_value = gestures.pinch_value(hand)
        if not is_open_hand_gradient:
          is_open_hand_gradient = gestures.is_hand_openness_gesture(hand)
          hand_openness_value = gestures.hand_openness(hand)
        if not is_horns:
           is_horns = gestures.is_horns_gesture(hand)
        if not is_shaka:
           is_shaka = gestures.is_shaka_gesture(hand)

      client.send_message("/is_open_hand", int(is_open_hand))  # Send if open hand or not
      if is_pinching:
        client.send_message("/pinch_value", float(pinch_value))  # Send pinch value
      if is_open_hand_gradient:
        client.send_message("/hand_openness_value", float(hand_openness_value))  # Send hand openness value
      if is_horns:
        client.send_message("/is_horns", int(is_horns))  # Send if horns gesture detected
        print("HORNS GESTURE DETECTED")
      if is_shaka:
        client.send_message("/is_shaka", int(is_shaka))  # Send if shaka gesture detected
        print("SHAKA GESTURE DETECTED")
      # print(f"Sent is_open_hand: {is_open_hand}")  # Print the sent value and its type  

    # Draw result
    annotated = draw_landmarks_on_image(rgb_frame, detection_result)

    # Convert back to OpenCV format
    annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)

    cv2.imshow("Hand Tracking", annotated_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# image_tutorial()
