function filterBooksByAvailability(e) {
    console.log(e)
    e.preventDefault()
    changeButtonName()
}

fetchBooks()

function changeButtonName() {

    if (document.cookie == "view-state=show" || document.querySelector(".book-display-control").innerHTML == "Hide Checked Out Books") {
         document.querySelector(".book-display-control").innerHTML = "Show Checked Out Books"
         let hiddenBooks = document.querySelectorAll(".checked-out")
         hiddenBooks.forEach(function(book) {
            book.classList.add("hidden")
         })
    }
    else {
        document.querySelector(".book-display-control").innerHTML = "Hide Checked Out Books"
        let hiddenBooks = document.querySelectorAll(".checked-out")
        hiddenBooks.forEach(function(book) {
            book.classList.remove("hidden")
            console.log("added hidden:")
            console.log(book.classList)
        })
        //deletes show cookie when we want to hide checked out books
        document.cookie = "view-state=show; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
    }
};

function fetchBooks() {
    fetch('/getbooks/all')
    .then(response => response.json())
    .then((data) => {

       document.getElementById('book-holder').innerHTML += '';

       for (index in data) {
            book = data[index]
            console.log(book)
            console.log(book.title)
            let html = ``
            if (book.available == 1) {
                html += `<div class="book">`
            } else {
                html += `<div class="book checked-out hidden">`
            }

            html += `<p>` + book['title'] + `</p>`
            html += `<p>` + book['author'] + `</p>`
            html += `<p>` + book['year'] + `</p>`
            html += `<p>` + book['name'] + `</p>`
            html += `<form availability="${book.available}" action="/setavail", method="post">`

            if (book.available == 1) {
                html += `<input style="display: none;" class="hidden" name="book_id" type="text" value="` + book.book_id + `" hidden>
                            <input style="display: none;" class="hidden" name="availability" type="text" value="0" hidden>
                            <input type="submit" value="Check Out" class="check-btn">`
            } else {
               html += `<input style="display: none;" class="hidden" name="book_id" type="text" value="` + book.book_id + `" hidden>
                            <input style="display: none;" class="hidden" name="availability" type="text" value="1" hidden>
                            <input type="submit" value="Check In" class="check-btn">`
            }
            html += `</form></div>`
            document.getElementById('book-holder').innerHTML += html;
       }
       changeButtonName()
    })
}
