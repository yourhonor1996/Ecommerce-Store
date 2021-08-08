var updateBtns = document.getElementsByClassName('update-cart')
var cart_total = document.getElementById('cart-total')

refreshCartIcon()

for(var i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        // console.log('productId: ', productId, 'Action: ', action)

        // console.log('User: ', user)
        if(user == 'AnonymousUser'){
            // console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action){
    // console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json(); 
    })
    .then((data) => {
        // console.log('Data:', data)
        cart_total.innerHTML = data['cart_item_count']
    });
}


function refreshCartIcon(){
    var url = '/info_query_api/'
    fetch(url, {
        method: 'GET',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        }
    })
    .then((response) => {
        return response.json(); 
    })
    .then((data) => {
        // console.log('Data:', data)
        cart_total.innerHTML = data['cart_item_count']
    });
}