import math
import itertools

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def thumb_extended(lm):
    return distance (lm[4], lm[17]) > distance(lm[0], lm[17])
def index_extended(lm):
    return distance(lm[8], lm[0]) > distance(lm[6], lm[0])
def middle_extended(lm):
    return distance(lm[12], lm[0]) > distance(lm[10], lm[0])
def ring_extended(lm):
    return distance(lm[16], lm[0]) > distance(lm[14], lm[0])
def pinky_extended(lm):
    return distance(lm[20], lm[0]) > distance(lm[18], lm[0])

def palm_facing_camera(lm):
    # Check if the palm is facing the camera by comparing the z-coordinates of the wrist and thumb tip
    return lm[17].z < lm[4].z

def is_open_hand(lm):
    return (
        index_extended(lm) and
        middle_extended(lm) and
        ring_extended(lm) and
        pinky_extended(lm)
    )

def is_fist(lm):
    return not (
        thumb_extended(lm) or
        index_extended(lm) or
        middle_extended(lm) or
        ring_extended(lm) or
        pinky_extended(lm)
    )

def is_peace_sign(lm):
   return(
      not thumb_extended(lm) and
      index_extended(lm) and
      middle_extended(lm) and
      not ring_extended(lm) and
      not pinky_extended(lm)
   )

def is_horns_gesture(lm):
    return (
        not thumb_extended(lm) and
        index_extended(lm) and
        not middle_extended(lm) and
        not ring_extended(lm) and
        pinky_extended(lm)
    )

def is_shaka_gesture(lm):
    return (
        thumb_extended(lm) and
        not index_extended(lm) and
        not middle_extended(lm) and
        not ring_extended(lm) and
        pinky_extended(lm)
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
    return (distance(lm[8], lm[0]) > distance(lm[5], lm[0]) and  # index stretched
            distance (lm[12], lm[0]) > distance(lm[9], lm[0]) and  # middle stretched
            distance(lm[16], lm[0]) > distance(lm[13], lm[0]) and  # ring stretched
            distance(lm[20], lm[0]) > distance(lm[17], lm[0]))     # pinky stretched
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
    return (
        index_extended(lm) and
        not middle_extended(lm) and
        not ring_extended(lm) and
        not pinky_extended(lm)   
    )
def pinch_value(lm):
    thumb = lm[4]
    index = lm[8]
    thumb_index = distance(thumb, index)

    # normalize with palm size
    palm_size = distance(lm[0], lm[5])
    pinch = thumb_index  / palm_size

    return 1.0 - min(pinch / 1.15, 1.0)