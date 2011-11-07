jcrawler is a collection of [focused web crawlers](http://en.wikipedia.org/wiki/Focused_crawler) for crawling three Japanese social websites:

1. [Yahoo!モバゲー](http://yahoo-mbga.jp) (Yahoo! Mobage), a mobile game social network
2. [２ちゃんねる](http://2ch.net) (2channel), an anonymous bulletin board system
3. [ニコニコ動画](http://nicovideo.jp) (Nico Nico Douga), a social video-sharing website

Crawlers
-----------
Nico Nico Douga [provides an API](http://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E5%8B%95%E7%94%BBapi) for accessing basic video metadata such as date uploaded and number of comments. `nico_crawler.py` uses this API to crawl randomly sampled videos.

Mobage and 2channel, however, do not provide an API or a crawler-friendly form of accessing their sites, so I used a Firefox plugin called [iMacros](https://addons.mozilla.org/en-US/firefox/addon/imacros-for-firefox/) to create crawlers for Mobage and 2channel in JavaScript. These crawlers are `2ch_crawler.js` and `mbga_crawler.js`. 

These crawlers extract and save raw HTML without parsing it, and this raw data is saved into the `data` directory.

The `sources` directory contains a file `bbstable.html` that contains links to all the boards. This file is used by the 2channel crawler when randomly selecting boards to crawl.
