from config import cfg
import cv2
import numpy as np
from operator import itemgetter

class DrawPage:
    def __init__(self, pages):
        self.pages = pages

    def drawThePage(self, pageName, img):
        buttons = self.pages[pageName]["buttons"]
        btnclr = cfg["btnclr"]
        circlr = (255, 255, 255)  # Transparent circle outline
        R = cfg["btnparams"]["R"]
        txt = cfg["txtparams"]
        xadj, yadj, font, fontScale, tness = itemgetter("xadj", "yadj", "font", "fontScale", "thickness")(txt)
        txtclr = cfg["txtclr"]
        coords = self.getCoordinates(len(buttons))

        # Create an overlay layer for transparency effects
        overlay = img.copy()
        circle_layer = np.zeros_like(img, dtype=np.uint8)  # Transparent layer

        for i in range(len(buttons)):
            if buttons[i] and buttons[i].strip():
                if i < len(coords):
                    center_x, center_y = coords[i]

                    # Get text size dynamically
                    text_size = cv2.getTextSize(buttons[i], font, fontScale, tness)[0]
                    text_width, text_height = text_size

                    # Adjust button size based on text width
                    padding_x = 20  # Extra padding around text
                    padding_y = 15
                    btn_width = text_width + 2 * padding_x
                    btn_height = text_height + 2 * padding_y

                    # Calculate button rectangle
                    pt1 = (center_x - btn_width // 2, center_y - btn_height // 2)
                    pt2 = (center_x + btn_width // 2, center_y + btn_height // 2)

                    # Draw the button background
                    cv2.rectangle(img, pt1, pt2, btnclr, cv2.FILLED)

                    # Center text inside the button
                    text_x = center_x - text_width // 2
                    text_y = center_y + text_height // 2
                    cv2.putText(img, buttons[i], (text_x, text_y), font, fontScale, txtclr, tness)

                    # Draw a transparent circle outline
                    cv2.circle(circle_layer, (center_x, center_y), R, circlr, 2)  # Thin outline

                else:
                    print(f"Warning: Button {i} has no coordinates!")

        # Blend the transparent circle layer with the main image
        alpha = 0.3  # Adjust transparency (lower = more transparent)
        cv2.addWeighted(circle_layer, alpha, img, 1, 0, img)

        # Draw the page title if available
        if "pagetitle" in self.pages[pageName]:
            title, titleY, fontSize, titleclr, titletness = self.pages[pageName]["pagetitle"]
            titleX = self.getXOrgofText(title, font, fontSize, titletness)
            cv2.putText(img, title, (titleX, titleY), font, fontSize, titleclr, titletness)

    def getXOrgofText(self, text, fontFace, fontScale, thickness):
        (W, _), _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
        rem = cfg["screen_x"] - W
        return rem // 2

    def getCoordinates(self, num_buttons):
        """Corrected coordinates for 12 buttons (3x4 grid)"""
        button_positions = [
            (213, 660), (639, 660), (1065, 660),  # Row 1: 1, 2, 3
            (213, 560), (639, 560), (1065, 560),  # Row 2: 4, 5, 6
            (213, 460), (639, 460), (1065, 460),  # Row 3: 7, 8, 9
            (213, 360), (639, 360), (1065, 360)   # Row 4: E, 0, C
        ]
        return button_positions[:num_buttons]
