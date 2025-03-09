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

    def get_user_models(self, user_id):
        try:
            self.database_connection.reconnect()

            cursor = self.database_connection.cursor()
            query = "SELECT * FROM models WHERE user_id = %s AND tuned = 1"

            cursor.execute(query, (user_id,))

            models = cursor.fetchall()

            cursor.close()

            print('User models returned successfully!')
            return models
        except Exception as e:
            print("Error", e)
            return []
        finally:
            cursor.close()

    def get_model(self, user_id, model_id):
        try:
            self.database_connection.reconnect()

            cursor = self.database_connection.cursor()
            query = "SELECT * FROM models WHERE user_id = %s AND model_id = %s"

            cursor.execute(query, (user_id, model_id))

            model = cursor.fetchall()

            cursor.close()

            print('Model returned successfully!')
            return model[0]
        except Exception as e:
            print("Error", e)
            return None
        finally:
            cursor.close()


if __name__ == '__main__':
    model_db = ModelDB()
    print(model_db.get_user_models(7047174818))
