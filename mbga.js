var FILE_PATH = "/Users/pete/iMacros/Macros/jcrawler/{0}";
var REGEX_HREF = new RegExp("href=\"[^\"]+\"", "gi");
var REGEX_IMGSRC = new RegExp("src=\"[^\"]+\"", "gi");
var URL_PROFILE = "http://yahoo-mbga.jp/{0}";
var URL_GROUP = "http://yahoo-mbga.jp/group/{0}";

// Source: http://forum.iopus.com/viewtopic.php?f=11&t=5267
// Note: this may not work depending on Java version(?)
write_file = function(path, data) {
  iimDisplay("Writing file:"+path);
   try {
      var out = new java.io.BufferedWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(new java.io.File(path)), "UTF8"));
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

save_profile = function(id, source_id) {
  var raw_demo = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof1-lay EXTRACT=HTM", 1);
  var raw_qa = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof2-lay EXTRACT=HTM", 1);
  var raw_diary = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof3-lay EXTRACT=HTM", 1);
  var raw_disc = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof4-lay EXTRACT=HTM", 1);
  var raw_greet = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof6-lay EXTRACT=HTM", 1);
  var raw_test = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof5-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+id+"_"+source_id+"_{0}.data";
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("demo")), raw_demo);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("qa")), raw_qa);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("diary")), raw_diary);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("disc")), raw_disc);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("greet")), raw_greet);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("test")), raw_test);
  write_file(FILE_PATH.format("data/mbga/person/"+filename.format("img")), avatar_url());
};

avatar_url = function() {
  var raw = run("TAG POS=1 TYPE=DIV ATTR=CLASS:lv3-ava-wrap EXTRACT=HTM", 1);
  var src = raw.match(REGEX_IMGSRC)[0]
  return src.substring(5, src.length - 1);
};

save_group = function(id) {
  var raw_meta = run("TAG POS=1 TYPE=UL ATTR=CLASS:blk-lay EXTRACT=HTM", 1);
  var raw_msg = run("TAG POS=1 TYPE=DIV ATTR=CLASS:crcltopic-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+id+"_{0}.data";
  var path_meta = FILE_PATH.format("data/mbga/group/"+filename.format("meta"));
  var path_msg = FILE_PATH.format("data/mbga/group/"+filename.format("msg"));
  write_file(path_meta, raw_meta);
  write_file(path_msg, raw_msg);
};

extract_profiles = function(source_id) {
  var raw = run("TAG POS=1 TYPE=DIV ATTR=ID:circlemem-sec EXTRACT=HTM", 1);
  var links = raw.match(REGEX_HREF);
  links.pop(); // last link isn't a profile
  var mod_links = [];
  for(var i=0; i<links.length; i++) {
    if(i % 2 == 0)
      mod_links.push({
        type:"profile",
        id: links[i].substring(7, links[i].length - 1),
        source: source_id
      });
  }
  return mod_links;
};

extract_groups = function() {
  var raw = run("TAG POS=1 TYPE=DIV ATTR=ID:circleentry-sec EXTRACT=HTM", 1);
  var links = raw.match(REGEX_HREF);
  links.pop(); // last link isn't a group link
  var mod_links = [];
  for(var i=0; i<links.length; i++) {
    if(i % 2 == 0)
      mod_links.push({
        type:"group",
        id: links[i].substring(13, links[i].length - 1)
      });
  }
  return mod_links;
};

main = function() {
  // randomly generated valid group IDs using random number generator
  // note: mgba seems to have skipped IDs from ~2,000,000 to ~30,000,000
  var seed_nodes = [
    {type: "group", id: "30704159"}
    , {type: "group", id: "1901844"}
    , {type: "group", id: "30945349"} // example of no threads
    , {type: "group", id: "487069"} 
    , {type: "group", id: "1719377"} // example of single thread
  ];
  var queue = [];
  queue = queue.concat(seed_nodes);
  var visited_groups = [];
  var visited_profiles = [];
  while(queue.length > 0){
    var item = queue.shift();
    if(item.type === "profile") {
      if(visited_profiles.indexOf(item.id) >= 0) continue;
      visit_url(URL_PROFILE.format(item.id));
      save_profile(item.id, item.source);
      visited_profiles.push(item.id);
      queue = queue.concat(extract_groups());
    }
    else {
      if(visited_groups.indexOf(item.id) >= 0) continue;
      visit_url(URL_GROUP.format(item.id));
      save_group(item.id);
      visited_groups.push(item.id);
      queue = queue.concat(extract_profiles(item.id));
    }
    sleep(random_range(3, 8));
    // if visited > 3000 people and next link is a group, finish
    if(visited_profiles.length > 3000 && queue[1].type !== "profile") break; 
  }
};

main();