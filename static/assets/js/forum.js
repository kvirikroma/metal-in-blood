const addFormTrigger = document.querySelector('.add-new');
const addForm = document.querySelector('.add-new__form');

addForm.addEventListener('submit', (e) => {
    e.preventDefault();
    addNew(addForm.heading.value, addForm.body.value);
    console.log(addForm.heading.value, addForm.body.value);
});

addFormTrigger.addEventListener('click', function() {
    this.classList.toggle('active');
    addForm.classList.toggle('active');

    this.classList.contains('active') ? this.textContent = 'Скрыть' : this.textContent = 'Добавить тред';

    
});

function renderThread(data) {
const parent = document.querySelector('.forum .main__content');
let threads =  [];
    
    if(!Array.isArray(data)) {
        threads.push(data);
    } else {
        threads = data;
    }
console.log(threads, data)
    threads.forEach(thread => {
        const pattern = `
                    <a class="forum__item" href="comments.html?page=1&id=${thread.thread_id}">
                        <div class="forum__item-text">
                            <p>${thread.title}</p>
                        </div>
                        <div class="forum__item-info">
                            <div class="forum__item-views"><div></div>${thread.messages_count}</div>
                            <div class="forum__item-comments"><div></div>${thread.users_count}</div>
                        </div>
                    </a>
        `;
        parent.innerHTML += pattern;
    });

}

function addNew(title, body) {
    const send = {
        title,
        body
    };

    postData(`http://0.0.0.0:5000/api/v1/forum/threads`, send, 'POST')
        .then((data) => {
            console.log(data);
            renderThread(data);
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}

function renderDefaultThread() {
    postData('http://0.0.0.0:5000/api/v1/forum/threads?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            renderThread(data.threads);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultThread();