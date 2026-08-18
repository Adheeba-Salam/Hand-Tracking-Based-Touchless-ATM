import cv2
import time
import datetime
from config import cfg
import mediapipe as mp
from drawpage import DrawPage
from detectclick import DetectClick
from facerec import FaceRec
from database import Database

def main():
    cap = cv2.VideoCapture(0)

    # Set window size for better visibility
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    cv2.namedWindow("Gesture Based - Touchless ATM", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gesture Based - Touchless ATM", 1280, 720)

    dwPg = DrawPage(cfg["pages"])

    # Initialize DetectClick with button coordinates
    detClick = DetectClick(dwPg.getCoordinates(len(cfg["pages"][cfg["currentpage"]]["buttons"])))

    faceRec = FaceRec()
    db = Database()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    mp_hands = mp.solutions.hands.Hands(
        min_detection_confidence=cfg["min_detection_confidence"],
        min_tracking_confidence=cfg["min_tracking_confidence"],
        max_num_hands=cfg["max_num_hands"]
    )

    entered_pin = ""
    pin_submitted = False
    face_authenticated = False
    user_id = None
    user_name = None  # Variable to store the user's name
    balance = None  # Variable to store the user's balance
    face_rec_status = None  # Variable to store face recognition status
    pin_status = None  # Variable to store PIN entry status

    with mp_hands as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                break

            overlay = cv2.flip(image, 1).copy()
            output = cv2.flip(image, 1).copy()

            output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
            output.flags.writeable = False
            results = hands.process(output)
            output.flags.writeable = True
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                imgH, imgW, _ = output.shape
                xpos, ypos = int(hand.landmark[8].x * imgW), int(hand.landmark[8].y * imgH)

                cv2.circle(overlay, (xpos, ypos), 20, (255, 0, 255), cv2.FILLED)
                clickedBtnIndex = detClick.detectClick((xpos, ypos))

                if clickedBtnIndex is not None:
                    print(f"Button {clickedBtnIndex} clicked.")

                    # Face Recognition Logic
                    if cfg["currentpage"] == "FaceRec" and clickedBtnIndex == 2:  # Match button
                        print("Match button clicked. Performing face recognition...")
                        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.05, 5)
                        face_authenticated, user_id, user_name = faceRec.MatchTheFace(image)  # Get user name

                        if face_authenticated:
                            print(f"✅ Face Matched! Welcome, {user_name}. Moving to PIN entry...")
                            face_rec_status = "Face Matched"
                            time.sleep(2)  # Delay to allow hand repositioning
                            cfg["currentpage"] = "PinEntry"
                        else:
                            print("❌ Face Not Matched! Try Again.")
                            face_rec_status = "Face Not Matched"

                    # PIN Entry Logic
                    elif cfg["currentpage"] == "PinEntry" and not pin_submitted:
                        pin_buttons = cfg["pages"]["PinEntry"]["buttons"]
                        if 0 <= clickedBtnIndex < 9:  # Numbers 1-9
                            entered_pin += str(clickedBtnIndex + 1)
                            print(f"Entered PIN: {entered_pin}")
                        elif clickedBtnIndex == 9:  # "E" (Enter)
                            if user_id is not None and db.verify_pin(user_id, entered_pin):
                                print(f"✅ PIN Correct! Welcome, {user_name}. Redirecting to Transactions...")
                                pin_status = "PIN Correct"
                                pin_submitted = True
                                time.sleep(2)  # Delay before transition
                                cfg["currentpage"] = "Transactions"
                            else:
                                print("❌ Incorrect PIN. Try again.")
                                pin_status = "Incorrect PIN"
                                entered_pin = ""
                                time.sleep(1.5)
                        elif clickedBtnIndex == 10:  # "0"
                            entered_pin += "0"
                            print(f"Entered PIN: {entered_pin}")
                        elif clickedBtnIndex == 11:  # "C" (Clear)
                            entered_pin = ""
                            print("🔄 PIN Cleared")

                        # Automatically validate PIN if 4 digits are entered
                        if len(entered_pin) == 4:
                            if user_id is not None and db.verify_pin(user_id, entered_pin):
                                print(f"✅ PIN Correct! Welcome, {user_name}. Redirecting to Transactions...")
                                pin_status = "PIN Correct"
                                pin_submitted = True
                                time.sleep(2)  # Delay before transition
                                cfg["currentpage"] = "Transactions"
                            else:
                                print("❌ Incorrect PIN. Try again.")
                                pin_status = "Incorrect PIN"
                                entered_pin = ""
                                time.sleep(1.5)

                    # Transactions Page Logic
                    elif cfg["currentpage"] == "Transactions":
                        navigation_target = cfg["pages"]["Transactions"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            cfg["currentpage"] = navigation_target
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Withdraw Account Selection Logic
                    elif cfg["currentpage"] == "Withdraw-SelAccType":
                        navigation_target = cfg["pages"]["Withdraw-SelAccType"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            cfg["currentpage"] = navigation_target
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Withdraw Amount Selection Logic
                    elif cfg["currentpage"] == "SelectAmountW":
                        navigation_target = cfg["pages"]["SelectAmountW"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            try:
                                # Extract amount from button text (e.g., "Rs.100")
                                amount = int(cfg["pages"]["SelectAmountW"]["buttons"][clickedBtnIndex].split("Rs.")[1])
                                if db.update_balance(user_id, amount, "Withdraw"):
                                    print(f"✅ Withdrawal of Rs.{amount} successful!")
                                    cfg["currentpage"] = "Withdraw"
                                else:
                                    print("❌ Insufficient balance or error during withdrawal.")
                            except (IndexError, ValueError) as e:
                                print(f"❌ Error extracting amount from button text: {cfg['pages']['SelectAmountW']['buttons'][clickedBtnIndex]}")
                                print(f"Error details: {e}")
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Balance Account Selection Logic
                    elif cfg["currentpage"] == "Balance-SelAccType":
                        navigation_target = cfg["pages"]["Balance-SelAccType"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            balance = db.get_balance(user_id)  # Fetch balance from the database
                            print(f"Your balance is: Rs.{balance}")
                            cfg["currentpage"] = "ReceiptBL"
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Deposit Account Selection Logic
                    elif cfg["currentpage"] == "Deposit-SelAccType":
                        navigation_target = cfg["pages"]["Deposit-SelAccType"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            cfg["currentpage"] = navigation_target
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Deposit Amount Selection Logic
                    elif cfg["currentpage"] == "SelectAmountD":
                        navigation_target = cfg["pages"]["SelectAmountD"]["navigation"][clickedBtnIndex]
                        if navigation_target:
                            print(f"Navigating to: {navigation_target}")
                            try:
                                # Extract amount from button text (e.g., "Rs.100")
                                amount = int(cfg["pages"]["SelectAmountD"]["buttons"][clickedBtnIndex].split("Rs.")[1])
                                if db.update_balance(user_id, amount, "Deposit"):
                                    print(f"✅ Deposit of Rs.{amount} successful!")
                                    cfg["currentpage"] = "Deposit"
                                else:
                                    print("❌ Error during deposit.")
                            except (IndexError, ValueError) as e:
                                print(f"❌ Error extracting amount from button text: {cfg['pages']['SelectAmountD']['buttons'][clickedBtnIndex]}")
                                print(f"Error details: {e}")
                            time.sleep(1)  # Optional: Add a small delay for better UX

                    # Handle "Back" button on receipt and success pages
                    elif cfg["currentpage"] in ["ReceiptBL", "Withdraw", "Deposit"]:
                        if clickedBtnIndex == 8:  # "Back" button
                            cfg["currentpage"] = "Transactions"
                            time.sleep(1)  # Optional: Add a small delay for better UX

            # Draw the current page
            dwPg.drawThePage(cfg["currentpage"], overlay)

            # Display face recognition status only on the FaceRec page
            if cfg["currentpage"] == "FaceRec" and face_rec_status:
                cv2.putText(overlay, face_rec_status, (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if face_authenticated else (0, 0, 255), 2)

            # Display PIN entry status only on the PinEntry page
            if cfg["currentpage"] == "PinEntry" and pin_status:
                cv2.putText(overlay, pin_status, (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if pin_status == "PIN Correct" else (0, 0, 255), 2)

            # Display entered PIN as asterisks (*) on the PinEntry page
            if cfg["currentpage"] == "PinEntry":
                masked_pin = "*" * len(entered_pin)
                cv2.putText(overlay, f"Entered PIN: {masked_pin}", (550, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display balance on the ReceiptBL page
            if cfg["currentpage"] == "ReceiptBL" and balance is not None:
                cv2.putText(overlay, f"Your balance is: Rs.{balance}", (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Show the output
            cv2.imshow("Gesture Based - Touchless ATM", overlay)

            # Exit loop if 'q' is pressed
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()