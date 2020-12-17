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

    this.classList.contains('active') ? this.textContent = `${voc.hide}` : this.textContent = `${voc.add_thread}`;

    
});

function renderThread(data) {
const parent = document.querySelector('.forum .main__content');
let threads =  [];
    parent.innerHTML = null;
    if(!Array.isArray(data)) {
        threads.push(data);
    } else {
        threads = data;
    }
console.log(threads, data)
    threads.forEach(thread => {
        const pattern = `
                    <div class="forum__item" data-author="${thread.author}" data-id="${thread.thread_id}" data-href="comments.html?page=1&id=${thread.thread_id}">
                        <div class="forum__item-text">
                            <p>${thread.title}</p>
                        </div>
                        <div class="forum__item-info">
                            <div class="forum__item-views"><div></div>${thread.users_count}</div>
                            <div class="forum__item-comments"><div></div>${thread.messages_count}</div>
                        </div>
                        <p class="comment-del"><img src="https://icons.iconarchive.com/icons/graphicloads/android-settings/256/cross-icon.png" width="20"></p>
                    </div>
        `;
        parent.innerHTML += pattern;
    });

    const items = parent.querySelectorAll('.forum__item');
    const currentSession = sessionStorage.getItem('current_user'); 
    items.forEach(comment => {
        if(comment.getAttribute('data-author') === currentSession) {
            comment.classList.add('active');
        }
    });
}

const items = document.querySelector('.main__content');
items.addEventListener('click', (e) => {
    let current = e.target;
    if(!current.classList.contains('forum__item')) {
        current = current.offsetParent;
    }

    // console.log(e.target,current.offsetParent, current, e.target.classList)
    if(current.classList.contains('forum__item')) {
        console.log('/' + current.getAttribute('data-href'))
        window.location.href = '/' + current.getAttribute('data-href');
    }
    else if(e.target.offsetParent.classList.contains('comment-del')) {
        const parent = e.target.offsetParent.offsetParent;
        const data_author = parent.getAttribute('data-author');
        const data_id = parent.getAttribute('data-id');

        console.log(e.target.offsetParent)
        postData(`/api/v1/forum/threads?id=${data_id}`, {}, 'DELETE')
            .then((data) => {
                console.log(data);
                renderDefaultThread();
            }).catch((data) => {
                console.error(data);
                console.trace();
            });
    }
});
    

function addNew(title, body) {
    const send = {
        title,
        body
    };

    postData(`/api/v1/forum/threads`, send, 'POST')
        .then((data) => {
            console.log(data);
            renderDefaultThread();
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}

function renderDefaultThread() {
    postData('/api/v1/forum/threads?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            renderThread(data.threads);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultThread();

const input = document.querySelector('.main__inner .search input');
const btn = document.querySelector('.btn');

input.addEventListener('input', function() {
    if (input.value.length !== 0) {
        btn.style.display = 'inline-block'
    } else {
        btn.style.display = 'none';
        renderDefaultThread();
    }
});

btn.addEventListener('click', () => {
    postData(`/api/v1/forum/threads/search?page=1&text=${input.value}`, {}, 'GET')
        .then((data) => {
            console.log(data);
            renderThread(data.threads)
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
});


const main__content = document.querySelector('.main__content');

main__content.addEventListener('click', (e) => {
    
});