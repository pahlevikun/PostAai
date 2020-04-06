from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline
from datetime import datetime
from time import sleep

# To obtain API Keys, you have to visit https://my.telegram.org/apps, and make an app.
API_ID = 0  # ENTER YOU API ID HERE (SHOUlD BE AN INT)
API_HASH = '<ENTER YOUR API HASH HERE>'

USERNAMES = [
    # enter all username you wish to track here
    # like 'aswin_shenoy'
]

PAIRS = [
    # enter pair of usernames you wish to track together here
    # they must be also part of usernames in order to be tracked
    # like ('aswinshenoy', 'aswin_shenoy')
]

# Sleep time before each instance of tracking
# if sleep time is too low, a 24hr lock with telethon.errors.rpcerrorlist.FloodWaitError will be hit
# ^ @todo fix this
TRACK_FREQUENCY = 15

client = TelegramClient('bot', API_ID, API_HASH)


async def main():
    while True:
        online = []
        offline = []

        # loop through each username provided, and get their current status
        for i in USERNAMES:
            entity = await client.get_entity(i)
            name = entity.first_name + ' ' + entity.last_name
            if isinstance(entity.status, UserStatusOnline):
                # print if user tracked is online
                print('[' + datetime.now().isoformat() + ']: ' + name + ' is online')
                online.append(entity.username)
            else:
                offline.append(entity.username)

        # loop through each pair of username given
        for u in PAIRS:
            # check if both users in the given pair are online right now
            if u[0] in online and u[1] in online:
                print('[' + datetime.now().isoformat() + ']: ' + u[0] + ' & ' + u[1] + ' are both online right now')
            elif u[0] in offline and u[1] in offline:
                print('[' + datetime.now().isoformat() + ']: ' + u[0] + ' & ' + u[1] + ' are both offline right now')

        # sleep until provided seconds
        sleep(TRACK_FREQUENCY)

if __name__ == "__main__":
    print("Tracker Started")
    client.start()
    print("Tracker successfully connected to Telegram.")
    with client:
        client.loop.run_until_complete(main())
