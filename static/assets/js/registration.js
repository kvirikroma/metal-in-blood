function formatData(data) {
    return JSON.stringify(data)
}

function registration(email, login, password) {

    const info = {
        email,
        login,
        password
    }

    postData('/api/v1/user/signup', info)
        .then((data) => {
            console.log(data)

            if (data == null) {
                alert('Registration success'); // JSON data parsed by `response.json()` call
                location.href = '/signin.html';
            } else {
                alert(data.message)
            }
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}

(function() {
    const form = document.querySelector('#registration');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const config = [form.login.value, form.mail.value, form.pass.value, form.repeat_pass.value];
        if (validateForm(...config)) {
            console.info('Validation passed');
            registration(form.mail.value, form.login.value, form.pass.value);
        } else {
            console.info('Validation failed');
        }

    })
})();

function validateForm(login, email, password1, password2) {
    if (password1 === password2 && password1.length >= 6) {
        return true
    }
    return false;
}