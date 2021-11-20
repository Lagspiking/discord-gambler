from .postgres import PostgresDAO
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class CoinflipsDAO(PostgresDAO):
    def __init__(self):
        super(CoinflipsDAO, self).__init__()
        self._tax_rate = 0.2

    def get_open_coinflip(self, user_id: int):
        self.cur.execute(
            "SELECT created_id, staked_amount FROM coinflips WHERE created_id = %s and accepted_id is null",
            (user_id,),
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchone()
        return False

    def get_open_coinflips(self):
        self.cur.execute(
            "SELECT created_id, staked_amount FROM coinflips WHERE accepted_id is null order by created_at ASC"
        )
        if self.cur.rowcount != 0:
            return {x[0]: x[1] for x in self.cur.fetchall()}
        return False

    def get_recent_coinflips(self):
        self.cur.execute(
            "SELECT winning_id, staked_amount, losing_id FROM coinflips WHERE accepted_id is not null order by finished_at ASC limit 10"
        )
        if self.cur.rowcount != 0:
            return self.cur.fetchall()
        return False

    def get_won_games(self, user_id: int):
        self.cur.execute(
            "SELECT COUNT(*) FROM coinflips WHERE winning_id = %s",
            (user_id,),
        )
        return self.cur.fetchone()[0]

    def get_lost_games(self, user_id: int):
        self.cur.execute(
            "SELECT COUNT(*) FROM coinflips WHERE losing_id = %s",
            (user_id,),
        )
        return self.cur.fetchone()[0]

    def create_coinflip(self, user_id: int, stake: int):
        self.cur.execute(
            "INSERT INTO coinflips (created_id, staked_amount) VALUES (%s, %s)",
            (user_id, stake),
        )
        self.conn.commit()

    def remove_coinflip(self, user_id: int):
        self.cur.execute(
            "DELETE FROM coinflips WHERE created_id = %s and accepted_id is null",
            (user_id,),
        )
        self.conn.commit()

    def accept_coinflip(self, user_id: int, accepted_id: int):
        self.cur.execute(
            "UPDATE coinflips SET accepted_id = %s WHERE created_id = %s and finished_at is null",
            (accepted_id, user_id),
        )
        self.conn.commit()

    def finish_coinflip(
        self, user_id: int, accepted_id: int, winning_id: int, losing_id: int
    ):
        current_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.cur.execute(
            "UPDATE coinflips SET finished_at = %s, winning_id = %s, losing_id = %s WHERE created_id = %s AND accepted_id = %s and finished_at is null",
            (current_datetime, winning_id, losing_id, user_id, accepted_id),
        )
        self.conn.commit()
