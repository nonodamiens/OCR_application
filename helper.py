import sqlite3
import traceback

DB_PATH = './OCR.db'   # Update this path accordingly


def add_to_list(url, text):

    try:
        conn = sqlite3.connect(DB_PATH)

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()
        # print (text)
        # Keep the initial status as Not Started
        res = c.execute("SELECT MAX(id) FROM RESULTS")
        id = res.fetchone()[0]
        id += 1
        print(id)
        c.execute("insert into RESULTS values ('{id}', '{url}', '{value}');".format(id = id, url = url, value = text))

        # We commit to save the change
        conn.commit()
        return {"texte": text}
    except Exception as e:
        # print('Error: ', e)
        print(traceback.format_exc())
        return None