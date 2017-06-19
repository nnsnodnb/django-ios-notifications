$(function() {
    $('#id_target').attr('onClick', 'change_target()');
    $('#id_target').attr('name', 'target');

    if (sessionStorage.getItem(['send_title'])) {
        $('#id_title').prop('value', sessionStorage.getItem(['send_title']));
        sessionStorage.removeItem(['send_title']);
    }
    if (sessionStorage.getItem(['send_subtitle'])) {
        $('#id_subtitle').prop('value', sessionStorage.getItem(['send_subtitle']));
        sessionStorage.removeItem(['send_subtitle']);
    }
    if (sessionStorage.getItem(['send_body'])) {
        $('#id_body').prop('value', sessionStorage.getItem(['send_body']));
        sessionStorage.removeItem(['send_body']);
    }
    if (sessionStorage.getItem(['send_sound'])) {
        $('#id_sound').prop('value', sessionStorage.getItem(['send_sound']));
        sessionStorage.removeItem(['send_sound']);
    }
    if (sessionStorage.getItem(['send_badge'])) {
        $('#id_badge').prop('value', sessionStorage.getItem(['send_badge']));
        sessionStorage.removeItem(['send_badge']);
    }
    if (sessionStorage.getItem(['send_extra'])) {
        $('#id_extra').prop('value', sessionStorage.getItem(['send_extra']));
        sessionStorage.removeItem(['send_extra']);
    }
});

function change_target() {
    title = $('#id_title').val();
    subtitle = $('#id_subtitle').val();
    body = $('#id_body').val();
    sound = $('#id_sound').val();
    badge = $('#id_badge').val();
    extra = $('#id_extra').val();

    if (title) {
        sessionStorage.setItem(['send_title'], [title]);
    }
    if (subtitle) {
        sessionStorage.setItem(['send_subtitle'], [subtitle]);
    }
    if (body) {
        sessionStorage.setItem(['send_body'], [body]);
    }
    if (sound) {
        sessionStorage.setItem(['send_sound'], [sound]);
    }
    if (badge) {
        sessionStorage.setItem(['send_badge'], [badge]);
    }
    if (extra) {
        sessionStorage.setItem(['send_extra'], [extra]);
    }

    targets = $('input[name="target"]')
    if (targets[0].checked == true) {
        location.href = location.pathname + '?target=' + targets[0].value;
    } else if (targets[1].checked == true) {
        location.href = location.pathname + '?target=' + targets[1].value;
    }
}
