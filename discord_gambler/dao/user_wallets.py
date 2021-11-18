from .postgres import PostgresDAO
import logging

logging.basicConfig(level=logging.INFO)


class UserWalletsDAO(PostgresDAO):
    def __init__(self):
        super(UserWalletsDAO, self).__init__()

    def get_wallet(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if self.cur.rowcount == 0:
            return None
        else:
            return self.cur.fetchone()

    def get_all_wallets(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def update_wallet(self, user_id, balance):
        if self.get_wallet(user_id):
            self.cur.execute(
                "UPDATE users SET wallet = wallet + %s WHERE user_id = %s",
                (balance, user_id),
            )
        else:
            self.cur.execute("INSERT INTO users VALUES (%s, %s)", (user_id, balance))

        self.conn.commit()


if __name__ == "__main__":
    testconn = UserWalletsDAO()

    # execute a statement
    logging.info("PostgreSQL database version:")
    testconn.cur.execute("SELECT version()")

    # display the PostgreSQL database server version
    db_version = testconn.cur.fetchone()
    logging.info(db_version)
    testconn.close()
