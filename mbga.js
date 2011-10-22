var FILE_PATH = "/Users/pete/iMacros/Macros/jcrawler/{0}";

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

save_profile = function(id) {
  var raw_profile = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof1-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+id+".data";
  var path = FILE_PATH.format("data/mbga/person/"+filename);
  write_file(path, raw_profile);
};

save_group = function(id) {
  var raw_group = run("TAG POS=1 TYPE=UL ATTR=CLASS:blk-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+id+".data";
  var path = FILE_PATH.format("data/mbga/group/"+filename);
  write_file(path, raw_group);
};

visit_profile = function(id) {
  
};

visit_group = function(id) {
  
};

extract_profiles = function() {
  
};

extract_groups = function() {
  
};

main = function() {
  //save_profile("http://yahoo-mbga.jp/10086","10086");
  //save_group("http://yahoo-mbga.jp/group/31966079", "31966079");
  
  var queue = []; // TODO seed nodes
  var visited_groups = [];
  var visited_profiles = [];
  while(queue.length > 0){
    var item = queue.shift();
    if(item["type"] === "profile") {
      if(visited_profiles.indexOf(item["id"]) < 0) continue;
      visit_profile(item["id"]);
      save_profile(item["id"]);
      visited_profiles.push(item["id"]);
      queue.concat(extract_groups());
    }
    else {
      if(visited_groups.indexOf(item["id"]) < 0) continue;
      visit_group(item["id"]);
      save_group(item["id"]);
      visited_groups.push(item["id"]);
      queue.concat(extract_profiles());
    }
  }
};

main();