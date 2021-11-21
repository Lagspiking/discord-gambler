from .postgres import PostgresDAO
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class CoinflipsDAO(PostgresDAO):
    def __init__(self):
        super(CoinflipsDAO, self).__init__()
        self._tax_rate = 0.2

    def get_open_coinflip(self, _guild_id: int, user_id: int):
        self.cur.execute(
            "SELECT created_id, staked_amount FROM coinflips WHERE guild_id = %s AND created_id = %s and accepted_id is null",
            (
                _guild_id,
                user_id,
            ),
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchone()
        return False

    def get_open_coinflips(
        self,
        _guild_id: int,
    ):
        self.cur.execute(
            "SELECT created_id, staked_amount FROM coinflips WHERE guild_id = %s AND accepted_id is null order by created_at ASC",
            (_guild_id,),
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchall()
        return False

    def get_recent_coinflips(self, _guild_id: int):
        self.cur.execute(
            "SELECT winning_id, staked_amount, losing_id FROM coinflips WHERE guild_id = %s AND accepted_id is not null order by finished_at ASC limit 10",
            (_guild_id,),
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchall()
        return False

    def get_won_games(self, _guild_id: int, user_id: int):
        self.cur.execute(
            "SELECT COUNT(*) FROM coinflips WHERE guild_id = %s AND winning_id = %s",
            (
                _guild_id,
                user_id,
            ),
        )
        return self.cur.fetchone()[0]

    def get_lost_games(self, _guild_id: int, user_id: int):
        self.cur.execute(
            "SELECT COUNT(*) FROM coinflips WHERE guild_id = %s AND losing_id = %s",
            (
                _guild_id,
                user_id,
            ),
        )
        return self.cur.fetchone()[0]

    def create_coinflip(self, _guild_id: int, user_id: int, stake: int):
        self.cur.execute(
            "INSERT INTO coinflips (guild_id, created_id, staked_amount) VALUES (%s, %s, %s)",
            (_guild_id, user_id, stake),
        )
        self.conn.commit()

    def remove_coinflip(self, _guild_id: int, user_id: int):
        self.cur.execute(
            "DELETE FROM coinflips WHERE guild_id = %s AND created_id = %s and accepted_id is null",
            (
                _guild_id,
                user_id,
            ),
        )
        self.conn.commit()

    def accept_coinflip(self, _guild_id: int, user_id: int, accepted_id: int):
        self.cur.execute(
            "UPDATE coinflips SET accepted_id = %s WHERE guild_id = %s AND created_id = %s and finished_at is null",
            (accepted_id, _guild_id, user_id),
        )
        self.conn.commit()

    def finish_coinflip(
        self, _guild_id, user_id: int, accepted_id: int, winning_id: int, losing_id: int
    ):
        current_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.cur.execute(
            "UPDATE coinflips SET finished_at = %s, winning_id = %s, losing_id = %s WHERE guild_id = %s AND created_id = %s AND accepted_id = %s and finished_at is null",
            (current_datetime, winning_id, losing_id, _guild_id, user_id, accepted_id),
        )
        self.conn.commit()
