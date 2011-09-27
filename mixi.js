run = function(code, n) {
  var retcode = iimPlay("CODE: "+code);
  if(retcode != 1) {
    alert("BAD CODE:"+code+"\n\nretcode:"+retcode);
    return;
  }
  var extract = iimGetLastExtract(n);
  if(extract == "#EANF#") return false; // nothing was found
  return extract;
};

is_logged_in = function(){
  iimPlay("CODE: URL GOTO=http://mixi.jp/");
  result = run("TAG POS=1 TYPE=FORM ATTR=NAME:login_form EXTRACT=TXT");
  return !result;
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
