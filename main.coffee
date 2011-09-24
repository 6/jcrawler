p = require('sys').puts
env = require './config/env'
mixi_crawler = require './mixi_crawler'

m = new mixi_crawler.MixiCrawler()
m.get 'http://www.google.com/intl/en/about/corporate/index.html'
