cfg = {
    "screen_x": 1280,
    "screen_y": 720,
    "min_detection_confidence": 0.65,
    "min_tracking_confidence": 0.65,
    "max_num_hands": 1,
    "tolerance": 0.75,
    "alpha": 0.75,
    "btnClickDelay": 1.5,
    "btnclr": (0, 0, 0),  # Changed to black
    "txtclr": (255, 255, 255),
    "btnparams": {
        "W": 400,
        "H": 80,
        "BtnSp": 20,
        "R": 40,
        "CirSp": 50
    },
    "txtparams": {
        "xadj": +20,
        "yadj": -20,
        "font": 0,
        "fontScale": 1.8,
        "thickness": 2
    },
    "currentpage": "FaceRec",
    "pages": {
        "FaceRec": {
            "pagetitle": ["Select Match to match your face and Login", 100, 1.5, (255, 0, 0), 4],
            "buttons": ["","","Match","","","","","","","","",""],
            "navigation": ["", "", "PinEntry", "", "", "", "", "","","","",""]
        },
        "PinEntry": {
            "pagetitle": ["Enter Your PIN", 150, 2, (255, 0, 0), 4],
            "buttons": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Enter", "0", "Clear"],
            "navigation": ["", "", "", "", "", "", "", "", "", "", "", "Transactions"]
        },
        "Transactions": {
            "pagetitle": ["Select Any Transaction", 150, 2, (255, 0, 0), 4],
            "buttons": ["DEPOSIT", "", "EXIT", "", "", "", "WITHDRAW", "","BALANCE","","",""],
            "navigation": ["Deposit-SelAccType", "", "Exit","","","", "Withdraw-SelAccType", "", "Balance-SelAccType", "","",""]
        },
        "Withdraw-SelAccType": {
            "pagetitle": ["Select Account Type", 150, 2, (255, 0, 0), 4],
            "buttons": ["","", "","","","Savings", "", "", "Current"],
            "navigation": ["","", "","","","SelectAmountW", "", "","SelectAmountW" ]
        },
        "SelectAmountW": {
            "pagetitle": ["Select Amount to Withdraw", 150, 2, (255, 0, 0), 4],
            "buttons": ["","","Rs.100","","", "Rs.200","","", "Rs.500","","","Rs.2000"],
            "navigation": ["","","Withdraw","","", "Withdraw","","", "Withdraw","","","Withdraw"]
        },
        "Balance-SelAccType": {
            "pagetitle": ["Select Account Type", 150, 2, (255, 0, 0), 4],
            "buttons": ["","", "","","","Savings", "", "", "Current"],
            "navigation": ["","", "","","","ReciptBL", "", "", "ReciptBL"]
        },
        "Deposit-SelAccType": {
            "pagetitle": ["Select Account Type", 150, 2, (255, 0, 0), 4],
            "buttons": ["","", "","","","Savings", "", "", "Current"],
            "navigation": ["","", "","","","SelectAmountD", "", "","SelectAmountD"]
        },
        "SelectAmountD": {
            "pagetitle": ["Select Amount to Deposit", 150, 2, (255, 0, 0), 4],
            "buttons": ["","","Rs.100","","", "Rs.200","","", "Rs.500","","","Rs.2000"],
            "navigation": ["","","Deposit","","", "Deposit","","", "Deposit","","","Deposit"]
        },
        "ReceiptBL": {
            "pagetitle": ["Your Balance is:", 150, 2, (255, 0, 0), 4],
            "buttons": ["", "", "", "", "", "", "", "", "Back"],
            "navigation": ["", "", "", "", "", "", "", "", "Transactions"]
        },
        "Withdraw": {
            "pagetitle": ["Withdraw Successful!", 150, 2, (255, 0, 0), 4],
            "buttons": ["", "", "", "", "", "", "", "", "Back"],
            "navigation": ["", "", "", "", "", "", "", "", "Transactions"]
        },
        "Deposit": {
            "pagetitle": ["Deposit Successful!", 150, 2, (255, 0, 0), 4],
            "buttons": ["", "", "", "", "", "", "", "", "Back"],
            "navigation": ["", "", "", "", "", "", "", "", "Transactions"]
        },
    }
}