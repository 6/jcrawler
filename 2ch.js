var FILE_PATH = "/Users/pete/iMacros/Macros/jcrawler/{0}";
var URL_BBS_LIST = "http://menu.2ch.net/bbstable.html";
var THREAD = "http://{0}.2ch.net/test/read.cgi/{1}/{2}/";
var REGEX_HREF = new RegExp("href=\"[^\"]+\"", "gi");
var REGEX_2CH_HREF = new RegExp("http://[^\.]+\.2ch\.net/");
var REGEX_BOARD_HREF = new RegExp("http://([^\.]+)\.2ch\.net/([^/]+)");
var IGNORE_BBS_SUBDOMAIN = ["qb5","www2", "headline", "www", "info", "watch", "shop", "epg", "find", "be", "newsnavi", "irc"];

// Source: http://forum.iopus.com/viewtopic.php?f=11&t=5267
// Note: this may not work depending on Java version(?)
write_file = function(path, data) {
  iimDisplay("Writing file:"+path);
   try {
      var out = new java.io.BufferedWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(new java.io.File(path)), "Shift_JIS"));
      out.write(data);
      out.close();
      out=null;
   }
   catch(e) { //catch and report any errors
      alert(""+e);
   }
};

// Source: http://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format/4256130#4256130
String.prototype.format = function() {
  var formatted = this;
  for (var i = 0; i < arguments.length; i++) {
    var regexp = new RegExp('\\{'+i+'\\}', 'gi');
    formatted = formatted.replace(regexp, arguments[i]);
  }
  return formatted;
};

// Source: http://stackoverflow.com/questions/646628/javascript-startswith
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) == str;
  };
}

// Source: http://stackoverflow.com/questions/280634/endswith-in-javascript
if (typeof String.prototype.endsWith != 'function') {
  String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
  };
}

// inclusive random range
// Source: http://www.admixweb.com/2010/08/24/javascript-tip-get-a-random-number-between-two-integers/
random_range = function(from, to){
  var val = Math.floor(Math.random() * (to - from + 1) + from);
  if(val > to) { // in case Math.random() can produce 1.0 (does it?)
    val = to;
  }
  return val;
};

// Source: https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Date
function date_string(d){
 function pad(n){return n<10 ? '0'+n : n}
 return d.getUTCFullYear()+''
      + pad(d.getUTCMonth()+1)+''
      + pad(d.getUTCDate())+''
      + pad(d.getUTCHours())+''
      + pad(d.getUTCMinutes())+''
      + pad(d.getUTCSeconds())}

srswor = function(list, n, ignore) {
  if(!ignore) ignore = [];
  for(var i=0; i<ignore.length; i++) {
    var idx = list.indexOf(ignore[i]);
    if(idx >= 0) list.splice(idx, 1);
  }
  if(list.length < n) return list;
  var new_list = [];
  while(new_list.length < n && list.length > 0) {
    var rand_idx = random_range(0, list.length - 1);
    new_list.push(list.splice(rand_idx, 1));
  }
  return new_list;
};

run = function(code, n) {
  var retcode = iimPlay("CODE: "+code);
  if(retcode != 1) {
    alert("BAD CODE:\n"+code+"\n\nretcode:"+retcode);
    return;
  }
  if(n) {
    var extract = iimGetLastExtract(n);
    if(extract == "#EANF#") return false; // "Extraction Anchor Not Found"
    return extract;
  }
};

sleep = function(seconds) { run("WAIT SECONDS="+seconds); };
visit_url = function(url) { run("URL GOTO="+url); };

random_boards_list = function(n) {
  visit_url("file://"+FILE_PATH.format("/sources/bbstable.html"));
  var raw = run("TAG POS=1 TYPE=FONT ATTR=* EXTRACT=HTM", 1);
  var raw_list = raw.match(REGEX_HREF);
  var mod_list = [];
  for(var i=0; i<raw_list.length; i++) {
    var link = raw_list[i].substring(6, raw_list[i].length - 2);
    if(!link.match(REGEX_2CH_HREF)) {
      continue;
    }
    var ignore_subdomain = false;
    for(var j=0; j<IGNORE_BBS_SUBDOMAIN.length; j++) {
      if(link.startsWith("http://"+IGNORE_BBS_SUBDOMAIN[j]+".")) {
        ignore_subdomain = true; break;
      }
    }
    if(ignore_subdomain) {
      continue;
    }
    mod_list.push(link);
  }
  return srswor(mod_list, n);
};

random_threads_list = function(board_url, n, ignore) {
  visit_url(subback_board_url(board_url));
  var raw = run("TAG POS=1 TYPE=SMALL ATTR=* EXTRACT=HTM", 1);
  var list = raw.match(REGEX_HREF);
  var mod_list = [];
  for(var i=0; i<list.length; i++) {
    mod_list.push(list[i].substring(6, list[i].length - 5));
  }
  return srswor(mod_list, n, ignore);
};

subback_board_url = function(board_url) {
  if(!board_url.endsWith("/")) board_url += "/";
  return board_url + "subback.html";
};

board_url_info = function(url_string) {
  var match = url_string.match(REGEX_BOARD_HREF);
  // [subdomain, board_name]
  return [match[1], match[2]];
};

thread_link = function(subdomain, board, thread) {
  return THREAD.format(subdomain, board, thread);
};

save_thread = function(board_url, thread) {
  var info = board_url_info(board_url);
  var subdomain = info[0];
  var board = info[1];
  visit_url(thread_link(subdomain, board, thread));
  var raw_messages = run("TAG POS=1 TYPE=DL ATTR=CLASS:thread EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+subdomain+"_"+board+"_"+thread;
  var path = FILE_PATH.format("data/2ch/"+filename+".data");
  write_file(path, raw_messages);
};

main = function() {
  for(var m=0; m<3; m++) {
    var saved_threads = [];
    var boards = random_boards_list(100);
    for(var i=0; i<boards.length; i++) {
      var board_url = String(boards[i]);
      var threads = random_threads_list(board_url, 5, saved_threads);
      for(var j=0; j<threads.length; j++) {
        sleep(random_range(4, 6));
        save_thread(board_url, threads[j])
        saved_threads.push(threads[j]);
      }
      sleep(random_range(2, 4));
    }
  }
};

main();