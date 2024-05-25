from typing import Union

from discord.ext import commands

from bot import Korii


class BalanceConverter(commands.Converter):
    async def convert(self, ctx, argument) -> int:
        if argument.lower() == "all":
            number = await get_balance(ctx.bot, ctx.author.id)

            if number < 0:
                raise commands.BadArgument(f"'{argument}' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{argument}' is too low. Please provide a number more than 0.")

            return number
        elif argument.lower() == "half":
            number = int(await get_balance(ctx.bot, ctx.author.id) / 2)

            if number < 0:
                raise commands.BadArgument(f"'{number} ({argument})' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{number} ({argument})' is too low. Please provide a number more than 0.")

            return number

        try:
            number = int(argument)

            if number < 0:
                raise commands.BadArgument(f"'{number} ({argument})' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{number} ({argument})' is too low. Please provide a number more than 0.")

            return number

        except ValueError:
            raise commands.BadArgument(f"'{argument}' is not a valid input. Please provide 'all', 'half', or a number.")


class BankConverter(commands.Converter):
    async def convert(self, ctx, argument) -> int:
        if argument.lower() == "all":
            number = await get_bank(ctx.bot, ctx.author.id)
            
            if number < 0:
                raise commands.BadArgument(f"'{number} ({argument})' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{number} ({argument})' is too low. Please provide a number more than 0.")

            return number
        
        elif argument.lower() == "half":
            number = int(await get_bank(ctx.bot, ctx.author.id) / 2)

            if number < 0:
                raise commands.BadArgument(f"'{number} ({argument})' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{number} ({argument})' is too low. Please provide a number more than 0.")

            return number

        try:
            number = int(argument)

            if number < 0:
                raise commands.BadArgument(f"'{argument}' is a negative number. Please provide a positive number.")

            if number == 0:
                raise commands.BadArgument(f"'{argument}' is too low. Please provide a number more than 0.")

            return number
        
        except ValueError:
            raise commands.BadArgument(f"'{argument}' is not a valid input. Please provide 'all', 'half', or a number.")


class RouletteConverter(commands.Converter):
    async def convert(self, ctx, argument) -> str:
        # VALID INPUTS: COLORS: red, black, green
        # VALID INPUTS: NUMBERS: 00, all numbers from 0-36

        if argument.isnumeric():
            if int(argument) > 36:
                raise commands.BadArgument(f"'{argument}' is too high. Please provide a number less than or equal to 36.")

            if int(argument) < 0 and argument != "00":
                raise commands.BadArgument(f"'{argument}' is too low. Please provide a number more than or equal to 0 or 00.")

            if argument == "00" or int(argument) == 0:
                correct_color = "green"
            elif int(argument) % 2 == 0:
                correct_color = "red"
            else:
                correct_color = "black"

            return correct_color

        elif argument.lower() in ["red", "black", "green"]:
            return argument.lower()

        else:
            raise commands.BadArgument(f"'{argument}' is not a valid input. Please provide a number between 0-36, or 00.")


numbers = Union[int, BalanceConverter, BankConverter]


async def create_account(bot: Korii, user: int):
    return await bot.pool.execute("INSERT INTO economy(user_id, balance, bank) VALUES ($1, $2, $3)", user, 100, 1)


async def has_account(bot: Korii, user: int):
    data = await bot.pool.fetch("SELECT * FROM economy WHERE user_id = $1", user)

    if data:
        return True
    return False


async def get_balance(bot: Korii, user: int):
    balance = await bot.pool.fetchval("SELECT balance FROM economy WHERE user_id = $1", user)

    return balance


async def get_bank(bot: Korii, user: int):
    bank = await bot.pool.fetchval("SELECT bank FROM economy WHERE user_id = $1", user)

    return bank


async def add_money(bot: Korii, user: int, amount: numbers):
    return await bot.pool.execute("UPDATE economy SET balance = balance + $1 WHERE user_id = $2", amount, user)


async def remove_money(bot: Korii, user: int, amount: numbers):
    return await bot.pool.execute("UPDATE economy SET balance = balance - $1 WHERE user_id = $2", amount, user)


async def add_bank(bot: Korii, user: int, amount: numbers):
    return await bot.pool.execute("UPDATE economy SET bank = bank + $1 WHERE user_id = $2", amount, user)


async def remove_bank(bot: Korii, user: int, amount: numbers):
    return await bot.pool.execute("UPDATE economy SET bank = bank - $1 WHERE user_id = $2", amount, user)


async def has_enough_money(bot: Korii, user: int, amount: numbers):
    balance = await get_balance(bot, user)

    if amount > balance:
        return False
    return True


async def has_enough_bank(bot: Korii, user: int, amount: numbers):
    bank = await get_bank(bot, user)

    if amount > bank:
        return False
    return True
