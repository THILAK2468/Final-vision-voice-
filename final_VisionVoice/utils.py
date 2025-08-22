object_counter = {}
prev_boxes = {}
priority_classes = ["car", "truck", "bus", "motorbike"]

def get_direction(cx, width):
    if cx < width // 3:
        return "ఎడమ"
    elif cx > width * 2 // 3:
        return "కుడి"
    return "ముందు"

def update_counter(label, direction):
    key = f"{label}_{direction}"
    object_counter[key] = object_counter.get(key, 0) + 1
    return object_counter[key]

def is_approaching(curr_box, prev_box):
    if not prev_box:
        return False
    return curr_box[1] < prev_box[1] and (curr_box[2] - curr_box[0]) > (prev_box[2] - prev_box[0])