var update = document.getElementsByClassName('update-cart')

for(var i=0; i<update.length; i++) {
    update[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action

        console.log('productID:', productID, 'action:', action)
        console.log('USER:', user)
        
        if(user == 'AnonymousUser'){
            addCookie(productID, action)
        }else{
            OrderUser(productID, action)
        }
    })
}

function addCookie(productID, action) {
    console.log('Usuario No Registrado')

    if(action == 'add'){
        if (cart[productID] == undefined ) {
            cart[productID] = {'quantity':1}
        }else{
            cart[productID]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productID]['quantity'] -= 1

        if(cart[productID]['quantity'] <= 0){
            console.log('Sacando Objeto...')
            delete cart[productID]
        }
    }

    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function OrderUser(productID, action) {
    console.log('El Usuario esta Registrado, Enviando Datos...')
    var url = '/update-item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productID':productID, 
            'action':action
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}