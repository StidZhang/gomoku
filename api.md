# API

## Auth

| method | path              | comment |
| ------ | ----------------- | ------- |
| GET    | /api/login        |         |
| POST   | /api/login        |         |
| POST   | /api/logout       |         |
| POST   | /api/register     |         |
| POST   | /api/changepasswd |         |

## Gomoku

| method | path                | comment |
| ------ | ------------------- | ------- |
| GET    | /api/gomoku/history |         |

## SocketIO

| direction | event               | comment                      |
| --------- | ------------------- | ---------------------------- |
| c -> s    | connected           | check current_game / invite  |
| c -> s    | gomoku_create       | create a game                |
| c -> s    | gomoku_join         | join a game                  |
| c -> s    | gomoku_fail         | fail a game                  |
| c -> s    | gomoku_move         | a move                       |
| s -> c    | gomoku_status       | reply for connected          |
| s -> c    | gomoku_invite       | to another c for create game |
| s -> c    | gomoku_board        | to both for a join           |
| s -> c    | gomoku_board_update | to another c for move        |
| s -> c    | gomoku_end          | to both for game end / fail  |

gomoku_status may contains message to indicate a failure of a action.

# CSS

<https://github.com/vueComponent/ant-design-vue>

# Backend

## Game logic

..

## User logic

Flask-Login

# Frontend

## Component

Board ..

User ..

# Route

## Authentications

### /login

### /register

## In game

### /history

### /gomoku

# Database

## User

| field    | type     |
| -------- | -------- |
| username | text     |
| password | text     |
| created  | datetime |

## User_Gomoku

| field        | type   |
| ------------ | ------ |
| userid       | userid |
| current_game | gameid |
| total_won    | int    |
| total_game   | int    |

## Gomoku

| field      | type            |
| ---------- | --------------- |
| status     | int             |
| board      | board           |
| history    | list of history |
| game_host  | userid          |
| game_guest | userid          |
| config     | config          |

status(IntEnum):

-   1 - New
-   2 - Host
-   3 - Guest
-   4 - Host won
-   5 - Guest won
-   6 - Host Cancelled
-   7 - Guest Refused

# Data Model

## history

```json
{
  "user": "<userid>",
  "time": "<datetime>",
  "move": "<move>"
}
```

## move

## config

```json
{
  "size": "<int>",
  "rule": "<string>"
}
```

## board

```json
  ["length=size * size"]
```

# Folders

## /app

Flask backend

## /src

Vue frontend

## /dist

Vue compiled files

## /public

Vue static files
