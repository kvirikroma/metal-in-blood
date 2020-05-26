

// Динамическое изменение страницы
function controller() { // определяем на какой странице находится пользователь
    const url = location.href;
    const main_url = 'index.html';
    const global_url = url.slice(0, url.lastIndexOf('/') + 1);
    localStorage.setItem('global', global_url)
    let current_url = url.slice(url.lastIndexOf('/') + 1, url.length);
    current_url = current_url.indexOf('#') == -1 ? current_url : current_url.slice(0, current_url.length - 1);
    if(current_url !== main_url) {
        drawMenuButton(document.body);
        drawMenu(document.body);
        drawUser(document.body);
        addListenerOnMenu();
    }
    if(current_url == 'tips.html') {
        connect();
    }
}
controller();


function drawMenuButton(body) {
    const btn = `
        <div class="menu">
            <div></div>
            <div></div>
            <div></div>
        </div>
    `;

    body.innerHTML += btn;
    
}

function drawMenu(body) {
    const user = sessionStorage.getItem('current_user');

    const menu = 
    `
    <div id="menu">
        <div class="menu__controls">
            <div>
                <div class="menu__controls-language"><img src="static/metal-in-blood/lang.png" alt="" class="menu-img"> Select language...</div>
                <div class="menu__controls-login"><img src="static/metal-in-blood/exit.png" alt="" class="menu-img"><span id="wr">${isLogged() ? user + ', ' + '  ' + ' <a href="#" id="logout"> exit</a>' : ' <a href="signin.html">Login</a>'}</span></div>
            </div>
            <div class="menu__controls-arrow"><img src="static/metal-in-blood/arrows.png" alt="" class="menu-img"></div>
        </div>
        <div class="menu__nav">
            <h3>Sections</h3>
            <nav class="main__navigation">
                <a href="news.html">
                    <div class="main__navigation-item">
                        <div class="main__navigation-item__img"><img src="https://thewarriorledger.com/wp-content/uploads/2019/02/william-krause-697816-unsplash-900x600.jpg" alt=""></div>
                        <div class="main__navigation-item__text">News</div>
                    </div>
                </a>
                <a href="tips.html">
                    <div class="main__navigation-item">
                        <div class="main__navigation-item__img"><img src="https://i.pinimg.com/originals/80/62/a2/8062a205dce6229d2f3259c33bfe27ec.jpg" alt=""></div>
                        <div class="main__navigation-item__text">Tips</div>
                    </div>
                </a>
                <a href="compilations.html">
                    <div class="main__navigation-item">
                        <div class="main__navigation-item__img"><img src="https://www.straitstimes.com/sites/default/files/styles/article_pictrure_780x520_/public/articles/2019/03/22/jtoncert220319.jpg?itok=x-woy2uM&timestamp=1553254399" alt=""></div>
                        <div class="main__navigation-item__text">Compilations</div>
                    </div>
                </a>
                <a href="forum.html">
                    <div class="main__navigation-item">
                        <div class="main__navigation-item__img"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQaLO9_p9WGyooVBroRlHgSsDAA6jGuYeQ4ch3CixSr1qZRrizG&usqp=CAU" alt=""></div>
                        <div class="main__navigation-item__text">Forum</div>
                    </div>
                </a>
            </nav>
        </div>
    </div>
    `
    body.innerHTML += menu;
}

function addListenerOnMenu() {
    const btn_outro = document.querySelector('.menu');
    const btn_exit = document.querySelector('.menu__controls-arrow');
    const menu = document.querySelector('#menu');
    [btn_outro, btn_exit].forEach(el => el.addEventListener('click', () => {
        menu.classList.toggle('active');
        console.log('work')
    }));
    if(document.querySelector('#logout')) {
        document.querySelector('#logout').onclick = () => {
            localStorage.removeItem('current_user', JSON.stringify({}));
            document.querySelector('#wr').innerHTML = ' <a href="signin.html">Login</a>';
            document.querySelector('#hello').remove();
        }
    }
    
}

// function drawTips(data) {
//     console.log(data);
//     const wrapper = document.querySelector('.main.tips .main__content');

//     data = JSON.parse(data);
//     data.forEach(post => {
//         const pattern = `
//         <article class="main__content-item">
//             <div class="main__content-item__text">
//                 <h3>${post.title}</h3>
//                 <p>${post.text}</p>
//             </div>
//             <div class="main__content-item__img">
//                 <img src="${post.img}" alt="">
//             </div>
//         </article>
//         `;

//         wrapper.innerHTML += pattern;
//     })
// }

function connect(to = "tips") {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'static/assets/js/tips_db.json');
    xhr.send();
    xhr.addEventListener('readystatechange', () => {
    if (xhr.status === 200 && xhr.readyState == 4) {
        switch(to) {
            case 'tips':
                drawTips(xhr.response)
                return true;
                break
        }
    } else return;
    });
}


function drawUser(body) {
    const user = JSON.parse(localStorage.getItem('current_user'));
    const pattern = `
        <span id="hello">Hello, <b style="color:#8DC714">${user ? user.login : null}</b></span>
    `;

    user ? body.innerHTML += pattern : null;
}



