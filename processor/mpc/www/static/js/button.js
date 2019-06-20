var options = {
    zone: document.getElementById('joystick'),
    mode: 'dynamic',
    position: {
        top: 0,
        left: '100%'
    }
};
var manager = nipplejs.create(options);

function run(target, id = null, vars=null) {
    console.log(vars)
    $.get($SCRIPT_ROOT + target, vars, function (data) {
        if (id != null) {
            $(id).text = data
        }
        console.log('AJAX: ' + data)
        return data;
    });
}