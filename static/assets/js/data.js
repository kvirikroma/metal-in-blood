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
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getCookie('token')}`
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client

    }
    method == 'POST' ? config.body = JSON.stringify(data) : null; // body data type must match "Content-Type" header
    // Default options are marked with *
    const response = await fetch(url, config);
    console.log(response.status);

    if (response.status == 401) {
    console.log(response.status);
        refreshToken();
        return postData(url, data, method);
    } else if(response.status > 401){
        showError(response.status, response)
    } else {
        return await response.json() // parses JSON response into native JavaScript objects
    }
    // if(response.status >= 200 && response.status < 300) {
    
    // } 

}

function logOut() {
    document.cookie = 'token=null';
    document.cookie = 'refreshToken=null';
    sessionStorage.clear();
}

function refreshToken() {
    const ref_token = getCookie('refreshToken');

    refData(`http://0.0.0.0:5000/api/v1/user/refresh`, {}, 'POST')
        .then((data) => {
            console.log(data);
            console.log('REFRESHING TOKEN  IS SUCCESS');

            document.cookie = `token=${data.access_token}`;
            document.cookie = `refreshToken=${data.refresh_token}`;

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}

// refreshToken();


async function refData(url = '', data = {}, method = 'POST') {
    const config = {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getCookie('refreshToken')}`
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client

    }
    method == 'POST' ? config.body = JSON.stringify(data) : null; // body data type must match "Content-Type" header
    // Default options are marked with *
    const response = await fetch(url, config);
    console.log(response.status);

    
    return await response.json() // parses JSON response into native JavaScript objects
    
    // if(response.status >= 200 && response.status < 300) {
    
    // } 

}


function showError(error, data) {
    console.log(data);
    return alert(`Error code: ${error}, ${data.statusText ? data.statusText : ''}`)
}