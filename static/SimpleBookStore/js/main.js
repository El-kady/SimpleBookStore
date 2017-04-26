$('.ui.rating')
    .rating({
        maxRating: 5,
        onRate: function (value) {
            var book_id = $(this).data('id');
            $.post(urls.rate, {book_id: book_id, value: value}, function (response) {
                console.log(response)
            }, 'json')
        }
    });
$('.ui.dropdown')
    .dropdown()
;