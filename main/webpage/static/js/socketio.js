var socket = io.connect('http://' + document.domain + ':' + location.port);
var map
socket.on('connect', function() {
    console.log('connected')
    socket.emit('get_map')
});

socket.on('get_map', (data) => {
    map = data
    console.log(map)
});

function take_photo() {
    socket.emit(map[1])
}
