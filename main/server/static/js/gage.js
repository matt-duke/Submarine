//todo: dynamically add gauge from html

$('.gauge').each(function(i, obj) {
    console.log($(obj).attr('id'))
    var g = new JustGage({
        id: $(obj).attr('id')
    });
});

gage_dict = {}
var g = new JustGage({
    id: "depth",
    value: 67,
    min: 0,
    max: 100,
    title: "Depth",
    label: "m"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "voltage",
    value: 5,
    min: 0,
    max: 100,
    title: "Battery",
    label: "V"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "pressure",
    value: 67,
    min: 0,
    max: 100,
    title: "Tank",
    label: "psi"
});
gage_dict[g.config.id] = g;
/*var g = new JustGage({
    id: "cpu",
    value: 67,
    min: 0,
    max: 100,
    title: "CPU"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "mem",
    value: 67,
    min: 0,
    max: 100,
    title: "RAM"
});
gage_dict[g.config.id] = g;*/