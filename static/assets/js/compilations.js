function renderAlbums(data) {
const parent = document.querySelector('.comp .main__albums-content');
parent.innerHTML = null;

    data.forEach(album => {
        const pattern = `
                    <div class="main__item">
                        <a href="${album.link}" style="color:white">
                            <div><p>${album.author} - ${album.title}</p></div>
                            <img src="${album.picture}" alt="">
                        </a>
                    </div>
        `;
        parent.innerHTML += pattern;
    });

}
function renderDefaultAlbums() {
    postData('/api/v1/compilations/albums?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            renderAlbums(data.albums);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultAlbums();

function renderComp(data) {
const parent = document.querySelector('.comp .main__random .main__albums-content');
    parent.innerHTML = null;

    data.forEach(comp => {
        const pattern = `
                    <div class="main__item">
                        <a href="${comp.link}" style="color:white">
                            <div style="display:flex; flex-direction: column;">
                            <p style="font-size: 20px">${comp.channel}</p>
                            <p>${comp.video_name}</p>
                            </div>
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQil5hfR-TPbe5IvxA_qvx9VUG7p3kYfpMU6C6odqnVKl7fWehK&usqp=CAU" alt="">
                        </a>
                    </div>
        `;
        parent.innerHTML += pattern;
    });

}
function renderDefaultComp() {
    postData('/api/v1/compilations/yt?page=1', {}, 'GET')
        .then((data) => {
            console.log(data); // JSON data parsed by `response.json()` call
            renderComp(data.compilations);

        }).catch((data) => {
            console.error(data);
            console.trace();
        });
}
renderDefaultComp();


const input1 = document.querySelector('.main__albums .search input');
const btn1 = document.querySelector('.main__albums .search .btn');

input1.addEventListener('input', function() {
    if (input1.value.length !== 0) {
        btn1.style.display = 'inline-block'
    } else {
        btn1.style.display = 'none';
        renderDefaultAlbums();
    }
});

btn1.addEventListener('click', () => {
    postData(`/api/v1/compilations/albums/search?page=1&text=${input1.value}`, {}, 'GET')
        .then((data) => {
            console.log(data);
            renderAlbums(data.albums)
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
});

const input = document.querySelector('.main__random .search input');
const btn = document.querySelector('.main__random .btn');

input.addEventListener('input', function() {
    if (input.value.length !== 0) {
        btn.style.display = 'inline-block'
    } else {
        btn.style.display = 'none';
        renderDefaultComp();
    }
});

btn.addEventListener('click', () => {
    postData(`/api/v1/compilations/yt/search?page=1&text=${input.value}`, {}, 'GET')
        .then((data) => {
            console.log(data);
            renderComp(data.compilations)
        }).catch((data) => {
            console.error(data);
            console.trace();
        });
});
