p = require('sys').puts
jcrawler = require './jcrawler'

class exports.MixiCrawler extends jcrawler.JCrawler
  success: ($) ->
    console.log "contents of corp mission", $("#corp-mission").text()
