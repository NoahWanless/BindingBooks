

let dataFromDjango

document.addEventListener('DOMContentLoaded', function() {
        const djangoDataElement = document.getElementById('django-data');
        if (djangoDataElement) {
            dataFromDjango = JSON.parse(djangoDataElement.textContent);            
            console.log("js got the data");
            console.log(dataFromDjango);
        }
    });


document.getElementById("checkoutbutton").addEventListener("click", function(event){
    console.log(dataFromDjango)
    var book_to_buy = dataFromDjango.product_id;
    console.log("book_to_buy:")
    console.log(book_to_buy)
    var all_owned_books = dataFromDjango.all_books;
    var can_book_be_got = true;
    for (var key in all_owned_books){
        if(all_owned_books[key] == book_to_buy){
            can_book_be_got = false;
            console.log("ah looks like the book cant be gotten, its been found already----")
        }
    }
    console.log("we are done searching for the book")
    if (can_book_be_got){
        //redirect user
        console.log("the book can be gotten")
    } else{
        //dont redirect user and display message
        console.log("HEY YOU CANT BUY THIS YOU ALREADY OWN IT")
    }
    
})


