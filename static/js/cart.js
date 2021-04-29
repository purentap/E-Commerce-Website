var addToCartButtons = document.getElementsByClassName("update-cart")

for(var i=0; i< addToCartButtons.length ; i++)
{   
    addToCartButtons[i].addEventListener('click',function() //adding event listener for each Add to Cart Button
    {
        var productID = this.dataset.product
        var action = this.dataset.action
        var stock = this.dataset.stock
        console.log('productID: ', productID, 'Action: ', action)
        if(stock >0 ){
            console.log('user:', user) //if not logged in, logs AnonymousUser

            if(user != 'AnonymousUser')
            {   
                updateUserOrderToCart(productID, action)
            }
            else{
                getCookieItems(productID, action)
            }
        }
    })

}

function getCookieItems(productID, action)
{   
    console.log("Not logged in")
    if(action == 'add')
    {   
        if(cart[productID] == undefined)
        {   
            cart[productID] = {'quantity' : 1}
        }
        else{
            cart[productID]['quantity'] = cart[productID]['quantity'] +1 
        }
    }
    else if(action == 'remove')
    {   cart[productID]['quantity'] -=1

        if(cart[productID]['quantity'] <= 0)
        {
            console.log('Removing item')
            delete cart[productID]
        }
    }
    console.log("Cart: " , cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
function updateUserOrderToCart(productID, action)
{   
    console.log("User is logged in, sending data.")

    var url = '/update-item/'

    fetch(url, {
        method: 'POST' ,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({
            'productID': productID,
            'action' : action
        })
    })

    .then((response) => {   
        return response.json()
    })

    .then((data) => {   
        console.log('data: ', data)
        location.reload()
    })
}