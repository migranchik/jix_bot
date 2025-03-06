import mysql.connector


class ModelDB:
    def __init__(self):
        self.database_connection = mysql.connector.connect(host='localhost', user='root', password='Ilyas2006#', database='jix_bot')

    def create_model(self, user_id, model_name, model_id, model_title):
        self.database_connection.reconnect()

        cursor = self.database_connection.cursor()
        query = "INSERT INTO models (user_id, model_name, model_id, model_title) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, (user_id, model_name, model_id, model_title))

        self.database_connection.commit()
        print('Model created in DB successfully!')

        cursor.close()

    def update_model_tuned_status(self, model_title):
        self.database_connection.reconnect()

        cursor = self.database_connection.cursor()
        query = "UPDATE models SET tuned = %s WHERE model_title = %s"

        cursor.execute(query, (1, model_title))

        self.database_connection.commit()
        print('Model tuned status in DB successfully!')

        cursor.close()


if __name__ == '__main__':
    model_db = ModelDB()
    model_db.update_model_tuned_status("da52ac1c-eeef-4841-890e-6f69a5fd7f0e")
