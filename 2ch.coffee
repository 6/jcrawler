fs = require 'fs'
Iconv  = require('iconv').Iconv
h = require './helpers'
p = h.p
jcrawler = require './jcrawler'

REGEX_2CH_HREF = new RegExp("http://[^\.]+\.2ch\.net/")
REGEX_BOARD_HREF = new RegExp("http://([^\.]+)\.2ch\.net/([^/]+)")
IGNORE_BBS_SUBDOMAIN = ["headline", "www", "info", "watch", "shop", "epg", "find", "be", "newsnavi", "irc"]

class NiCrawler extends jcrawler.JCrawler
  constructor: (@options) ->
    super @options

  random_boards_list: (n, cb) ->
    this.get 'http://menu.2ch.net/bbstable.html', ($) ->
      boards = []
      $("font > a").each (idx) ->
        link = "#{$(this).attr("href")}subback.html"
        ignore_subdomain = false
        for subdomain in IGNORE_BBS_SUBDOMAIN
          if h.startsWith(link, "http://#{subdomain}.")
            ignore_subdomain = true
            break
        boards.push link unless !link.match(REGEX_2CH_HREF) or ignore_subdomain
      cb h.srswor(boards, n)
  
  random_threads_list: (board_url, n, cb) ->
    this.get board_url, ($) ->
      threads = []
      $("small#trad > a").each (idx) ->
        link = $(this).attr("href")
        threads.push link.substring(0, link.length - 4)
      cb h.srswor(threads, n)

  board_url_info: (url_string) ->
    match = url_string.match(REGEX_BOARD_HREF);
    [match[1], match[2]] # [subdomain, board_name]
  
  thread_link: (subdomain, board_name, thread) ->
    "http://#{subdomain}.2ch.net/test/read.cgi/#{board_name}/#{thread}"
  
  save_thread: (url, thread) ->
    this.get url, ($) ->
      content = $("dl.thread").html()
      filename = "#{h.date_string new Date()}_#{thread}"
      iconv = new Iconv('Shift-JIS', 'UTF-8')
      buffer = iconv.convert(content)
      fs.writeFileSync "data/2ch/#{filename}.data", buffer, "UTF-8"
      
main = () ->
  Ni = new NiCrawler
  #Ni.random_boards_list 10, (boards) ->
  #  p boards, boards.length
  board_url = "http://yuzuru.2ch.net/billiards/subback.html"
  [subdomain, board_name] = Ni.board_url_info(board_url)
  Ni.random_threads_list board_url, 1, (threads) ->
    for thread in threads
      link = Ni.thread_link(subdomain, board_name, thread)
      p link
      Ni.save_thread link, thread

main()
