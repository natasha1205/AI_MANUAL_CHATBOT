# image_mapping.py

IMAGE_FOLDER = "images"


# ======================================
# IMAGE DATABASE
# ======================================

IMAGE_MAP = {


    # =========================
    # D SECTION (Machine Parts)
    # =========================

    "safety gate": [
        "main_D.jpeg",
        "D1_safety_gate.jpeg"
    ],

    "cover": [
        "main_D.jpeg",
        "D2_cover.jpeg"
    ],

    "cooling valve": [
        "main_D.jpeg",
        "D3_cooling_valve.jpeg"
    ],

    "mold mounting bolt": [
        "main_D.jpeg",
        "D4_mold_mounting_bolt.jpeg"
    ],

    "mold": [
        "main_D.jpeg",
        "D5_mold.jpeg"
    ],

    "controller": [
        "main_D.jpeg",
        "D6_controller.jpeg"
    ],

    "controller setting": [
        "main_D.jpeg",
        "D7_controller_setting.jpeg"
    ],

    "barrel cover": [
        "main_D.jpeg",
        "D8_barrel_cover.jpeg"
    ],

    "servo motor": [
        "main_S.jpeg",
        "S3_hydraulic_motor.jpeg",
        "main_D.jpeg",
        "D9_cooler_servo_motor.jpeg"
    ],

    "oil cooler": [
        "main_D.jpeg",
        "D9_oil_cooler.jpeg"
    ],

    "oil level": [
        "main_D.jpeg",
        "D10_oil_level.jpeg"
    ],



    # =========================
    # S SECTION (Maintenance)
    # =========================


    "hydraulic motor": [
        "main_S.jpeg",
        "S3_hydraulic_motor.jpeg"
    ],

    "nozzle": [
        "main_S.jpeg",
        "S5_nozzle.jpeg"
    ],

    "tank cooler": [
        "main_S.jpeg",
        "S6_tank_cooler.jpeg"
    ],

    "high pressure hose": [
        "main_S.jpeg",
        "main_D.jpeg",
        "S7_high_pressure_hose.png"
    ],

    "tank pump": [
        "main_S.jpeg",
        "S8_tank_pump.jpeg"
    ],

    "air filter": [
        "main_S.jpeg",
        "S9_air_filter.jpeg"
    ],

    "screw tip": [
        "main_S.jpeg",
        "S10_screw_tip.jpeg",
        "screw and barrel.jpeg"
    ],

    "screw and barrel": [
        "screw and barrel.jpeg",
        "S10_screw_tip.jpeg"
    ]

}



# ======================================
# IMAGE SEARCH FUNCTION
# ======================================


def get_related_images(answer):

    answer = answer.lower()


    result = []


    has_D = False
    has_S = False



    # Always detect main section
    for keyword, images in IMAGE_MAP.items():

        if keyword in answer:


            for img in images:

                result.append(img)


                if img.startswith("D"):
                    has_D = True


                if img.startswith("S"):
                    has_S = True



    # ==============================
    # ADD MAIN IMAGE
    # ==============================


    final_images = []


    # D related
    if has_D:

        final_images.append(
            "main_D.jpeg"
        )


    # S related
    if has_S:

        final_images.append(
            "main_S.jpeg"
        )


    # no relation
    if not has_D and not has_S:

        final_images.append(
            "main_D.jpeg"
        )

        final_images.append(
            "main_S.jpeg"
        )



    # add related images

    for img in result:

        if img not in final_images:

            final_images.append(img)



    return final_images