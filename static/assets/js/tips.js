function drawTips(data) {
    console.log(data);
    const wrapper = document.querySelector('.main.tips .main__content');
    wrapper.innerHTML = '';

    data.forEach(post => {
        const pattern = `
        <article class="main__content-item">
            <div class="main__content-item__text">
                <h3>${post.title}</h3>
                <p>${post.body}</p>
            </div>
            <div class="main__content-item__img">
                ${post.img ? ('<img src=' + post.img + ' alt="">') : ''}
            </div>
        </article>
        `;

        wrapper.innerHTML += pattern;
    })
}

function renderDefault() {
	postData('/api/v1/tips?page=1', {}, 'GET')
              .then((data) => {
              	
                console.log(data); // JSON data parsed by `response.json()` call
                drawTips(data.tips);

            }).catch((data) => {
                console.error(data);
                console.trace();
          });
};
renderDefault();


const input = document.querySelector('.main__content-inner .search input');
const btn = document.querySelector('.btn');

    input.addEventListener('input', function() {
      if(input.value.length !== 0) {
        btn.style.display = 'inline-block'
      } else {
        btn.style.display = 'none';
        renderDefault();
      }
    });

   btn.addEventListener('click', () => {
   	postData(`/api/v1/tips/search?page=1&text=${input.value}`, {}, 'GET')
              .then((data) => {
                console.log(data); 
                drawTips(data.tips)
            }).catch((data) => {
                console.error(data);
                console.trace();
            });
   });