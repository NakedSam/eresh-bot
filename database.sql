/*
-----------------------------------------------------------------------
|    Creates the necessary database and tables for the bot    |
-----------------------------------------------------------------------
*/

CREATE DATABASE IF NOT EXISTS `er_blindtest`;
CREATE DATABASE IF NOT EXISTS `er_news`;
CREATE DATABASE IF NOT EXISTS `er_servers`;

USE `er_blindtest`;

CREATE TABLE IF NOT EXISTS `er_bt_users`
(
    id_user INT NOT NULL AUTO_INCREMENT,
    `user_name` VARCHAR(255) NOT NULL,
    user_blindtestCount INT NOT NULL DEFAULT 0,
    user_blindtestPoints INT NOT NULL DEFAULT 0,
    user_addedDate DATETIME NOT NULL DEFAULT NOW(),

    PRIMARY KEY(id_user)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `er_bt_logs`
(
    id_bt INT NOT NULL AUTO_INCREMENT,
    bt_player INT NOT NULL,
    bt_blindtestNumber INT NOT NULL DEFAULT 0,
    bt_playerScore INT NOT NULL,
    bt_type VARCHAR(50),
    bt_playerResponseTimes TEXT,
    bt_server VARCHAR(255) NOT NULL,

    PRIMARY KEY(id_bt),
    FOREIGN KEY(bt_player) REFERENCES `er_bt_users`(`id_user`)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `er_bt_songs`
(
    id_song INT NOT NULL AUTO_INCREMENT,
    song_title TEXT NOT NULL,
    song_filename TEXT NOT NULL,
    song_aliases TEXT,
    song_oped VARCHAR(15),
    song_addedDate DATETIME,
    song_insertDate DATETIME DEFAULT NOW(),
    song_contributor VARCHAR(255),
    song_lastModification DATETIME,

    PRIMARY KEY(id_song)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `er_news`;

CREATE TABLE IF NOT EXISTS `er_news`
(
    id_new INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    new_title TEXT NOT NULL,
    new_link TEXT NOT NULL,
    new_source TEXT NOT NULL,
    new_date DATETIME NOT NULL DEFAULT NOW()
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `er_servers`;

CREATE TABLE IF NOT EXISTS `er_servers_table`
(
    id_server INT NOT NULL AUTO_INCREMENT,
    server_id INT UNIQUE NOT NULL,
    server_name VARCHAR(255) NOT NULL,
    server_btChannel VARCHAR(255),
    server_newsChannel VARCHAR(255),
    server_usesNews BOOLEAN DEFAULT 0,
    server_usesBlindtest BOOLEAN DEFAULT 0,

    PRIMARY KEY(id_server)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
