console.log('SocketIO')
const socket = io.connect('/io');

function refresh(msg) {
    object = $('[data-subscribe="'+msg.id+'"]');
    if (typeof object !== 'undefined') {
        if (object.hasClass("progress-bar")) {
            console.log('Changing progress bar width: '+msg.id+': '+msg.data.value+'%')
            object.css('width', msg.data.value);
        }
    }
    if (typeof gage_dict["gauge-"+msg.name] !== 'undefined') {
        var val = ((msg.value == null) ? 0 : msg.data.value);
        console.log(val)
        gage_dict["gauge-"+msg.name].refresh(msg.data.value)
    }
};

var socketMethods = {
    refresh:function(msg){
        refresh(msg);
    },
    test:function(msg){
        console.log("socket.test");
    }
}

function makeOn(key) {
  return function(msg) {
    socketMethods[key].call(socket, msg);
  }
}

socket.on('sensor-list', function(msg){
    console.log(msg)
    for(key in socketMethods){
        socket.on(key, makeOn(key));
    }
});