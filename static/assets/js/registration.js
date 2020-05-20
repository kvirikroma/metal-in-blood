let users = JSON.parse(localStorage.getItem('users'));
if (users) {
    null;
} else {
    localStorage.setItem('users', JSON.stringify(data));
    users = JSON.parse(localStorage.getItem('users'));

}
function sendToStorage() {
    // const xhr = new XMLHttpRequest();
    // xhr.open('GET', 'static/assets/js/users_db.json');
    // xhr.send();
    // xhr.addEventListener('readystatechange', () => {
    // if (xhr.status === 200 && xhr.readyState == 4) {
    //     localStorage.setItem('users', xhr.response)
    // } else return;
    // });
}

function formatData(data) {
    return JSON.stringify(data)
}

function registration(login, password) {
    const data = users;
    data.push({
        login: login,
        password: password    
    });
    localStorage.setItem('users', JSON.stringify(data));
    location.href = localStorage.getItem('global') + 'signin.html'

}

(function() {
    const form = document.querySelector('#registration');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const config = [form.login.value, form.mail.value, form.pass.value, form.repeat_pass.value];
        if(validateForm(...config)) {
            alert('success');
            registration(form.login.value, form.mail.value, form.pass.value);
        } else {
            alert('Smth wrong...')
        }
        
    })
})();

function validateForm(login, email, password1, password2) {
    const data = users;
    let success = false;
    if (password1 === password2 && password1.length >= 6) {
        const filtered = data.filter(user => user.login == login || user.email == email);
        filtered.length == 0 ? success = true : success = false
    }
    return success;
}
sendToStorage();
