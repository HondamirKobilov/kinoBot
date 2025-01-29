from datetime import datetime
import pytz
from environs import Env
from data.channels_manager import ChannelsManager
env = Env()
env.read_env()

BOT_TOKEN1 = env.str("BOT_TOKEN1")
BOT_TOKEN2 = env.str("BOT_TOKEN2")
ADMINS = env.list("ADMINS")
USERNAME_START = env.str("USERNAME_START")


DB_USER = "postgres"
DB_PASS = "123"
DB_HOST = "localhost"
DB_NAME = "kinoBot"

channels_manager = ChannelsManager()

uzbekistan_timezone = pytz.timezone("Asia/Tashkent")

months_uz = {
    1: "yanvar", 2: "fevral", 3: "mart", 4: "aprel",
    5: "may", 6: "iyun", 7: "iyul", 8: "avgust",
    9: "sentabr", 10: "oktabr", 11: "noyabr", 12: "dekabr"
}
def toshkent_now() -> datetime:
    toshkent_zone = pytz.timezone('Asia/Tashkent')
    return datetime.now(toshkent_zone).replace(tzinfo=None)
private_channel = "-1002479702033"
asosiy_bot = "https://t.me/Kinolar_olami_09_bot"
yordamchi_bot = "https://t.me/itpark123245bot?start="
asosiy_channel = "@Kinolar_olami_09"
kino_kodKey = 'olma'