env = module.exports =
  node_env: process.env.NODE_ENV || 'development'
  port: parseInt(process.env.PORT) || 8000

env.development = env.node_env == 'development'
env.production = !env.development

if env.development
  env.hostname = 'http://localhost:' + env.port
  env.secrets = require './secrets'

else
  env.hostname = 'http://jcrawl.herokuapp.com'
  env.secrets =
    mixi_user:
      login: process.env.MIXI_LOGIN
      password: process.env.MIXI_PASSWORD
