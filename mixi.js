MAX_PERSON_ID = 34440000;
PROFILE_URL = "http://mixi.jp/show_friend.pl?id={0}"
COMMUNITY_URL = "http://mixi.jp/view_community.pl?id={0}"

// Source: http://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format/4256130#4256130
String.prototype.format = function() {
  var formatted = this;
  for (var i = 0; i < arguments.length; i++) {
    var regexp = new RegExp('\\{'+i+'\\}', 'gi');
    formatted = formatted.replace(regexp, arguments[i]);
  }
  return formatted;
};

rand_range = function(start, end) {
  return Math.floor(Math.random()*end - 1) + start;
};

run = function(code, n) {
  var retcode = iimPlay("CODE: "+code);
  if(retcode != 1) {
    alert("BAD CODE:"+code+"\n\nretcode:"+retcode);
    return;
  }
  if(n) {
    var extract = iimGetLastExtract(n);
    if(extract == "#EANF#") return false; // nothing was found
    return extract;
  }
};

visit_url = function(url) { run("URL GOTO="+url); };

is_logged_in = function(){
  visit_url("http://mixi.jp/");
  result = run("TAG POS=1 TYPE=FORM ATTR=NAME:login_form EXTRACT=TXT");
  return !result;
};

random_person_id = function() {
  var rand_id = rand_range(1, MAX_PERSON_ID);
  visit_url(PROFILE_URL.format(rand_id));
  title = run("TAG POS=1 TYPE=TITLE ATTR=* EXTRACT=TXT", 1);
  if(title.substring(0,1) == "[") return rand_id;
  else return random_person_id();
};

main = function() {
  iimDisplay("Check if logged in to Mixi...");
  if(!is_logged_in()) {
    iimDisplay("Please login first.");
    return;
  }
  iimDisplay("Logged in. Start crawling...");
};

main();
