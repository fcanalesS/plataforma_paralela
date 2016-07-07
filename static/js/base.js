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

//*************************************************************************************

jQuery('#negativo').click(function () {
    jQuery.get('/realzado-imagen/inversion-colores', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

jQuery('#grises').click(function () {
    jQuery.get('/realzado-imagen/escala-grises', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

jQuery('#sepia').click(function () {
    jQuery.get('/realzado-imagen/sepia', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});


var nearest = document.getElementById('nearest');
noUiSlider.create(nearest, {
    start: 0,
    range: {'min': 0, 'max': 100},
    step: 2
});

nearest.noUiSlider.on('end', function (values) {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-nearest',
        data: {'valor': parseInt(values)}
    }).success(function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

var bicubic = document.getElementById('bicubic');
noUiSlider.create(bicubic, {
    start: 0,
    range: {'min': 0, 'max': 100},
    step: 2
});

bicubic.noUiSlider.on('end', function (values) {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-nearest',
        data: {'valor': parseInt(values)}
    }).success(function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

var bilineal = document.getElementById('bilineal');
noUiSlider.create(bilineal, {
    start: 0,
    range: {'min': 0, 'max': 100},
    step: 2
});

bilineal.noUiSlider.on('end', function (values) {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-nearest',
        data: {'valor': parseInt(values)}
    }).success(function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

jQuery('#bordes').click(function () {
    jQuery.get('/realzado-imagen/posicionar-bordes', function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

jQuery('#polar').click(function () {
    jQuery.get('/realzado-imagen/polar', function (result) {
        jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});

jQuery('#rgb').click(function () {
    jQuery.get('/realzado-imagen/rgb', function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

jQuery('#log_ri').click(function () {
    jQuery.get('/realzado-imagen/log', function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

jQuery('#espejo').click(function () {
    jQuery.get('/realzado-imagen/espejo', function (result) {
        if (result == 'None'){
            jQuery('.imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('.imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});