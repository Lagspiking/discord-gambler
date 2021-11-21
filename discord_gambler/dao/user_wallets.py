from .postgres import PostgresDAO
import logging

logging.basicConfig(level=logging.INFO)


class UserWalletsDAO(PostgresDAO):
    def __init__(self):
        super(UserWalletsDAO, self).__init__()
        self._default_coins = 1000

    def get_wallet(self, guild_id: int, user_id: int):
        self.cur.execute(
            "SELECT wallet FROM users WHERE guild_id = %s and user_id = %s",
            (guild_id, user_id),
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchone()[0]
        else:
            self.cur.execute(
                "INSERT INTO users (guild_id, user_id, wallet) values (%s ,%s, %s)",
                (guild_id, user_id, self._default_coins),
            )
            self.commit()
            return self._default_coins

    def has_coins(self, guild_id: int, user_id: int, balance: int):
        self.cur.execute(
            "SELECT wallet FROM users WHERE guild_id = %s and user_id = %s",
            (
                guild_id,
                user_id,
            ),
        )
        if self.cur.rowcount != 0:
            coins = self.cur.fetchone()[0]
            if coins >= balance:
                return True
            return False
        return False

    def get_top_wallets(self, guild_id: int):
        self.cur.execute(
            "SELECT user_id, wallet FROM users WHERE guild_id = %s ORDER BY wallet DESC limit 5",
            (guild_id,),
        )
        return self.cur.fetchall()

    def update_wallet(self, guild_id: int, user_id: int, balance: int):
        wallet = self.get_wallet(guild_id, user_id)
        if wallet == 0:
            self.cur.execute(
                "UPDATE users SET wallet = %s WHERE guild_id = %s AND user_id = %s",
                (balance, guild_id, user_id),
            )
        elif wallet:
            self.cur.execute(
                "UPDATE users SET wallet = wallet + %s WHERE guild_id = %s AND user_id = %s",
                (balance, guild_id, user_id),
            )
            self.conn.commit()

    def set_wallet(self, guild_id: int, user_id: int, balance: int):
        if self.get_wallet(guild_id, user_id):
            self.cur.execute(
                "UPDATE users SET wallet = %s WHERE guild_id = %s AND user_id = %s",
                (balance, guild_id, user_id),
            )

        self.conn.commit()

    def update_wallets(self, guild_id: int, users: list, balance: int):
        for user in users:
            self.update_wallet(guild_id, user.id, balance)
        self.conn.commit()

    def transfer_coins(
        self, guild_id: int, user_id: int, gifted_user_id: int, balance: int
    ):
        if self.has_coins(guild_id, user_id, balance):
            UserWalletsDAO().update_wallet(guild_id, user_id, -balance)
            UserWalletsDAO().update_wallet(guild_id, gifted_user_id, balance)
            return True
        return False
