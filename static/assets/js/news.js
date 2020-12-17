function drawPosts(data) {
    const parent = document.querySelector('.news .main__content');
    parent.innerHTML = '';
    data.forEach(post => {
        let pattern = `
        <article class="main__article" data-id="${post.post_id}">
                        <div class="article__info">
                            <img src="https://img.favpng.com/12/24/4/heavy-metal-music-hard-rock-microphone-sound-png-favpng-6dhU4fDSgaHBj2VgGeQw3XK1F.jpg" alt="">
                            <div>
                                <p class="username">${post.author}</p>
                                <p class="date">${post.date.split('-').reverse().join('.')}</p>
                            </div>
                        </div>
                        <div class="article__main">
                            <div class="article__text">
                                ${post.title ? '<h2>' + post.title + '</h2>' : null}
                                ${post.body}
                            </div>
                            <div class="article__img"><img src="${post.picture}" alt=""></div>
                        </div>
                        <p class="del">${voc.delete}</p>
                    </article>
                   `;
        parent.innerHTML += pattern;
    });

}

function renderDefault() {
    postData('/api/v1/news?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            drawPosts(data.posts);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefault();

const input = document.querySelector('.main__content-inner .search input');
const btn = document.querySelector('.btn');

input.addEventListener('input', function() {
    if (input.value.length !== 0) {
        btn.style.display = 'inline-block'
    } else {
        btn.style.display = 'none';
        renderDefault();
    }
});

btn.addEventListener('click', () => {
    postData(`/api/v1/news/search?page=1&text=${input.value}`, {}, 'GET')
        .then((data) => {
            console.log(data);
            drawPosts(data.posts)
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
});

const addFormTrigger = document.querySelector('.add-new');
const addForm = document.querySelector('.add-new__form');

addForm.addEventListener('submit', (e) => {
    e.preventDefault();
    addNew(addForm.heading.value, addForm.body.value, addForm.picture.value);
});

addFormTrigger.addEventListener('click', function() {
    this.classList.toggle('active');
    addForm.classList.toggle('active');

    this.classList.contains('active') ? this.textContent = voc.hide : this.textContent = voc.add_news;

    
});

function addNew(title, body, picture) {
    const send = {
        title,
        body,
        picture
    };

    postData(`/api/v1/news`, send, 'POST')
        .then((data) => {
            console.log(data);
            renderDefault();
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}


const main__content = document.querySelector('.main__content');

main__content.addEventListener('click', (e) => {
    if(e.target.classList.contains('del')) {
        const parent = e.target.offsetParent;
        const data_id = parent.getAttribute('data-id');


        postData(`/api/v1/news?post_id=${data_id}`, {}, 'DELETE')
            .then((data) => {
                console.log(data);
                renderDefault();
            }).catch((data) => {
                console.error(data);
                console.trace();
            });
    }
});