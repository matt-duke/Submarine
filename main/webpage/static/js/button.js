var options = {
    zone: document.getElementById('joystick'),
    mode: 'dynamic',
    position: {
        top: 0,
        left: '100%'
    }
};
var manager = nipplejs.create(options);

function run(target, id = null) {
    $.get($SCRIPT_ROOT + target, {

    }, function (data) {
        if (id != null) {
            $(id).text = data
        }
        console.log('AJAX: ' + data)
    });
    return false;
}
