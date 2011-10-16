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

save_profile = function(link, profile) {
  var raw_profile = run("TAG POS=1 TYPE=DIV ATTR=CLASS:prof1-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+profile+".data";
  var path = FILE_PATH.format("data/mbga/person/"+filename);
  write_file(path, raw_profile);
};

save_group = function(link, group) {
  var raw_group = run("TAG POS=1 TYPE=UL ATTR=CLASS:blk-lay EXTRACT=HTM", 1);
  var filename = date_string(new Date())+"_"+group+".data";
  var path = FILE_PATH.format("data/mbga/group/"+filename);
  write_file(path, raw_group);
};

main = function() {
  //save_profile("http://yahoo-mbga.jp/10086","10086");
  save_group("http://yahoo-mbga.jp/group/31966079", "31966079");
};

main();