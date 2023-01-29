import tomli

with open("config.toml", "rb") as file:
    config = tomli.load(file)

BOT_TOKEN = config["bot"]["settings"]["token"]
DATABASE = config["bot"]["settings"]["database"]
