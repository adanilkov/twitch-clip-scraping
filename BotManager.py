import ClippingBot
import StreamListener
from typing import List
import Utils as utils


class BotManager:
    def __init__(self):
        self.active_bots: List[ClippingBot.Bot] = []
        self.watching_channels: List[str] = []

    def create_bot(self, channel: str, force: bool = False):
        if channel in self.watching_channels and not force:
            return None
        try:
            if channel not in self.watching_channels: StreamListener.subscribe_to_stream_online(utils.streamer_to_id(channel), utils.get_callback_url())
            if utils.check_stream_status(channel):
                bot = ClippingBot.Bot(channel)
                self.watching_channels.append(channel)
                self.active_bots.append(bot)
                bot.run()
                return bot
        except Exception as e:
            print(e)
            return None
    
    def remove_bot(self, channel: str):
        for bot in self.active_bots:
            if bot.chanel == channel:
                self.active_bots.remove(bot)
                bot.close()
                return bot
        return None
    
