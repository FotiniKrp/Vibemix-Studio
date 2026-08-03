import math
import itertools

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def palm_facing_camera(lm):
    # Check if the palm is facing the camera by comparing the z-coordinates of the wrist and thumb tip
    return lm[17].z < lm[4].z

def is_open_hand(lm):
    return (
        lm[8].y < lm[6].y and   # index up
        lm[12].y < lm[10].y and # middle up
        lm[16].y < lm[14].y and # ring up
        lm[20].y < lm[18].y     # pinky up
    )

def is_fist(is_hand_right, lm):
    return (
        lm[8].y > lm[5].y and   # index down
        lm[12].y > lm[9].y and  # middle down
        lm[16].y > lm[13].y and # ring down
        lm[20].y > lm[17].y and # pinky down
        (lm[4].x < lm[1].x if is_hand_right 
         else lm[4].x > lm[1].x)  # thumb tucked
    )

def is_peace_sign(is_hand_right, lm):
   return(
      lm[8].y < lm[6].y and   # index up
      lm[12].y < lm[10].y and # middle up
      lm[16].y > lm[14].y and # ring up
      lm[20].y > lm[18].y and # pinky up
      (lm[4].x < lm[1].x if is_hand_right 
       else lm[4].x > lm[1].x)  # thumb tucked
   )

def is_horns_gesture(is_hand_right, lm):
    return (
        lm[8].y < lm[6].y and    # index up
        lm[20].y < lm[18].y and  # pinky up
        lm[12].y > lm[10].y and  # middle down
        lm[16].y > lm[14].y and  # ring down
        (lm[4].x < lm[1].x if is_hand_right 
         else lm[4].x > lm[1].x)  # thumb tucked
    )

def is_shaka_gesture(is_hand_right, lm):
    return (
        lm[4].y < lm[3].y and   # thumb extended upwards
        (lm[6].x < lm[8].x if not is_hand_right 
         else lm[6].x > lm[8].x) and # index tucked
        (lm[10].x < lm[12].x if not is_hand_right 
        else lm[10].x > lm[12].x) and # middle tucked
        (lm[14].x < lm[16].x if not is_hand_right 
        else lm[14].x > lm[16].x) and # ring tucked
        (lm[20].x < lm[18].x if not is_hand_right 
        else lm[20].x > lm[18].x)  # pinky extended outwards
    )

def open_palms_parallel(lm1, lm2):
    return (palm_facing_camera(lm1) and is_open_hand(lm1) and 
            palm_facing_camera(lm2) and is_open_hand(lm2))
def hands_distance(lm1, lm2):
    dist = abs(lm1[9].x - lm2[9].x)

    min_d = 0.0; max_d = 0.8
    norm = (dist - min_d) / (max_d - min_d)

    return max(0.0, min(1.0, norm))

def is_hand_openness_gesture(lm):
    return (lm[12].y < lm[9].y and  # middle stretched
            lm[16].y < lm[13].y and  # ring stretched
            lm[20].y < lm[17].y)     # pinky stretched
def hand_openness_value(lm):
    MIN_OPEN = 0.20; MAX_OPEN = 1.05
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
    palm_size = distance(lm[0], lm[5])
    ratio = avg_distance / palm_size
    openness = (ratio - MIN_OPEN) / (MAX_OPEN - MIN_OPEN)

    return max(0.0, min(1.0, openness))

def is_pinch_gesture(lm):
    return (lm[12].y > lm[9].y and   # middle tucked
            lm[16].y > lm[13].y and  # ring tucked
            lm[20].y > lm[17].y and  # pinky tucked
            lm[8].y < lm[5].y)         # index up
def pinch_value(lm):
    thumb = lm[4]
    index = lm[8]
    thumb_index = distance(thumb, index)

    # normalize with palm size
    palm_size = distance(lm[0], lm[5])
    pinch = thumb_index  / palm_size

    return 1.0 - min(pinch / 1.15, 1.0)
