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
        }
    })

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
    })
}