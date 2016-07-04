/**
 * Created by fcanales on 01-07-16.
 */
jQuery('#subir-imagen').click(function () {
    console.log(1)
    jQuery('.upload-file').toggle()
});

jQuery('#autocorreccion').click(function () {
    jQuery.get('/realzado-imagen/autocorreccion', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

jQuery('#invertir').click(function () {
    jQuery.get('/realzado-imagen/invertir', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

jQuery('#redimensionar').click(function () {
    jQuery.get('/realzado-imagen/redimensionar', function (result) {
        //jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        alert('No implementado')
    })
});

jQuery('#convolucion').click(function () {
    jQuery.get('/realzado-imagen/convolucion', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

//*************************************************************************************

var enfoque_desenfoque = document.getElementById('enfoque-desenfoque');
noUiSlider.create(enfoque_desenfoque, {
    start: 0,
    range: {'min': -100, 'max': 100},
    step: 1
});

enfoque_desenfoque.noUiSlider.on('end', function (values, handle) {
    jQuery.ajax({
        method: 'get',
        url: '/realzado-imagen/enfoque-desenfoque',
        data: {e_d: parseInt(values)}
    }).success(function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});