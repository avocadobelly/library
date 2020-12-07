fetch('/getbooks/all')
    .then(response => response.json())
    .then((data) => {
       console.log(data);

       // add event listener to show/hide books button
       document.querySelector(".book-display-control").addEventListener('click', function (e) {
        e.preventDefault()
        changeButtonName()
       });

       for (index in data) {
            book = data[index]
            console.log(book)
            console.log(book.title)
            let html = ``
            //if show checked out books is clicked --event listener? --
            //then
            //un-hide those books -- turn off hidden
            if (book.available == 1) {
                html += `<div class="book">`
            } else {
                html += `<div class="book checked-out hidden">`
            }

            html += `<p>` + book['title'] + `</p>`
            html += `<p>` + book['author'] + `</p>`
            html += `<p>` + book['year'] + `</p>`
            html += `<p>` + book['name'] + `</p>`
            //Show checked out displays everything
            //Hide unavailable books from view when 'hide checked out books' clicked
            html += `<form action="/setavail", method="post">`

            if (book.available == 1) {
                html += `<input style="display: none;" class="hidden" name="book_id" type="text" value="` + book.book_id + `"hidden>
                            <input style="display: none;" class="hidden" name="availability" type="text" value="0" hidden>
                            <input type="submit" value="Check Out" class="check-btn">`
            } else {
               html += `<input style="display: none;" class="hidden" name="book_id" type="text" value="` + book.book_id + `"hidden>
                            <input style="display: none;" class="hidden" name="availability" type="text" value="1" hidden>
                            <input type="submit" value="Check In" class="check-btn">`
            }
            html += `</form></div>`
            document.getElementById('book-holder').innerHTML += html;
       }
    }
);

function changeButtonName() {
    if (document.querySelector(".book-display-control").innerHTML == "Show Checked Out Books") {
         document.querySelector(".book-display-control").innerHTML = "Hide Checked Out Books"
         let hiddenBooks = document.querySelectorAll(".checked-out")
         hiddenBooks.forEach(function(book) {
            book.classList.remove("hidden")
         })
    }
    else {
        document.querySelector(".book-display-control").innerHTML = "Show Checked Out Books"
        let hiddenBooks = document.querySelectorAll(".checked-out")
        hiddenBooks.forEach(function(book) {
            book.classList.add("hidden")
        })
    }
};


