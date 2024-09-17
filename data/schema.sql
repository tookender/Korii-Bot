DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'blacklist_type') THEN
        CREATE TYPE blacklist_type AS ENUM ('user', 'guild');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'owo_type') THEN
        CREATE TYPE owo_type AS ENUM ('owo', 'uwu', 'qwq', ':3', '-w-');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS levels (
    guild_id BIGINT NOT NULL,
    user_id  BIGINT PRIMARY KEY,
    level    BIGINT NOT NULL,
    xp       BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS role_rewards (
    guild_id BIGINT NOT NULL,
    role_id  BIGINT PRIMARY KEY,
    level    BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS economy (
    user_id  BIGINT PRIMARY KEY,
    guild_id BIGINT,
    balance BIGINT,
    bank    BIGINT,
    job     TEXT,
    last_job_claim TIMESTAMP WITH TIME ZONE,

    last_daily TIMESTAMP WITH TIME ZONE,
    last_weekly TIMESTAMP WITH TIME ZONE,
    last_monthly TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS guilds (
    guild_id               BIGINT  PRIMARY KEY,
    levelling_enabled      BOOLEAN DEFAULT FALSE,
    levelling_announce     BOOLEAN DEFAULT TRUE,
    levelling_channel      BIGINT,
    levelling_message      TEXT    DEFAULT '**GG**, **{user}** has reached level **{level}**!',
    levelling_multiplier   FLOAT   DEFAULT 1.0,
    levelling_delete_after INT     DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS log_channels (
    guild_id BIGINT PRIMARY KEY,
    default_channel TEXT,
    default_chid BIGINT NOT NULL,
    message_channel TEXT,
    message_chid BIGINT,
    join_leave_channel TEXT,
    join_leave_chid BIGINT,
    member_channel TEXT,
    member_chid BIGINT,
    voice_channel TEXT,
    voice_chid BIGINT,
    server_channel TEXT,
    server_chid BIGINT,
    CONSTRAINT fk_log_channels_guild_id FOREIGN KEY (guild_id) REFERENCES guilds(guild_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logging_events (
    guild_id BIGINT PRIMARY KEY,
    message_delete BOOLEAN DEFAULT true NOT NULL,
    message_purge BOOLEAN DEFAULT true NOT NULL,
    message_edit BOOLEAN DEFAULT true NOT NULL,
    member_join BOOLEAN DEFAULT true NOT NULL,
    member_leave BOOLEAN DEFAULT true NOT NULL,
    member_update BOOLEAN DEFAULT true NOT NULL,
    user_ban BOOLEAN DEFAULT true NOT NULL,
    user_unban BOOLEAN DEFAULT true NOT NULL,
    user_update BOOLEAN DEFAULT true NOT NULL,
    invite_create BOOLEAN DEFAULT true NOT NULL,
    invite_delete BOOLEAN DEFAULT true NOT NULL,
    voice_join BOOLEAN DEFAULT true NOT NULL,
    voice_leave BOOLEAN DEFAULT true NOT NULL,
    voice_move BOOLEAN DEFAULT true NOT NULL,
    voice_mod BOOLEAN DEFAULT true NOT NULL,
    emoji_create BOOLEAN DEFAULT true NOT NULL,
    emoji_delete BOOLEAN DEFAULT true NOT NULL,
    emoji_update BOOLEAN DEFAULT true NOT NULL,
    sticker_create BOOLEAN DEFAULT true NOT NULL,
    sticker_delete BOOLEAN DEFAULT true NOT NULL,
    sticker_update BOOLEAN DEFAULT true NOT NULL,
    server_update BOOLEAN DEFAULT true NOT NULL,
    stage_open BOOLEAN DEFAULT true NOT NULL,
    stage_close BOOLEAN DEFAULT true NOT NULL,
    channel_create BOOLEAN DEFAULT true NOT NULL,
    channel_delete BOOLEAN DEFAULT true NOT NULL,
    channel_edit BOOLEAN DEFAULT true NOT NULL,
    role_create BOOLEAN DEFAULT true NOT NULL,
    role_delete BOOLEAN DEFAULT true NOT NULL,
    role_edit BOOLEAN DEFAULT true NOT NULL,
    CONSTRAINT fk_logging_events_guild_id FOREIGN KEY (guild_id) REFERENCES guilds(guild_id) ON DELETE CASCADE
);
