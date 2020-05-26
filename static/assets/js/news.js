
function drawPosts(data) {
	const parent = document.querySelector('.news .main__content');
	data.forEach(post => {
		const pattern = `
		<article class="main__article">
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
                                <a href="#" class="read-more">Read more...</a>
                            </div>
                            <div class="article__img"><img src="${post.picture}" alt=""></div>
                        </div>
                    </article>
                   `;
                   parent.innerHTML += pattern;
	});

}


postData('http://0.0.0.0:5000/api/v1/news?page=1', {}, 'GET')
              .then((data) => {
                console.log(data); // JSON data parsed by `response.json()` call
                drawPosts(data.posts);

            }).catch((data) => {
                console.error(data);
                console.trace();
            });