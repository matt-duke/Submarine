console.log('SocketIO')

// SETUP
// Classes
class Sensor {
    constructor(name) {
        this.name = name;
        this.value = 0;
        this.valid = false;
    }
    set(value, valid) {
        this.value = value;
        this.valid = valid;
    }
};

class DataSubscription {
    constructor(object) {
        this.object = $(object)
        this.equation = object.dataset['subscribe'];
        this.value = null;
        
        var keys = Object.keys(sensors)
        for(var i = 0; i < keys.length; i++) {
            if (this.equation.includes(keys[i])) {
                this.equation = this.equation.replace(new RegExp(keys[i], "g"), 'sensors["'+keys[i]+'"].value');
                console.log(this.equation)
            }
        };
    };
    update() {
        try {
            this.value = eval(this.equation)
        }
        catch(e) {
            console.log('Error on: '+this.equation)
        };
        if (this.object.hasClass('progress-bar')) {
            this.object.show()
            this.value = Math.round(this.value*100)
            if (this.value < 5) {
                this.object.hide()
            }
            this.object.css('width', this.value+'%')
            this.object.attr('aria-valuenow',this.value)
        };
    };
}
// VARIABLES
var subscribers = [];
var sensors = {};

// SOCKET IO
const socket = io.connect('/io');

socket.on('refresh', function(msg) {
    for(i = 0; i < subscribers.length; i++) {
        subscribers[i].update()
    };
});

socket.on('sensor-list', function(msg){
    console.log(msg)
    //Define sensors
    for(var i=0; i < msg.length; i++) {
        sensors[msg[i]] = new Sensor(msg[i])
    }
    $('[data-subscribe]').each(function(i, obj) {
        console.log($(obj))
        subscribers[i] = new DataSubscription(obj)
    });
});

socket.on('update', function(msg){
    sensors[msg.id].set(msg.data.value, msg.data.valid)
});