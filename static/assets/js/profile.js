const name = sessionStorage.getItem("current_user");

get_data();

function draw_profile(pic_source, language)
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
    <div><img src="${pic_source}" width="300" height="300" style="border-radius: 150px;"></div>
    <div><span style="font-family: 'Doom-L'; font-size: 32pt">${first}</span><span style="font-family: 'Doom-R'; font-size: 32pt">${second}</span></div>
    <div>${voc.plang}: ${language}</div>
    `;
    parrent.innerHTML += pattern;
}

function get_data()
{ 
    postData(`/api/v1/user?id=${user_id}`, {}, 'GET')
    .then((data) => {
        console.log(data);
        draw_profile(data.account_picture, data.language);

    }).catch((data) => {
        console.error(data);
        console.trace();
    });    
}
