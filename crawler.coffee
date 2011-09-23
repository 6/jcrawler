r = require 'restler'
fs = require 'fs'
path = require 'path'
jsdom = require 'jsdom'
p = require('sys').puts

jquery_path = path.join __dirname, 'jquery-1.6.4.js'
jquery = fs.readFileSync(jquery_path).toString()

url = 'http://www.google.com/intl/en/about/corporate/index.html'

r.get(url).on 'complete', (html) ->
  p html
  jsdom.env
    html: html
    src: jquery
    done: (errors, window) ->
      console.log "contents of corp mission", window.$("#corp-mission").text()
