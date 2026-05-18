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