import time
from config import cfg

class DetectClick:
    def __init__(self, circleCenters):
        self.circleCenters = circleCenters or []
        self.last_click_time = 0

    def detectClick(self, fingertip):
        curPg = cfg.get("currentpage", "")
        buttons = cfg["pages"].get(curPg, {}).get("buttons", [])
        radius = cfg["btnparams"].get("R", 40)
        click_delay = 0.8  # Reduced delay for responsiveness

        current_time = time.time()
        if current_time - self.last_click_time < click_delay:
            return None

        for i, (center_x, center_y) in enumerate(self.circleCenters):
            if i < len(buttons) and buttons[i]:
                distance_squared = (fingertip[0] - center_x) ** 2 + (fingertip[1] - center_y) ** 2
                if distance_squared < radius ** 2:
                    self.last_click_time = current_time
                    print(f"✅ Button {i} clicked at ({center_x}, {center_y})")  # Debug coordinates
                    return i
        return None