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
  "main": "index.js",
  "repository": {
    "type": "git",
    "url": "https://github.com/QuentinCG/REPO_HERE.git"
  },
  "scripts": {
    "ANYTHING_HERE": "CMD_TO_EXECUTE_HERE_WHEN 'npm run ANYTHING_HERE' IS_USED_FROM_CMD"
  },
  "author": "Quentin Comte-Gaz",
  "license": "MIT",
  "dependencies": {
  },
  "devDependencies": {
    "nodemon": "*"
  },
  "bugs": {
    "url": "https://github.com/QuentinCG/REPO_HERE/issues"
  },
  "homepage": "https://github.com/QuentinCG/REPO_HERE"
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
- Usage: `nodemon [node app here]`

## Axios (Do request to HTTP client/API)

- Install: `npm install axios`
- Usage:
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
