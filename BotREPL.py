import BotManager
import Utils as utils


BM = BotManager.BotManager()

callbackurl = input("Input ngrok callback URL:")
utils.set_callback_url(callbackurl)

while True:
    try:
        user_input = input(">>> ")
        if user_input == "exit":
            utils.save_user_ids(BM.watching_channels)
            print("Goodbye!")
            break
        
        args = user_input.split()
        arglen = len(args)
        if arglen == 0:
            continue

        command = args[0]

        match user_input:
            case "add":
                if arglen < 2:
                    print("Invalid args")
                    continue
                username = args[1]
                if BM.create_bot(username):
                    print(f"Bot for {username} created.")
                else:
                    print(f"Bot creation failed for {username}.")
                break

            case "remove":
                if arglen < 2:
                    print("Invalid args")
                    continue
                username = args[1]
                if BM.remove_bot(username):
                    print(f"Bot for {username} removed.")
                else:
                    print(f"Bot removal failed for {username}.")
                break

            case "list":
                print("---------------CURRENTLY LIVE BOTS---------------")
                for bot in BM.active_bots:
                    print(bot.chanel)

                print("---------------WATCHING CHANNELS---------------")
                for channel in BM.watching_channels:
                    print(channel)
                break
            case "":
                continue
            case _:
                print("Invalid command")
                continue

    except Exception as e:
        print(e)
        continue