# grillporn

## Device setup
```
...
```

## Heroku Deploy
```
heroku git:remote -a <app_name>
heroku config:set NPM_CONFIG_PRODUCTION=false --app <app_name>
heroku buildpacks:add heroku/nodejs --app <app_name>
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-static.git --app <app_name>
git push heroku master
```