import ClippingBot


class BotManager:
    def __init__(self):
        self.active_bots = []
        self.watching_channels = []

    def create_bot(self, channel: str):
        bot = ClippingBot.Bot(channel)
        self.bots.append(bot)
        return bot
    
