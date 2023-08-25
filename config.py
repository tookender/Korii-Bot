
import tomllib

with open("./data/config.toml", "rb") as file:
    config = tomllib.load(file)

BOT_TOKEN = config["bot"]["settings"]["token"]
DATABASE = config["bot"]["settings"]["database"]
JEYY_API_TOKEN = config["bot"]["apis"]["jeyy_api_token"]