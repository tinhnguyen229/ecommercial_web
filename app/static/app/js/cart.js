var updateBtns = document.getElementsByClassName('update-cart')
for (i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)
        console.log('user', user)
        if (user === 'AnonymousUser') {
            console.log('User did not log in!')

        } else {
            console.log('You logged in: ', user)
            updateUserOrder(productId, action)
        }
    })
}

//function updateUserOrder(productId, action) {
//    console.log('You logged in, add ', productId, ' successfully.');
//    console.log('You logged in, action ', action);
//    var url = '/update_item/'
//    fetch = (url, {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json',
//        },
//        body: JSON.stringify({'productId': productId, 'action': action})
//    })
//    .then((response) => {
//        return response.json();
//    })
//    .then((data) => {
//        console.log('data', data)
//    });
//};

function updateUserOrder(productId, action) {
    console.log('You logged in, add ', productId, ' successfully.');
    console.log('You logged in, action ', action);
    var url = '/update_item/'
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}),
    };

    fetch(url, fetchOptions)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload()
        console.log('data ', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};