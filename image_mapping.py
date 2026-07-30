IMAGE_FOLDER = "images"


IMAGE_MAP = {


    "safety gate":
    [
        "main_D.jpeg",
        "D1_safety_gate.jpeg",
        "D7_controller_setting.jpeg"
    ],
    "mechanical":
    [
        "main_D.jpeg",
        "mechanical safety.jpeg",
        "D1_safety_gate.jpeg"
    ],


    "cover":
    [
        "main_D.jpeg",
        "D2_cover.jpeg",
        "D8_barrel_cover.jpeg"
    ],


    "cooling valve":
    [
        "main_D.jpeg",
        "D3_cooling_valve.jpeg"
    ],


    "mold mounting bolt":
    [
        "main_D.jpeg",
        "D4_mold_mounting_bolt.jpeg"
    ],


    "mold":
    [
        "main_D.jpeg",
        "D5_mold.jpeg"
    ],


    "controller":
    [
        "main_D.jpeg",
        "D6_controller.jpeg",
        "D7_controller_setting.jpeg"
    ],


    "controller setting":
    [
        "main_D.jpeg",
        "D7_controller_setting.jpeg"
    ],


    "barrel cover":
    [
        "main_D.jpeg",
        "D8_barrel_cover.jpeg",
        "screw and barrel.jpeg"
    ],


    "oil cooler":
    [
        "main_D.jpeg",
        "D9_oil_cooler.jpeg"
    ],


    "oil level":
    [
        "main_D.jpeg",
        "D10_oil_level.jpeg"
    ],


    "hydraulic motor":
    [
        "main_S.jpeg",
        "servo motor.jpeg",
        "S3_hydraulic_motor.jpeg"
    ],

    "servo motor":
    [
        "main_S.jpeg",
        "main_D.jpeg",
        "servo motor.jpeg",
        "S3_hydraulic_motor.jpeg"
    ],

    "nozzle":
    [
        "main_S.jpeg",
        "S5_nozzle.jpeg"
    ],


    "tank cooler":
    [
        "main_S.jpeg",
        "S6_tank_cooler.jpeg"
    ],


    "high pressure hose":
    [
        "main_S.jpeg",
        "S7_high_pressure_hose.png"
    ],


    "tank pump":
    [
        "main_S.jpeg",
        "S8_tank_pump.jpeg"
    ],


    "air filter":
    [
        "main_S.jpeg",
        "S9_air_filter.jpeg"
    ],


    "screw tip":
    [
        "main_S.jpeg",
        "S10_screw_tip.jpeg",
        "screw and barrel.jpeg"
    ],

    "temperature":
    [
        "main_D.jpeg",
        "temperature.jpeg"
    ],

    "injection unit":
    [
        "main_D.jpeg",
        "injection unit.jpeg"
    ],

    "alarm":
    [
        "temperature.jpeg",
    ],

    "barrel temperature":
    [
        "main_D.jpeg",
        "temperature.jpeg",
        "screw and barrel.jpeg",
        "D6_controller.jpeg"
    ]

}



DEFAULT_IMAGES = [
    "main_D.jpeg",
    "main_S.jpeg"
]



def get_related_images(question):

    
    question = question.lower()


    result=[]


    for keyword, images in IMAGE_MAP.items():

        if keyword in question:

            for img in images:

                if img not in result:
                    result.append(img)


    if not result:

        result.extend(DEFAULT_IMAGES)


    return result