import mysql.connector


class UserDB:
    def __init__(self):
        self.database_connection = mysql.connector.connect(host='localhost', user='root', password='Ilyas2006#', database='jix_bot')

    def create_user(self, user_id, username):
        self.database_connection.reconnect()

        cursor = self.database_connection.cursor()
        query = "INSERT INTO users (user_id, username) VALUES (%s, %s)"

        cursor.execute(query, (user_id, username))

        self.database_connection.commit()
        print('User added successfully!')

        cursor.close()

    def get_all(self):
        try:
            self.database_connection.reconnect()
            cursor = self.database_connection.cursor()

            query = "SELECT * FROM users"

            cursor.execute(query)

            return cursor.fetchall()
        except Exception as e:
            print("Ошибка при работе с MySQL", e)

    def get_username_by_user_id(self, user_id):
        try:
            self.database_connection.reconnect()

            cursor = self.database_connection.cursor()
            query = "SELECT `username` FROM users WHERE user_id = %s"

            cursor.execute(query, (user_id,))

            print('Successfully return username by user id')
            return cursor.fetchall()[0][0]

        except Exception as e:
            print(e)

        finally:
            cursor.close()

    def get_user_id_by_username(self, username):
        try:
            self.database_connection.reconnect()

            cursor = self.database_connection.cursor()
            query = "SELECT `user_id` FROM users WHERE username = %s"

            cursor.execute(query, (username,))

            print('Successfully return user_id by username')
            return cursor.fetchall()[0][0]

        except Exception as e:
            print(e)

    def get_user_tokens(self, user_id):
        try:
            self.database_connection.reconnect()

            cursor = self.database_connection.cursor()
            query = "SELECT `tokens` FROM users WHERE user_id = %s"

            cursor.execute(query, (user_id,))

            print('Successfully return tokens by user_id')
            return cursor.fetchall()[0][0]

        except Exception as e:
            print(e)


if __name__ == '__main__':
    user_db = UserDB()
    print(user_db.get_user_tokens(7047174818) + 1)