r = require 'restler'
fs = require 'fs'
path = require 'path'
jsdom = require 'jsdom'
p = require('sys').puts

jquery_path = path.join __dirname, 'jquery-1.6.4.js'
jquery = fs.readFileSync(jquery_path).toString()

class exports.JCrawler
  constructor: (@options = {}) ->

  success: ($) ->
    p "Success! Override this function"

  error: (res) ->
    p "Error! #{res.statusCode}"

  get: (url) ->
    self = @
    r.get(url, @options)
      .on 'success', (html, res) ->
        jsdom.env
          html: html
          src: jquery
          done: (errors, window) -> self.success window.$
      .on 'error', (html, res) -> self.error res
