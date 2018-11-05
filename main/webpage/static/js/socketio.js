var socket = io.connect('http://' + document.domain + ':' + location.port);
var map
socket.on('connect', function() {
    console.log('connected')
    socket.emit('get_msg_map')
    var map_data = [45.273209, -79.416843, 14]
    socket.emit('save_map', map_data)
});

socket.on('get_msg_map', (data) => {
    map = data
    console.log(map)
});

function take_photo() {
    socket.emit(map[1])
}
