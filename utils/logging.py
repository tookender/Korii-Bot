from discord.flags import BaseFlags, fill_with_flags, flag_value

@fill_with_flags()
class LoggingEventsFlags(BaseFlags):
    def __init__(self, permissions: int = 0, **kwargs: bool):
        super().__init__(**kwargs)
        if not isinstance(permissions, int):
            raise TypeError(f"Expected int parameter, received {permissions.__class__.__name__} instead.")
        self.value = permissions
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f"{key!r} is not a valid permission name.")
            setattr(self, key, value)

    @classmethod
    def all(cls):
        bits = max(cls.VALID_FLAGS.values()).bit_length()
        value = (1 << bits) - 1
        self = cls.__new__(cls)
        self.value = value
        return self

    @classmethod
    def message(cls):
        return cls(0b000000000000000000000000000111)

    @classmethod
    def join_leave(cls):
        return cls(0b000000000000000000011000011000)

    @classmethod
    def member(cls):
        return cls(0b000000000000000000000111100000)

    @classmethod
    def voice(cls):
        return cls(0b000000110000000111100000000000)

    @classmethod
    def server(cls):
        return cls(0b111111111111111000000000000000)

    @flag_value
    def message_delete(self):
        return 1 << 0

    @flag_value
    def message_purge(self):
        return 1 << 1

    @flag_value
    def message_edit(self):
        return 1 << 2

    @flag_value
    def member_join(self):
        return 1 << 3

    @flag_value
    def member_leave(self):
        return 1 << 4

    @flag_value
    def member_update(self):
        return 1 << 5

    @flag_value
    def user_ban(self):
        return 1 << 6

    @flag_value
    def user_unban(self):
        return 1 << 7

    @flag_value
    def user_update(self):
        return 1 << 8

    @flag_value
    def invite_create(self):
        return 1 << 9

    @flag_value
    def invite_delete(self):
        return 1 << 10

    @flag_value
    def voice_join(self):
        return 1 << 11

    @flag_value
    def voice_leave(self):
        return 1 << 12

    @flag_value
    def voice_move(self):
        return 1 << 13

    @flag_value
    def voice_mod(self):
        return 1 << 14

    @flag_value
    def emoji_create(self):
        return 1 << 15

    @flag_value
    def emoji_delete(self):
        return 1 << 16

    @flag_value
    def emoji_update(self):
        return 1 << 17

    @flag_value
    def sticker_create(self):
        return 1 << 18

    @flag_value
    def sticker_delete(self):
        return 1 << 19

    @flag_value
    def sticker_update(self):
        return 1 << 20

    @flag_value
    def server_update(self):
        return 1 << 21

    @flag_value
    def stage_open(self):
        return 1 << 22

    @flag_value
    def stage_close(self):
        return 1 << 23

    @flag_value
    def channel_create(self):
        return 1 << 24

    @flag_value
    def channel_delete(self):
        return 1 << 25

    @flag_value
    def channel_edit(self):
        return 1 << 26

    @flag_value
    def role_create(self):
        return 1 << 27

    @flag_value
    def role_delete(self):
        return 1 << 28

    @flag_value
    def role_edit(self):
        return 1 << 29
