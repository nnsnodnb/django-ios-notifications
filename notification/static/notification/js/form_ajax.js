$(function() {
    $('#id_target').attr('onClick', 'change_target()');
    $('#id_target').attr('name', 'target');
})

function change_target() {
    targets = $('input[name="target"]')
    if (targets[0].checked == true) {
        location.href = location.pathname + '?target=' + targets[0].value;
    } else if (targets[1].checked == true) {
        location.href = location.pathname + '?target=' + targets[1].value;
    }
}
