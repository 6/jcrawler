var FILE_PATH = "/Users/pete/iMacros/Macros/jcrawler/{0}";
var URL_BBS_LIST = "http://menu.2ch.net/bbstable.html";
var THREAD = "http://{0}.2ch.net/test/read.cgi/{1}/{2}/";
var REGEX_HREF = new RegExp("href=\"[^\"]+\"", "gi");
var REGEX_2CH_HREF = new RegExp("http://[^\.]+\.2ch\.net/");
var REGEX_BOARD_HREF = new RegExp("http://([^\.]+)\.2ch\.net/([^/]+)");
var IGNORE_BBS_SUBDOMAIN = ["headline", "www", "info", "watch", "shop", "epg", "find", "be", "newsnavi", "irc"];

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

srswor = function(list, n) {
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
  visit_url(URL_BBS_LIST);
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

random_threads_list = function(n) {
  var raw = run("TAG POS=1 TYPE=SMALL ATTR=* EXTRACT=HTM", 1);
  var list = raw.match(REGEX_HREF);
  var mod_list = [];
  for(var i=0; i<list.length; i++) {
    mod_list.push(list[i].substring(6, list[i].length - 5));
  }
  return srswor(mod_list, n);
};

board_url_info = function(url_string) {
  var match = url_string.match(REGEX_BOARD_HREF);
  // [subdomain, board_name]
  return [match[1], match[2]];
};

thread_link = function(subdomain, board, thread) {
  return THREAD.format(subdomain, board, thread);
};

save_thread = function(link, thread) {
  visit_url(link);
  var raw_messages = run("TAG POS=1 TYPE=DL ATTR=CLASS:thread EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+thread;
  var path = FILE_PATH.format("data/2ch/"+filename+".data");
  write_file(path, raw_messages);
};

main = function() {
  //alert(random_boards_list(10));
  //http://yuzuru.2ch.net/billiards/subback.html
  //alert(board_url_info("http://yuzuru.2ch.net/billiards/"));
  //alert(random_threads_list(10));
  var thread = "1287916288";
  save_thread(thread_link("yuzuru", "billiards", thread),thread)
};

main();