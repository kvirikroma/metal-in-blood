const user_id = sessionStorage.getItem("user_id");
const name = sessionStorage.getItem("current_user");

draw_profile();

function draw_profile()
{
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
    <img>
    <font style="font-family: 'Doom-L'; font-size: 30pt">${first}</font><font style="font-family: 'Doom-R'; font-size: 30pt">${second}</font>
    `;
    parrent.innerHTML += pattern;
}
