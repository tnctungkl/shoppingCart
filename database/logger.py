import socket
import json
from datetime import datetime
import psycopg2
import psycopg2.extras

class DBLogger:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.conn = None
        self._connect()
        print("Database Logger initialized!!!")
        self._create_table()

    def _connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(**self.db_config)

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            computer_name TEXT,
            timestamp TEXT,
            action TEXT,
            status TEXT,
            cart_state JSONB
        );
        """
        with self.conn, self.conn.cursor() as cur:
            cur.execute(query)

    def log_action(self, action: str, status: str, cart_state: dict):
        payload = json.dumps(cart_state, ensure_ascii=False)
        with self.conn, self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO logs (computer_name, timestamp, action, status, cart_state)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    socket.gethostname(),
                    datetime.now().strftime("%d/%m/%Y | %H:%M:%S"),
                    action,
                    status,
                    payload,
                ),
            )