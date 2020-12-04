fetch('/getbooks/available')
    .then(response => response.json())
    .then((data) => {
        console.log(data);
       for (book in data) {
            let html = `<div class="book">`
            html += `<p>` + book.title + `</p>`
            html += `<p>` + book.author + `</p>`
            html += `<p>` + book.year + `</p>`
            html += `<p>` + book.name + `</p>`
            html += `<form action="/setavail", method="post">`
            if (book.available == 1) {
                html += `<input style="display: none;" class="hidden" name="book_id" type="text" value=` + book.book_id + `hidden>
                 <input style="display: none;" class="hidden" name="availability" type="text" value="0" hidden>
                <input type="submit" value="Check Out" class="check-btn">`
            } else {
               html += `<input style="display: none;" class="hidden" name="book_id" type="text" value=` + book.book_id + `hidden>
                            <input style="display: none;" class="hidden" name="availability" type="text" value="1" hidden>
                            <input type="submit" value="Check In" class="check-btn">`
            }
            html += `</form></div>`
            document.getElementById('book-holder').innerHTML = html;
       }
    }
);


