import logging
from datetime import time, datetime


class DataCollector:
    stats: dict
    recent_users: list
    reset_time: str

    def __init__(self):
        self.reset()

    def update_stats(self, key: str, user_id: str):
        user_id = str(user_id)
        self.stats[key] += 1
        logging.info("User {} commited '{}' action ({} in total)".format(user_id, key, self.stats[key]))
        if user_id not in self.recent_users:
            self.recent_users.append(user_id)
            logging.info(self.recent_users)
            logging.info("User {} commited his first action in this session ({} in total)".format(
                user_id, len(self.recent_users)))

    def reset(self):
        self.reset_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        stats_keys = ("today", "tomorrow", "weekday", "start", "report", "options", "donate", "dailymail")
        self.stats = dict.fromkeys(stats_keys, 0)
        self.recent_users = []

