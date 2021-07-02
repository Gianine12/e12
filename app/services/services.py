import psycopg2

def connection():
    connect = psycopg2.connect(
        host="localhost",
        database="anime",
        user="gianine",
        password="12345"
    )

    cur = connect.cursor()

    return [connect, cur]

def close_connection(connect,cur):
    
    connect.commit()
    cur.close()
    connect.close()

def check_key(data, available_keys
):
    receive_keys = data.keys()
    return [
        campo 
        for campo in available_keys 
        if campo not in receive_keys
    ]