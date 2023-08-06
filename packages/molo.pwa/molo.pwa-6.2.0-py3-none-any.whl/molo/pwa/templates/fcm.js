// Script loader
function script(url) {

    if(Array.isArray(url)) {
        var self = this, prom = [];
        url.forEach(function(item) {
            prom.push(self.script(item));
        });
        return Promise.all(prom);
    }

    return new Promise(function (resolve, reject) {
        var r = false,
            t = document.getElementsByTagName("script")[0],
            s = document.createElement("script");

        s.type = "text/javascript";
        s.src = url;
        s.async = true;
        s.onload = s.onreadystatechange = function () {
            if (!r && (!this.readyState || this.readyState == "complete")) {
                r = true;
                resolve(this);
            }
        };
        s.onerror = s.onabort = reject;
        t.parentNode.insertBefore(s, t);
    });

}

var loadFCM = script(["https://www.gstatic.com/firebasejs/4.1.3/firebase-app.js", "https://www.gstatic.com/firebasejs/4.1.3/firebase-messaging.js", "/toast.min.js"]);

loadFCM.then(function() {

  firebase.initializeApp(fcmConfig);
  
  // Get X-CSRFToken
  function parse_cookies() {
  var cookies = {};
  if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(function (c) {
          var m = c.trim().match(/(\w+)=(.*)/);
          if(m !== undefined) {
              cookies[m[1]] = decodeURIComponent(m[2]);
          }
      });
  }
  return cookies;
  }

  var cookies = parse_cookies();

  // Token magic
  const messaging = firebase.messaging();
  navigator.serviceWorker.register('/serviceworker.js')
    .then((registration) => {
      console.log(registration);
      messaging.useServiceWorker(registration);

      messaging.onTokenRefresh(function() {
       messaging.getToken()
       .then(function(refreshedToken) {
         setTokenSentToServer(false);
         sendTokenToServer(refreshedToken);
       });
      });

      function sendTokenToServer(currentToken) {
        if (!isTokenSentToServer()) {
          fetch('/notification_devices/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookies['csrftoken']
              },
            body: JSON.stringify({
              'registration_id': currentToken,
              'type': 'web',
            }),
            credentials: "include",
          })
          setTokenSentToServer(true);
        }
      }

      function isTokenSentToServer() {
       return window.localStorage.getItem('sentToServer') == 1;
      }
      function setTokenSentToServer(sent) {
       window.localStorage.setItem('sentToServer', sent ? 1 : 0);
      }

      function requestPermission() {
       messaging.requestPermission()
       .then(function() {
         messaging.getToken()
         .then(function(currentToken) {
           if (currentToken) {
             sendTokenToServer(currentToken);
           } else {
             setTokenSentToServer(false);
           }
         })
         .catch(function(err) {
           setTokenSentToServer(false);
         });
       });
      }

      requestPermission();

      // In app notification using Toast
      messaging.onMessage(function(data) {
        var options = {
              settings: {
                duration: 3000
              }
        };
        iqwerty.toast.Toast(data.notification.title + ' - ' + data.notification.body, options);
      });

    });

});
