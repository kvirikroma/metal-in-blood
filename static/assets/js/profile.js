const user_id = sessionStorage.getItem("user_id");
const name = sessionStorage.getItem("current_user");

draw_profile();

function draw_profile()
{
    var pic_src = "";
    postData(`/api/v1/user?id=${user_id}`, {}, 'GET')
    .then((data) => {
        console.log(data);
        pic_src += data.account_picture;

    }).catch((data) => {
        console.error(data);
        console.trace();
    });

    var first = "";
    var second = "";
    var i = 0;

    for (; i < name.length / 2; i++) {
        first += name[i];
    }
    for (; i < name.length; i++) {
        second += name[i];
    }

    const parrent = document.querySelector('.profile .main__content');
    parrent.innerHTML = '';
    const pattern = `
    <p><img src="${pic_src}" width="300" height="300"></p>
    <p><span style="font-family: 'Doom-L'; font-size: 32pt">${first}</span><span style="font-family: 'Doom-R'; font-size: 32pt">${second}</span></p>

    `;
    parrent.innerHTML += pattern;
}
