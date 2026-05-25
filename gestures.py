import math
import itertools

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def is_open_hand(lm):
    return (
        lm[8].y < lm[6].y and   # index up
        lm[12].y < lm[10].y and # middle up
        lm[16].y < lm[14].y and # ring up
        lm[20].y < lm[18].y     # pinky up
    )

def is_peace_sign(lm):
   return(
      lm[8].y < lm[6].y and   # index up
      lm[12].y < lm[10].y and # middle up
      lm[16].y > lm[14].y and # ring up
      lm[20].y > lm[18].y     # pinky up
   )

global_min_open = float("inf")
global_max_open = float("-inf")
def is_hand_openness_gesture(lm):
    return (lm[12].y < lm[9].y and  # middle stretched
            lm[16].y < lm[13].y and  # ring stretched
            lm[20].y < lm[17].y)     # pinky stretched

def hand_openness(lm):
    global global_min_open, global_max_open
    fingertips = [
        lm[4],   # thumb
        lm[8],   # index
        lm[12],  # middle
        lm[16],  # ring
        lm[20]   # pinky
    ]

    pairs = itertools.combinations(fingertips, 2)
    distances = []
    for a, b in pairs:
        distances.append(distance(a, b))

    avg_distance = sum(distances) / len(distances)
    # normalize with palm size
    palm_size = distance(lm[0], lm[9])
    normalized = avg_distance / palm_size

    # dynamic calibration
    global_min_open = min(global_min_open, normalized)
    global_max_open = max(global_max_open, normalized)

    openness = ((normalized - global_min_open) / (global_max_open - global_min_open)) if global_max_open > global_min_open else 0.0

    return max(0.0, min(1.0, openness))

global_min_pinch = float("inf")
global_max_pinch = float("-inf")
def is_pinch_gesture(lm):
    return (lm[12].y > lm[9].y and  # middle tucked
            lm[16].y > lm[13].y and  # ring tucked
            lm[20].y > lm[17].y)     # pinky tucked

def pinch_value(lm):
    global global_min_pinch, global_max_pinch
    thumb = lm[4]
    index = lm[8]
    dist = distance(thumb, index)

    # normalize with palm size
    palm_size = distance(lm[0], lm[9])
    normalized = dist / palm_size

    # calibration
    global_min_pinch = min(global_min_pinch, normalized)
    global_max_pinch = max(global_max_pinch, normalized)

    pinch = (normalized - global_min_pinch) / (global_max_pinch - global_min_pinch) if global_max_pinch > global_min_pinch else 0.0

    # invert (θέλουμε touching = 1)
    pinch = 1.0 - pinch

    return max(0.0, min(1.0, pinch))

def react_to_gesture(detection_result):
    if detection_result.hand_landmarks:
      for i in range(len(detection_result.hand_landmarks)):
            hand_landmarks = detection_result.hand_landmarks[i]
            print("Hand Openness:", hand_openness(hand_landmarks))
            # label = detection_result.handedness[i][0].display_name
            # if is_open_hand(hand_landmarks):
            #     print("OPEN HAND")
            # if is_peace_sign(hand_landmarks):
            #     print("PEACE EVERYBODY!")
