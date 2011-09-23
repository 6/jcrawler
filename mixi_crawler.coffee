p = require('sys').puts
jcrawler = require './jcrawler'

get_corp_mission = ($) ->
  console.log "contents of corp mission", $("#corp-mission").text()

j = new jcrawler.JCrawler()
j.get 'http://www.google.com/intl/en/about/corporate/index.html', get_corp_mission
