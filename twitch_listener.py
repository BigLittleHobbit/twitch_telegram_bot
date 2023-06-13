from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.eventsub import EventSub
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import asyncio

TARGET_USERNAME = 'BlackUFA'
EVENTSUB_URL = 'https://localhost'
APP_ID = 'f8s7cb4xx1pn6a0d3e399eiwpjuw93'
APP_SECRET = '5fzrtd4u684i0k1hyjddm5r0o1sw7x'
TARGET_SCOPES = [AuthScope.USER_READ_BROADCAST, AuthScope.USER_READ_FOLLOWS]

async def on_follow(data: dict):
    print(data)

async def eventsub_example():
    # create the API instance and get the ID of your target user
    twitch = await Twitch(APP_ID, APP_SECRET)
    user = await first(twitch.get_users(logins=TARGET_USERNAME))
    # the user has to authenticate once using the bot with our intended scope.
    # since we do not need the resulting token after this authentication, we just discard the result we get from authenticate()
    # Please read up the UserAuthenticator documentation to get a full view of how this process works
    auth = UserAuthenticator(twitch, TARGET_SCOPES)
    # basic setup, will run on port 8080 and a reverse proxy takes care of the https and certificate
    event_sub = EventSub(EVENTSUB_URL, APP_ID, 8080, twitch)
    # unsubscribe from all old events that might still be there. Надо будет попробовать убрать эту дичь.
    # this will ensure we have a clean slate
    await event_sub.unsubscribe_all()

    event_sub.start()

    await event_sub.listen_stream_online(user.id, on_follow)
    try:
        input("press Enter to shut down twitch listener...")
    finally:
         # stopping both eventsub as well as gracefully closing the connection to the API
        await event_sub.stop()
        await twitch.close()
    print('done')

if __name__=="__main__":
    # let's run our example
    asyncio.run(eventsub_example())