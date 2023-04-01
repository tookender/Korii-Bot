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

DROP TABLE IF EXISTS levels;
DROP TABLE IF EXISTS guilds;
DROP TABLE IF EXISTS role_rewards;

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

CREATE TABLE IF NOT EXISTS guilds (
    guild_id               BIGINT  PRIMARY KEY,
    levelling_enabled      BOOLEAN DEFAULT FALSE,
    levelling_announce     BOOLEAN DEFAULT TRUE,
    levelling_channel      BIGINT,
    levelling_message      TEXT DEFAULT '**GG**, **{user}** has reached level **{level}**!',
    levelling_double_xp    BOOLEAN DEFAULT FALSE,
    levelling_delete_after INT DEFAULT NULL
);