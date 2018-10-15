var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    console.log('connected')
    //socket.emit('start_video', 'start_video');
    setTimeout(stop_recording, 10*1000)
});

function stop_recording() {
    //socket.emit('stop_video', 'stop_video');
}
