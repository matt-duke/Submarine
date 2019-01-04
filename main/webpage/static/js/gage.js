gage_dict = {}
var g = new JustGage({
    id: "gauge-depth",
    value: 67,
    min: 0,
    max: 100,
    title: "Depth",
    label: "m"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "gauge-voltage",
    value: 5,
    min: 0,
    max: 100,
    title: "Battery",
    label: "V"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "gauge-press",
    value: 67,
    min: 0,
    max: 100,
    title: "Tank",
    label: "psi"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "gauge-cpu",
    value: 67,
    min: 0,
    max: 100,
    title: "CPU"
});
gage_dict[g.config.id] = g;
var g = new JustGage({
    id: "gauge-mem",
    value: 67,
    min: 0,
    max: 100,
    title: "RAM"
});
gage_dict[g.config.id] = g;