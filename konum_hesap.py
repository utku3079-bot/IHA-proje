import math
METRE_PER_DERECE = 111320
def mesafe(enlem_1, boylam_1, enlem_2, boylam_2):
    dikeyde_alinan_yol = (enlem_2 - enlem_1) * METRE_PER_DERECE
    yatayda_alinan_yol = (boylam_2 - boylam_1) * math.cos(math.radians(enlem_1)) * METRE_PER_DERECE
    alinan_yol = math.sqrt(yatayda_alinan_yol * yatayda_alinan_yol + dikeyde_alinan_yol * dikeyde_alinan_yol )
    return(alinan_yol)
print(mesafe(-35.3632627, 149.1652379, -35.3632627, 149.1652379))