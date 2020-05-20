

let users = JSON.parse(localStorage.getItem('users'));
if (users) {
    null;
} else {
    localStorage.setItem('users', JSON.stringify(data));
    users = JSON.parse(localStorage.getItem('users'));

}


function sendToStorage() {
   
}

function formatData(data) {
    return JSON.stringify(data)
}

function authorization(login, password) {
    const data = users;
    try {
        const filteredByLogin = data.filter(user => user.login == login);
        const user = filteredByLogin.find(user => user.password == password);
        console.log(user);
        if(user) { 
            localStorage.setItem('current_user', JSON.stringify(user));
            alert(`Hello, ${user.login}!`);
            location.href = localStorage.getItem('global') + 'index.html'
        } else {
            alert('Invalid login or password')
        };
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
sendToStorage();
