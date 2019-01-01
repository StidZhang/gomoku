# API

## Auth

| method | path              | comment |
| ------ | ----------------- | ------- |
| GET    | /api/login        |         |
| POST   | /api/login        |         |
| POST   | /api/logout       |         |
| POST   | /api/register     |         |
| POST   | /api/changepasswd |         |

Cookie: token

## Game

| method | path                | comment |
| ------ | ------------------- | ------- |
| GET    | /api/gomoku/history |         |
| POST   | /api/gomoku/create  |         |
| POST   | /api/gomoku/join    |         |

websocket:

# CSS

<https://github.com/vueComponent/ant-design-vue>

# Backend

## Game logic

..

## User logic

..

# Frontend

## Component

Board ..

User ..

# Route

## /

## /history

## /gomoku

# Database

## User

| field    | type     |
| -------- | -------- |
| username | text     |
| password | text     |
| created  | datetime |

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

-   1 - Host
-   2 - Guest
-   3 - Host won
-   4 - Guest won

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
