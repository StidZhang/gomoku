# gomoku

A prototype version of online multiplayer [Gomoku](https://en.wikipedia.org/wiki/Gomoku) web application based on [Vue.js](https://vuejs.org/),  [Flask](http://flask.pocoo.org/) and [MongoDB](https://www.mongodb.com/), running live on [Heroku](https://www.heroku.com/).

## [Live Demo](https://vue-gomoku.herokuapp.com)

## Project setup

Requirements:
* Python >= 3.6
* Node.js >= 8.0

```
git clone https://github.com/StidZhang/gomoku.git
cd gomoku
npm install
pip install -r requirements.txt
```

### Run in local environment
Need to install MongoDB >= 4.0, then run `npm run serve` and `flask run` separately
under `gomoku` folder. Project set to be running at http://localhost:8080 on default.

### Run on Heroku
1. Connect the repo to your Heroku app.
2. Add both `Python` and `Node.js` in your __Buildpacks__ under __Settings__.
3. If you don't have a MongoDB to connect to, add __mLab MongoDB__ Add-on in Heroku Resources. Then add the MongoDB URI into `MONGODB_URI` in __Config Vars__ under __Settings__.
4. Add a random string into `SECRET_KEY` in __Config Vars__ under __Settings__ for Flask security reason.

## Future plan

- Player matching and ranking system
- Swap2 rule implementation
- Historical match replay and view live match as audience
- Live chat
- Add bots trained by different machine learning model

## Author

[Stid Zhang](https://github.com/StidZhang)

[Yang Gao](https://github.com/criyle)

## LICENSE

[MIT](./LICENSE)
