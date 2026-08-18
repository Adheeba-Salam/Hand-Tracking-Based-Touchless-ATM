import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql@123",
            database="GestureATM"
        )
        self.cursor = self.conn.cursor()

    def get_user_by_face(self, face_id):
        query = "SELECT user_id, name, pin, balance FROM users WHERE face_id = %s"
        self.cursor.execute(query, (face_id,))
        return self.cursor.fetchone()

    def verify_pin(self, user_id, entered_pin):
        query = "SELECT pin FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        stored_pin = self.cursor.fetchone()
        return stored_pin and stored_pin[0] == entered_pin

    def get_balance(self, user_id):
        query = "SELECT balance FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.00

    def update_balance(self, user_id, amount, transaction_type):
        current_balance = self.get_balance(user_id)
        if transaction_type == "Withdraw":
            new_balance = current_balance - amount
        elif transaction_type == "Deposit":
            new_balance = current_balance + amount
        else:
            return False

        # Update user balance
        update_query = "UPDATE users SET balance = %s WHERE user_id = %s"
        self.cursor.execute(update_query, (new_balance, user_id))

        # Record transaction
        transaction_query = """
            INSERT INTO transactions (user_id, amount, transaction_type)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(transaction_query, (user_id, amount, transaction_type))
        self.conn.commit()
        return True

    def close_connection(self):
        self.cursor.close()
        self.conn.close()