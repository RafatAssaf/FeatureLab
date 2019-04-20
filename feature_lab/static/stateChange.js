// handle feature request state change
var handleStateChange = function(state, id) {
    console.log(state, id)
    $.ajax({
        url: '/request/' + id + '/update_state',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({ state: state })
    }).done(function(res) {
        $("body").html(res)
    }).fail(function(e) {
        console.log(e);
    });
}