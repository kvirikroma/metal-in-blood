

if (isLogged()) {
    const user = sessionStorage.getItem('current_user');
    document.querySelector('.mainSignIn__dialog').innerHTML = `<h1>${user}, do you want <a href="#">logout</a>?</h1>`
}

function formatData(data) {
    return JSON.stringify(data)
}

function authorization(login, password) {

    try {
        const info = {
            login,
            password
        }

            postData('http://0.0.0.0:5000/api/v1/user/signin', info)
              .then((data) => {
                console.log(data); // JSON data parsed by `response.json()` call
                 
                

                if(data.access_token) {
                    document.cookie = `token=${data.access_token}`;
                    sessionStorage.setItem('current_user', info.login)
                    location.href = 'http://0.0.0.0:5000/';
                } else {
                    document.cookie = `token=null`;
                }
                console.log(document.cookie); // JSON data parsed by `response.json()` call

            }).catch((data) => {
                console.error(data);
                console.trace();
            });
    }
    catch (e) {
        console.log(e);
    }
}

(function() {
    const form = document.querySelector('#login');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        authorization(form.login.value, form.pass.value);
    })
})();

const main_url = 'http://0.0.0.0:5000';





