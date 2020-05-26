

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function isLogged() {
    if (getCookie('token') != 'null' && getCookie('token')) return true
        else return false;
}

async function postData(url = '', data = {}, method = 'POST') {
    const config = {
    method: method, // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *client
    
  }
  method == 'POST' ? config.body = JSON.stringify(data) : null; // body data type must match "Content-Type" header
  // Default options are marked with *
  const response = await fetch(url, config);
  return await response.json(); // parses JSON response into native JavaScript objects
}



