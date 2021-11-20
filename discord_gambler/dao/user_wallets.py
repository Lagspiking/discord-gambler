from .postgres import PostgresDAO
import logging

logging.basicConfig(level=logging.INFO)


class UserWalletsDAO(PostgresDAO):
    def __init__(self):
        super(UserWalletsDAO, self).__init__()
        self._default_coins = 1000

    def get_wallet(self, user_id: int):
        self.cur.execute("SELECT wallet FROM users WHERE user_id = %s", (user_id,))
        if self.cur.rowcount != 0:
            return self.cur.fetchone()[0]
        else:
            self.cur.execute(
                "INSERT INTO users VALUES (%s, %s)",
                (user_id, self._default_coins),
            )
            self.commit()
            return self._default_coins

    def has_coins(self, user_id: int, balance: int):
        self.cur.execute("SELECT wallet FROM users WHERE user_id = %s", (user_id,))
        if self.cur.rowcount != 0:
            coins = self.cur.fetchone()[0]
            if coins >= balance:
                return True
            return False
        return False

    def get_top_wallets(self):
        self.cur.execute(
            "SELECT user_id, wallet FROM users ORDER BY wallet DESC limit 5"
        )
        return self.cur.fetchall()

    def update_wallet(self, user_id: int, balance: int):
        wallet = self.get_wallet(user_id)
        if wallet == 0:
            self.cur.execute(
                "UPDATE users SET wallet = %s WHERE user_id = %s",
                (balance, user_id),
            )
        elif wallet:
            self.cur.execute(
                "UPDATE users SET wallet = wallet + %s WHERE user_id = %s",
                (balance, user_id),
            )
            self.conn.commit()

    def set_wallet(self, user_id: int, balance: int):
        if self.get_wallet(user_id):
            self.cur.execute(
                "UPDATE users SET wallet = %s WHERE user_id = %s",
                (balance, user_id),
            )

        self.conn.commit()

    def update_wallets(self, users: list, balance: int):
        for user in users:
            self.update_wallet(user.id, balance)
        self.conn.commit()

    def transfer_coins(self, user_id: int, gifted_user_id: int, balance: int):
        if self.has_coins(user_id, balance):
            UserWalletsDAO().update_wallet(user_id, -balance)
            UserWalletsDAO().update_wallet(gifted_user_id, balance)
            return True
        return False
