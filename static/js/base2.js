/**
 * Created by fcanales on 04-07-16.
 */


var brillo = document.getElementById('brillo');
noUiSlider.create(brillo, {
    start: 0,
    range: {'min': -100, 'max': 100},
    step: 1
});

brillo.noUiSlider.on('end', function (value, handler) {
    console.log(value)
})

var contraste = document.getElementById('contraste');
noUiSlider.create(contraste, {
    start: 0,
    range: {'min': -100, 'max': 100},
    step: 1
});

contraste.noUiSlider.on('end', function (value, handler) {
    console.log(value)
})