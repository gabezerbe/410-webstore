console.log("JS running")

var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var pID = this.dataset.product
        var btnAction = this.dataset.action
        console.log("pID:", pID, "action:", btnAction)
        console.log('USER:', user)

        if(user == 'AnonymousUser'){
            console.log("No logged in User")
        } else {
            updateUserOrder(pID, btnAction)
        }
    })
}

function updateUserOrder(productID, action){
    console.log("User is logged in, sending Data...")

    var url='/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productID':productID, 'action':action })
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
    })
}