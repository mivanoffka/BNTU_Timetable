from queue import Queue

bot = None
dp = None

schedule = {}
users_and_groups = {}
waiting_for_group_num = []

exit_event = False
