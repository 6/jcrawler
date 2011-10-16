r = require 'request'
fs = require 'fs'
path = require 'path'
jsdom = require 'jsdom'
h = require './helpers'
p = h.p

jquery_path = path.join __dirname, 'lib/jquery-1.6.4.js'
jquery = fs.readFileSync(jquery_path).toString()

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'

class exports.JCrawler
  constructor: (@options) ->
    # defaults
    @options ?= {}
    @options.headers ?= {}
    @options.headers['User-Agent'] ?= ua

  error: (res) ->
    p "Error! #{res.statusCode} @ #{h.date_string new Date()}"

  get: (url, cb, cb_error) ->
    self = @
    opts = h.clone @options
    opts.url = url
    opts.method = 'GET'
    r opts, (err, res, body) ->
      if err? or res.statusCode != 200
        if cb_error? then cb_error(err, res, body) else self.error(res)
      else
        jsdom.env
          html: body
          src: jquery
          done: (error, window) -> cb window.$
