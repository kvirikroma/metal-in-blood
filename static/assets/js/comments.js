
const params = {};
getParams();
function getParams() {
	
	const url = window.location.search.replace( '?', '');
	const arrayParams = url.split('&');

	console.log(arrayParams);

	arrayParams.forEach(param => {
		const parameter = param.split('=');
		[parameter_name, parameter_value] = parameter;

		params[parameter_name] = parameter_value;
	});
}


function renderCommets(data) {
	const parent = document.querySelector('.comments .comment__main');
	parent.innerHTML = null;
    data.forEach(comment => {
        const pattern = `
                    <div class="comment__item" data-author="${comment.author}" data-id="${comment.message_id}">
                            <p>${comment.body}</p>
                            <div class="comment__info">
                                <div class="username">${comment.author}</div>
                                <p class="date">${timeConverter(comment.date)}</p>
                            </div>
                            <p class="comment-del">Delete</p>
                        </div>
        `;
        parent.innerHTML += pattern;
    });
    if(data.length == 0) {
    	const pattern = '<h4 class="nobody">Nobody comment this.</h4>';
    	parent.innerHTML += pattern;
    } else {
    	if(document.querySelector('.nobody')) document.querySelector('.nobody').remove();
    }

    const items = parent.querySelectorAll('.comment__item');
    const currentSession = sessionStorage.getItem('current_user'); 
    items.forEach(comment => {
    	if(comment.getAttribute('data-author') === currentSession) {
    		comment.classList.add('active');
    	}
    })
}


function renderDefaultComms() {
	console.log(`http://0.0.0.0:5000/api/v1/forum/messages?page=${params.page}&id=${params.id}`)
    postData(`http://0.0.0.0:5000/api/v1/forum/messages?page=${params.page}&id=${params.id}`, {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            renderCommets(data.messages);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultComms();



function renderThread(data) {
	const parent = document.querySelector('.comments .main__article');

    
        const pattern = `
                   <div class="article__info">
                            <img src="https://img.favpng.com/12/24/4/heavy-metal-music-hard-rock-microphone-sound-png-favpng-6dhU4fDSgaHBj2VgGeQw3XK1F.jpg" alt="">
                            <div>
                                <p class="username">${data.author}</p>
                                <p class="date">${timeConverter(data.date)}</p>
                            </div>
                        </div>
                        <div class="article__main">
                            <div class="article__text">
                                <h3>${data.title ? data.title : ''}</h3>
                                <p>${data.body}</p>
                            </div>
                        </div>
        `;
        parent.innerHTML = pattern;
}
function renderDefaultThread() {
    postData('http://0.0.0.0:5000/api/v1/forum/threads?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            const need = data.threads.find(el => el.thread_id == params.id)
            renderThread(need);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultThread();

function timeConverter(date){
	date = date + '';
	let days = date.split('T')[0].split('-').reverse().join('.');
	let time = date.split('T')[1].split('.')[0];

	days = days.slice(0, days.length - 2);
	time = time.slice(0, time.length - 3);
  	const str = days + ' ' + time;

  	return str;
}

const addFormTrigger = document.querySelector('.add-new');
const addForm = document.querySelector('.add-new__form');

addForm.addEventListener('submit', (e) => {
    e.preventDefault();
    addNew(addForm.body.value);
    console.log(addForm.body.value);
});

addFormTrigger.addEventListener('click', function() {
    this.classList.toggle('active');
    addForm.classList.toggle('active');

    this.classList.contains('active') ? this.textContent = 'Скрыть' : this.textContent = 'Добавить комментарий';

    
});

function addNew(body) {
	const related_to = params.id;

    const send = {
        body,
        related_to
    };

    postData(`http://0.0.0.0:5000/api/v1/forum/messages`, send, 'POST')
        .then((data) => {
            console.log(data);
            renderDefaultComms();
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}

const main__content = document.querySelector('.comment__main');

main__content.addEventListener('click', (e) => {
    if(e.target.classList.contains('comment-del')) {
        const parent = e.target.offsetParent;
        const data_author = parent.getAttribute('data-author');
        const data_id = parent.getAttribute('data-id');

        console.log(parent, data_id, data_author)
        postData(`http://0.0.0.0:5000/api/v1/forum/messages?id=${data_id}`, {}, 'DELETE')
            .then((data) => {
                console.log(data);
                renderDefaultComms();
            }).catch((data) => {
                console.error(data);
                console.trace();
            });
    }
});