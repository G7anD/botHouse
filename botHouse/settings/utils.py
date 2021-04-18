import requests
import json, os, django, sys
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher


class Initializer:
    def __init__(self, token, channel):
        path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        sys.path.append(path_dir)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
        django.setup()

        self.TOKEN = token
        self.CHANNEL = channel


    def run_bot(self):
        """ init bot """

        bot = Bot(token=self.TOKEN)
        dp = Dispatcher(bot)

        return (bot, dp)


    def is_member(self, user_id):
        """ check user is member of channel """

        url = f"https://api.telegram.org/bot{self.TOKEN}/getChatMember?"\
                            f"chat_id={self.CHANNEL_ID}&user_id={user_id}"

        response = requests.get(url)
        is_member = json.loads(response.text)

        if is_member['ok']:
            return is_member['result']['status'] in ['creator', 'administrator', 'member']
        else:
            return False


    @sync_to_async
    def register(user, Model):
        try:
            Model(user_id=user.id, firstname=user.first_name,
                    lastname=user.last_name, username=user.username).save()
        except Model.DoesNotExist:
            pass
