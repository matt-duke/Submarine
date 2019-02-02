var gauge = {}

$('.gauge').each(function(i, obj) {
    data = $(obj).attr('data-gauge').split(',')
    if (data.length < 4) {
        console.log('Invalid data-gauge string length')
    }
    gauge[$(obj).attr('id')] = new JustGage({
        id: $(obj).attr('id'),
        title: data[0],
        label: data[1],
        min: data[2],
        max: data[3]
    });
});