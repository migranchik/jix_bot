import mysql.connector


class LearnPhotoDB:
    def __init__(self):
        self.database_connection = mysql.connector.connect(host='localhost', user='root', password='Ilyas2006#', database='jix_bot')

    def add_photo(self, file_id, file_name, user_id, model_title):
        self.database_connection.reconnect()

        cursor = self.database_connection.cursor()
        query = "INSERT INTO learn_photo (file_id, file_name, user_id, model_title) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, (file_id, file_name, user_id, model_title))

        self.database_connection.commit()
        print('Photo for learn added in DB successfully!')

        cursor.close()

    def get_user_photo_file_names(self, model_title):
        self.database_connection.reconnect()

        cursor = self.database_connection.cursor()
        query = "SELECT * FROM learn_photo WHERE model_title = %s"

        cursor.execute(query, (model_title,))

        images = cursor.fetchall()
        image_names = [image[2] for image in images]

        cursor.close()

        print('Photo for model learn returned successfully!')
        return image_names


if __name__ == '__main__':
    learn_photo_db = LearnPhotoDB()
    learn_photo_db.get_user_photo_file_names('uuid')