# NPM

NPM is a packet manager for js projects.

## Install (NPM and NodeJs)

Download and install from https://www.npmjs.com/get-npm (add NPM to path if using windows)

## Initialize a project

Execute `npm init` in root of your project (It will create a `package.json`)

You could also create a `package.json` file following this standard:
```
{
  "name": "PROJECT_NAME_HERE",
  "version": "1.0.0",
  "description": "DESCRIPTION_HERE",
  "repository": {
    "type": "git",
    "url": "https://github.com/QuentinCG/REPO_HERE.git"
  },
  "bugs": {
    "url": "https://github.com/QuentinCG/REPO_HERE/issues"
  },
  "homepage": "https://github.com/QuentinCG/REPO_HERE",
  "author": "Quentin Comte-Gaz",
  "license": "MIT",
  "main": "index.js",
  "dependencies": {
  },
  "scripts": {
    "start": "npm run dev",
    "dev": "webpack --mode development --watch",
    "prod": "webpack --mode production --watch",
    "build": "webpack --mode production",
    "ANYTHING_HERE": "CMD_TO_EXECUTE_HERE_WHEN 'npm run ANYTHING_HERE' IS_USED_FROM_CMD"
  },
  "devDependencies": {
    "nodemon": "*",
    "webpack": "^4.30.0",
    "webpack-cli": "^3.3.1",
    "webpack-dev-server": "^3.7.2"
  },
}
```

## Add/Update dependencies to a project

`npm install` (with some potential parameters) will update `package.json` and add the lib in `node_modules` folder)

- Use `npm install --save DEPENDENCY_HERE` (or `DEPENDENCY_HERE`) to save the dependency in the project
- Use `npm install --save-dev DEPENDENCY_HERE` to save the dev dependency in the project
- Use `npm install --global DEPENDENCY_HERE` to install the package in your computer (for all projects but not stored in the `package.json` project file)
- Use `npm install` to update the `node_modules` folder (will install dependencies and devDependencies)
- Use `npm install --production` to update the `node_modules` folder (will install dependencies without devDependencies)


# Useful NPM packages

## Nodemon (restarts node app when file change detected)

- Install: `npm install --save-dev nodemon`
- <a target="_blank" href="https://github.com/remy/nodemon#usage">Usage</a>: `nodemon [node app here]`

## Webpack (Bundling and Packaging ressources and assets)

- Install: `npm install --save-dev webpack webpack-cli webpack-dev-server` (+ <a target="_blank" href="https://webpack.js.org/configuration/">configure a `webpack.config.js` file manually or with `npx webpack-cli init` command</a>)
- <a target="_blank" href="https://www.npmjs.com/package/webpack">Tools linked to webpack</a>; css-loader, sass, typescript, ...
- <a target="_blank" href="https://webpack.js.org/guides/getting-started/">Getting started</a>

## Axios (Do request to HTTP client/API)

- Install: `npm install axios`
- <a target="_blank" href="https://github.com/axios/axios#example">Usage</a>:
```
const httpRequest = require('axios');
 
// Make a request for a user with a given ID
httpRequest.get('/user?ID=12345')
  .then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
```

## Mongoose (Communicate with a MongoDB database)

- Install: `npm install mongoose`
- <a target="_blank" href="https://mongoosejs.com/docs/index.html">Usage</a>:
```
const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/test', {useNewUrlParser: true});

const Cat = mongoose.model('Cat', { name: String });

const kitty = new Cat({ name: 'Zildjian' });
kitty.save().then(() => console.log('meow'));
```
- Additional information: Create a free 512MB MongoDB cluster from https://www.mongodb.com/ (Try Free -> Choose cluster -> Create a DB user with read/write access -> Whitelist all IP if in dev mode, else only your server IP -> Get link to connect to your app with pass of the DB user)
