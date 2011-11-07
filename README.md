jcrawler is a collection of [focused web crawlers](http://en.wikipedia.org/wiki/Focused_crawler) and programs for crawling and analyzing three Japanese social websites:

1. [Yahoo!モバゲー](http://yahoo-mbga.jp) (Yahoo! Mobage), a mobile game social network
2. [２ちゃんねる](http://2ch.net) (2channel), an anonymous bulletin board system
3. [ニコニコ動画](http://nicovideo.jp) (Nico Nico Douga), a social video-sharing website

Crawlers
--------
Nico Nico Douga [provides an API](http://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E5%8B%95%E7%94%BBapi) for accessing basic video metadata such as date uploaded and number of comments. `nico_crawler.py` uses this API to crawl randomly sampled videos.

Mobage and 2channel, however, do not provide an API or a crawler-friendly form of accessing their sites, so I used a Firefox plugin called [iMacros](https://addons.mozilla.org/en-US/firefox/addon/imacros-for-firefox/) to create crawlers for Mobage and 2channel in JavaScript. These crawlers are `2ch_crawler.js` and `mbga_crawler.js`. 

I created a separate crawler, `mbga_avatar.py`,  for downloading all user avatar image files, since the JavaScript interface for iMacros does not include this functionality.

These crawlers extract and save raw HTML without parsing it, and this raw data is saved into the `data` directory.

The `sources` directory contains a file `bbstable.html` that contains links to all the boards. This file is used by the 2channel crawler when randomly selecting boards to crawl.

Parsers
-------
Parsers condense the raw data extracted by crawlers into a more easily analyzable form. I use these parsers to create [CSV](http://en.wikipedia.org/wiki/Comma-separated_values) files that can be imported into statistical analysis software such as Excel or Google Docs.

### Mobage
Mobage avatar images are preprocessed using `mbga_convert_avatar.py`, which uses [ImageMagick](http://imagemagick.org) to convert avatars from animated GIF format to a PNG of the first frame of the animated GIF. This conversion makes image analysis easier in the next stage of avatar image parsing.

`mbga_parser.py` has methods for analyzing people, groups, and avatar data. Avatar images are analyzed with [PIL](http://www.pythonware.com/products/pil/) and [NumPy](http://numpy.scipy.org/) to estimate whether or not the user has purchased a custom background for their avatar. The avatar image file URL reveals the emotion of the user's avatar image (Ex: the image file URL `xlarge-entire-smile.gif` means the avatar is displaying the "smile" emotion).

### 2channel
2channel data is parsed by `2ch_parser.py`, which parses data at the individual message level. This program has a method for parsing the message metadata, such as date posted, as well as a method for parsing the message content.

There were several issues encountered when parsing 2channel data:

* 2channel uses [Shift_JIS encoding](http://en.wikipedia.org/wiki/Shift_JIS) (Mobage and Nico Nico Douga both use UTF-8, a more common encoding for Japanese websites)
* 2channel had several invalid data points. For example, several posts had invalid dates posted, such as "2665/04/02" or "2006/03/32".
* Since the amount of data I collected for 2channel (~400,000 messages, or 2,400,000 total data points) was too large for Excel or Google Docs to handle, I created a `2ch_analyzer.py` to do some basic statistical analysis and summarization of the data.

### Nico Nico Douga
Nico Nico Douga data is parsed by `nico_parser.py`, which applies necessary conversions of data. These conversions includes:

* Converting length of video to from minutes/seconds to seconds. Ex: `1:23` is converted to `83`
* Scaling number views, comments, and mylists by time since video was uploaded
