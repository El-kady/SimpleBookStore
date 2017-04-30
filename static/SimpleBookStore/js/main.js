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

$(".book-actions").each(function () {
    var status = $(this).data('status');
    $(this).children().each(function(){
        if ($(this).data("action") === status) {
            $(this).addClass("positive");
        }
    })
});

$(document).on("click", ".book-actions > button", function () {
    var button = $(this);
    var buttons = button.parent();
    buttons.children().each(function () {
        $(this).removeClass("positive")
    });
    var id = buttons.data('id');
    var action = button.data('action');

    button.addClass('loading').prop("disabled", true);
    $.post(urls.book_action, {id: id, action: action}, function (response) {
        buttons.attr("data-status",action);
        button.removeClass('loading').prop("disabled", false).addClass("positive");
    }, 'json')
});

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

    button.addClass('loading').prop("disabled", true);
    $.post(urls.follow, {model: model, id: id, status: status}, function (response) {
        if (status === 1) {
            button.text(button.data('undo'));
        } else {
            button.text(button.data('do'));
        }
        button.attr('data-status', status);
        button.removeClass('loading').prop("disabled", false);
    }, 'json')
});
