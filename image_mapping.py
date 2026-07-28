IMAGE_MAP = {


# ===========
# MAINTENANCE D
# =========================

"barrel":
[
    "screw and barrel.jpeg"
],

    "screw":
    [
        "S10_screw_tip.jpeg",
        "screw and barrel.jpeg"
],

"mechanical safety":
[
"main_D.jpeg",
"D1_safety_gate.jpeg"
],

"safety gate":
[
"main_D.jpeg",
"D1_safety_gate.jpeg"
],


"cover":
[
"main_D.jpeg",
"D2_cover.jpeg"
],


"cooling":
[
"main_D.jpeg",
"D3_cooling_valve.jpeg"
],


"controller":
[
"main_D.jpeg",
"D6_controller.jpeg"
],


"temperature":
[
"main_D.jpeg",
"D6_controller.jpeg"
],


"oil":
[
"main_D.jpeg",
"D10_oil_level.jpeg"
],

"cooler":
[
"main_D.jpeg",
"D9_cooler_servo_motor.jpeg"
],


# =========================
# MAINTENANCE S
# =========================


"nozzle":
[
"main_S.jpeg",
"S5_nozzle.jpeg"
],


"hose":
[
"main_S.jpeg",
"S7_high_pressure_hose.png"
],


"pressure":
[
"main_S.jpeg",
"S7_high_pressure_hose.png"
],


"pump":
[
"main_S.jpeg",
"S8_tank_pump.jpeg"
],


"tank":
[
"main_S.jpeg",
"S8_tank_pump.jpeg"
],


"air":
[
"main_S.jpeg",
"S9_air_filter.jpeg"
],


"filter":
[
"main_S.jpeg",
"S9_air_filter.jpeg"
],


"servo motor":
[
"main_S.jpeg",
"S3_hydraulic_motor.jpeg"
],

"hydraulic motor":
[
"main_S.jpeg",
"S3_hydraulic_motor.jpeg"
]

}




DEFAULT_IMAGE = [

"main_D.jpeg",

"main_S.jpeg"

]





def find_related_image(question):


    question = question.lower()



    for keyword, images in IMAGE_MAP.items():


        if keyword in question:


            return images



    # IF NOTHING MATCH
    # ALWAYS SHOW MACHINE VISUAL

    return DEFAULT_IMAGE