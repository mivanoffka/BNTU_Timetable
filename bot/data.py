from queue import Queue

bot = None
dp = None

schedule = {}
users_and_groups = {}
waiting_for_group_num = []

interactions_count = {}

exit_event = False
