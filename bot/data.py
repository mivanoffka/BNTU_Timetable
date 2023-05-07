from queue import Queue

bot = None
dp = None

schedule = {}
users_and_groups = {}
waiting_for_group_num = []
waiting_for_sending_report = []
recently_sended_report = []

recent_users = []
interactions_count = {}

is_updating = False
exit_event = False
