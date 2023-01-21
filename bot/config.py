import tomli

with open("config.toml", "rb") as file:
    config = tomli.load(file)

BOT_TOKEN = config["bot"]["settings"]["token"]
EXTENSIONS = config["bot"]["settings"]["extensions"]
DATABASE = config["bot"]["settings"]["database"]
