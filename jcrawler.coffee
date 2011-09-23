r = require 'restler'
fs = require 'fs'
path = require 'path'
jsdom = require 'jsdom'
p = require('sys').puts

jquery_path = path.join __dirname, 'jquery-1.6.4.js'
jquery = fs.readFileSync(jquery_path).toString()

class exports.JCrawler
  constructor: (@options = {}) ->

  get: (url, cb_success, cb_error = null) ->
    r.get(url, @options)
      .on 'success', (html, res) ->
        jsdom.env
          html: html
          src: jquery
          done: (errors, window) ->
            $ = window.$
            cb_success $
      .on 'error', (html, res) ->
        status = res.statusCode
        if cb_error? then cb_error status else p "ERROR: #{res.statusCode}"
