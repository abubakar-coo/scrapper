var username = "";
var apkononline = "";

(async function(){
       
    
         var opcA = { usercx: null,  apkononline: null };
         var usercx = "";
         
         const apkon_key = "apkon_key";

         let storres = await chrome.storage.local.get([apkon_key]);

         if (apkon_key in storres) { opcA = storres[apkon_key] }
         if ( opcA.usercx ) { username = opcA.usercx; }
         else { username = "" + ranSX(10) + "".toLowerCase(); opcA.usercx = username; }

         if ( opcA.apkononline ) {  apkononline = opcA.apkononline; }
         else { apkononline = "1"; opcA.apkononline = "1"; }


        var stox = {};
        stox[apkon_key] = opcA;
        await chrome.storage.local.set(stox);
    
    
       if ( apkononline == "1")  {
            document.getElementById("xonline").checked = true;
        }
        else {
            document.getElementById("xonline").checked = false;
        }
        

        
        
        document.getElementById('integrator').innerText = "My ApkOnline username: "+username;     
        document.getElementById('loginxx').style.display = "none";
        document.getElementById('elfinder').style.display = "none";
        document.getElementById('listfilesx').style.display = "block";
        document.getElementById('perfecto').innerText = "";
        document.getElementById('integrator').style.display = "block";
        

        var xhr1 = new XMLHttpRequest();
                    xhr1.open('GET', 'https://www.uptoplay.net/media/system/ext/c-2-androidemulatorr.php?u=' + username, true);
                    xhr1.onload = function (e) {
                        if (xhr1.readyState === 4) {
                                if (xhr1.status === 200) {
                                        //console.log(xhr1.responseText);
                                        var response1 = xhr1.responseText;
                                        listfilesx.innerHTML = "<p>List of files detected in this webpage. Click to edit:</p> " + response1; 
                                        listfilesx.innerHTML = response1;

                                 } else {
                                        listfilesx = document.getElementById('listfilesx');  
                                        listfilesx.innerHTML = "<p>No files detected</p>";
                                }
                         }
                };
        xhr1.onerror = function (e) {
                        listfilesx = document.getElementById('listfilesx');  
                        listfilesx.innerHTML = "<p>No files detected</p>";
                };
        xhr1.send();     
    
    
    
    
        var  redxda = {};
    
        $("#xonline").click(async function() {
            if (document.getElementById('xonline').checked) {
                redxda.usercx = username;
                redxda.apkononline = "1";    
                var stox = {};
                stox[apkon_key] = redxda;
                await chrome.storage.local.set(stox);
            }
            else {
                redxda.usercx = username;
                redxda.apkononline = "0";    
                var stox = {};
                stox[apkon_key] = redxda;
                await chrome.storage.local.set(stox);
            }
            return false;
        });
    
    
        
    
    
          $("#dxee").click(function() {
        
                document.getElementById('listfilesx').style.display = "block";
                document.getElementById('loginxx').style.display = "none";
                document.getElementById('elfinder').style.display = "none";
                document.getElementById('perfecto').innerText = "";
                document.getElementById('notex').style.display = "block";
                document.getElementById('integrator').style.display = "block";


                var xhr1 = new XMLHttpRequest();
                    xhr1.open('GET', 'https://www.uptoplay.net/media/system/ext/c-2-androidemulatorr-17.php?u=' + username, true);
                    xhr1.onload = function (e) {
                        if (xhr1.readyState === 4) {
                                if (xhr1.status === 200) {
                                        //console.log(xhr1.responseText);
                                        var response1 = xhr1.responseText;
                                        listfilesx.innerHTML = "<p style='font-size:13px;'>List of files detected in this webpage. Click to edit:</p> " + response1; 
                                        listfilesx.innerHTML = response1;

                                 } else {
                                        listfilesx = document.getElementById('listfilesx');  
                                        listfilesx.innerHTML = "<p style='font-size:13px;'>No files detected. Goto a webpage with APK files.</p>";
                                }
                         }
                };
                xhr1.onerror = function (e) {
                        listfilesx = document.getElementById('listfilesx');  
                        listfilesx.innerHTML = "<p style='font-size:13px;'>No files detected. Goto a webpage with APK files.</p>";
                };
                xhr1.send();     

                return false;
        });
    
    
       $("#runemulx").click(function() {
        
                document.getElementById('listfilesx').style.display = "none";
                document.getElementById('loginxx').style.display = "block";
                document.getElementById('elfinder').style.display = "none";
                document.getElementById('notex').style.display = "none";
                document.getElementById('integrator').style.display = "none";
                document.getElementById('perfecto').innerText = "";

                var oreyy = document.getElementById('login_bannerxx');
            
                var iframe = document.createElement('iframe');
                iframe.id ="login_bannerxx";
                iframe.width = "100%";
                iframe.height = "500px";
                iframe.src = 'https://www.uptoplay.net/playonline/androidemulator-ext.php?apk=uptoplayrunemulator.apk';
                iframe.style.cssText = '';
                iframe.frameBorder = "0";          
                iframe.style.cssText = "border:0"; 
                oreyy = document.getElementById('login_bannerxx');
                oreyy.parentNode.insertBefore(iframe, oreyy);
                oreyy.parentNode.removeChild(oreyy);
                oreyy = document.getElementById('login_bannerxx'); 

                return false;
        });
    
        
        
        $("#files").click(function() {
        
            window.open("https://www.uptoplay.net/filemanager.php?username=" + username + "&apkononline=" + apkononline);
            return false;
        });
    
    
        $("#fullscreenx").click(function() {
            window.open("https://www.uptoplay.net/media/system/ext/run-androidemulator-3.php?username=" + username + "&url=2f7661722f7777772f68746d6c2f7765626f66666963652f6d79646174612f646f6b71696f336d6c6a2f4e6577446f63756d656e74732f52756e456d756c61746f722e61706b&apkononline=" + apkononline);
            return false;
        });
        
    
  
})();



function ranSX(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var ranSX = '';
    for (var i = 0; i < len; i++) {
        var rxDD = Math.floor(Math.random() * charSet.length);
        ranSX += charSet.substring(rxDD,rxDD+1);
    }
    return ranSX.toLowerCase();
}






