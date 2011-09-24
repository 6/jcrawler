r = require 'restler'
fs = require 'fs'
path = require 'path'
jsdom = require 'jsdom'
p = require('sys').puts

jquery_path = path.join __dirname, 'lib/jquery-1.6.4.js'
jquery = fs.readFileSync(jquery_path).toString()

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'

class exports.JCrawler
  constructor: (@options) ->
    default_options =
      headers:
        'User-Agent': ua

    @options ?= default_options

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
