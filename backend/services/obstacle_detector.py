# --------------------------------------------------
# OBJECT CATEGORIES
# --------------------------------------------------

OBSTACLE_CLASSES = {

    "pothole",
    "stairs",
    "curb",
    "pole",
    "obstacle",
    "barrier",
    "construction"

}


VEHICLE_CLASSES = {

    "car",
    "bus",
    "truck",
    "motorcycle",
    "bicycle",
    "vehicle"

}


SIGN_CLASSES = {

    "stop_sign",
    "no_entry",
    "warning_sign",
    "pedestrian_crossing",
    "speed_limit",
    "traffic_sign",
    "exit_sign",
    "sign",
    "traffic_light"

}


# --------------------------------------------------
# ANALYZE DETECTIONS
# --------------------------------------------------

def analyze_detections(detections):

    people = []

    obstacles = []

    vehicles = []

    signs = []


    # --------------------------------------------------
    # CLASSIFY DETECTIONS
    # --------------------------------------------------

    for detection in detections:

        name = detection[
            "class_name"
        ].lower().strip()


        if name == "person":

            people.append(
                detection
            )


        elif name in OBSTACLE_CLASSES:

            obstacles.append(
                detection
            )


        elif name in VEHICLE_CLASSES:

            vehicles.append(
                detection
            )


        elif name in SIGN_CLASSES:

            signs.append(
                detection
            )


    # --------------------------------------------------
    # HAZARD PRIORITY
    # --------------------------------------------------

    # Highest priority: obstacles
    if obstacles:

        first = obstacles[0]

        object_name = (
            first["class_name"]
            .replace("_", " ")
        )

        hazard = "HIGH"

        message = (
            f"Warning. {object_name} "
            f"detected ahead."
        )


    # Second priority: vehicles
    elif vehicles:

        first = vehicles[0]

        object_name = (
            first["class_name"]
            .replace("_", " ")
        )

        hazard = "HIGH"

        message = (
            f"Caution. {object_name} "
            f"detected nearby."
        )


    # Third priority: people
    elif people:

        hazard = "MEDIUM"

        message = (
            "Person detected ahead."
        )


    # Signs are informational
    elif signs:

        first = signs[0]

        object_name = (
            first["class_name"]
            .replace("_", " ")
        )

        hazard = "INFO"

        message = (
            f"{object_name} detected."
        )


    # Nothing detected
    else:

        hazard = "SAFE"

        message = (
            "The path ahead appears clear."
        )


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {

        "people": people,

        "obstacles": obstacles,

        "vehicles": vehicles,

        "signs": signs,

        "people_count": len(
            people
        ),

        "obstacle_count": len(
            obstacles
        ),

        "vehicle_count": len(
            vehicles
        ),

        "sign_count": len(
            signs
        ),

        "hazard": hazard,

        "message": message

    }