/**
 * Created by fcanales on 04-07-16.
 */

function setBC() {
    jQuery('#brightInp').val(sliders2[0].noUiSlider.get());
    jQuery('#contrastInp').val(sliders2[1].noUiSlider.get());

}
var sliders2 = document.getElementsByClassName('sliders2');

for (var i = 0; i < sliders2.length; i++) {

    noUiSlider.create(sliders2[i], {
        start: 0,
        step: 1,
        connect: "lower",
        orientation: "horizontal",
        range: {
            'min': -100,
            'max': 100
        }
    });
    sliders2[i].noUiSlider.on('slide', setBC)
}

jQuery('#btn-bc').on('click', function () {
    jQuery.ajax({
        method: 'get',
        url: '/mejora/mejora-brillo-contraste',
        data: {
            brillo: jQuery('#brightInp').val(),
            contraste: jQuery('#contrastInp').val()
        }
    }).success(function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});