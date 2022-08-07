import logging
from sys import stdout

log = logging.getLogger("bot")
log.setLevel(logging.INFO)
fh = logging.FileHandler("bot.log", encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(logging.StreamHandler(stdout))