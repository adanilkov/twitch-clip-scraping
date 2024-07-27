import ClippingBot
import StreamListener
from typing import List
import Utils as utils


class BotManager:
    def __init__(self):
        self.active_bots: List[ClippingBot.Bot] = []
        self.watching_channels: List[str] = []

    def create_bot(self, channel: str):
        for bot in self.active_bots:
            if bot.chanel == channel:
                return None
        try:
            bot = ClippingBot.Bot(channel)
            StreamListener.subscribe_to_stream_online(utils.streamer_to_id(channel), utils.get_callback_url())
            self.active_bots.append(bot)
            return bot
        except Exception as e:
            print(e)
            return None
    
    def remove_bot(self, channel: str):
        for bot in self.active_bots:
            if bot.chanel == channel:
                self.active_bots.remove(bot)
                return bot
        return None
    
