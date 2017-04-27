$('.ui.rating').rating({
    maxRating: 5,
    onRate: function (value) {
        var book_id = $(this).data('id');
        $.post(urls.rate, {book_id: book_id, value: value}, function (response) {
            console.log(response)
        }, 'json')
    }
});
$('.ui.dropdown').dropdown();

$('.toggle-follow').each(function () {
    var button = $(this);
    var status = button.data('status');
    if (status === 1) {
        button.text(button.data('undo'));
    } else if (status === 0) {
        button.text(button.data('do'));
    }
});

$(document).on("click", ".toggle-follow", function () {
    var button = $(this);
    var status = +button.attr('data-status') === 1 ? 0 : 1;
    var model = button.data('model');
    var id = button.data('id');

    button.addClass('loading');
    $.post(urls.follow, {model: model, id: id, status: status}, function (response) {
        if (status === 1) {
            button.text(button.data('undo'));
        } else {
            button.text(button.data('do'));
        }
        button.attr('data-status', status);
        button.removeClass('loading');
    }, 'json')
});
