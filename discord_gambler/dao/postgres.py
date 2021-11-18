import psycopg2 as db
from decouple import config
import logging

logging.basicConfig(level=logging.INFO)


class PostgresDAO:
    def __init__(self):
        self.conn = db.connect(config("postgres"))
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()
        logging.info("Connection closed")

    def commit(self):
        self.conn.commit()


if __name__ == "__main__":
    testconn = PostgresDAO()

    # execute a statement
    logging.info("PostgreSQL database version:")
    testconn.cur.execute("SELECT version()")

    # display the PostgreSQL database server version
    db_version = testconn.cur.fetchone()
    logging.info(db_version)
    testconn.close()
