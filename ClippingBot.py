from twitchio.ext import commands
import time
import datetime as dt
from collections import deque
import numpy as np
import Utils as utils

class Bot(commands.Bot):

    def __init__(self, chanel):
        super().__init__(token=utils.get_token(), prefix='?', initial_channels=[chanel])
        self.token = utils.get_token()
        self.client_id = utils.get_client_id()
        self.message_times = deque(maxlen=1000)  # Store timestamps of the last 1000 messages
        self.message_counts = deque(maxlen=100)  # Store message counts for each time window
        self.window_size = 20  # Window size in seconds
        self.chanel = chanel
        self.lastloop = None


    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)

        # Record the time of the message
        current_time = time.time()
        self.message_times.append(current_time)

        if self.lastloop is None or time.time() - self.lastloop > self.window_size:
                print('---------------Inside----------------')
                self.lastloop = time.time()
                # number of messages in the last window_size seconds
                window_messages_count = len([msg_time for msg_time in self.message_times if time.time() - msg_time < self.window_size])
                # calculate the mean and standard deviation of the message counts
                if len(self.message_counts) < 15:
                    mean = np.mean(self.message_counts)
                    std_dev = np.std(self.message_counts)
                    if mean + 2.5 * std_dev < window_messages_count:
                        for i in range(4):
                            print('[------------Creating Clip------------]')
                        clip_id, edit_url = utils.create_clip(utils.streamer_to_id(self.chanel))
                        # Save clip_id and clip_url to a file
                        with open('clips.txt', 'a') as f:
                            f.write(f'[{dt.now()}] {clip_id}, {edit_url}\n')
            
                self.message_counts.append(window_messages_count)


            
            


bot = Bot('ohnepixel')
bot.run()
