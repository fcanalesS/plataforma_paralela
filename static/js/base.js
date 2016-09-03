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

/**********************Nuevo interpolación nearest **************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/

/*Borrar las interpolaciones antiguas y reemplazarla por lo que está dentro de los comentarios*/

var nearest = document.getElementsByClassName('Inear');
for (var i = 0; i < nearest.length; i++) {
    noUiSlider.create(nearest[i], {
        start: 10,
        connect: "lower",
        orientation: "horizontal",
        tooltips: true,
        range: {
            'min': 10,
            'max': 10000
        }
    });
    nearest[i].noUiSlider.on('end', setValueNearest);
}

function setValueNearest() {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-nearest',
        data: {'alto': parseInt(nearest[0].noUiSlider.get()), 'ancho': parseInt(nearest[1].noUiSlider.get())}
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
}
/**********************Nuevo interpolación nearest **************************/

/**********************Nueva interpolación bicubic **************************/
var bicubic = document.getElementsByClassName('Ibic');
for (var i = 0; i < bicubic.length; i++) {
    noUiSlider.create(bicubic[i], {
        start: 10,
        connect: "lower",
        orientation: "horizontal",
        tooltips: true,
        range: {
            'min': 10,
            'max': 10000
        }
    });
    bicubic[i].noUiSlider.on('end', setValueBicubic);
}

function setValueBicubic() {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-bicubic',
        data: {'alto': parseInt(bicubic[0].noUiSlider.get()), 'ancho': parseInt(bicubic[1].noUiSlider.get())}
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
}
/**********************Nueva interpolación bicubic **************************/

/**********************Nueva interpolación bilineal **************************/
var bilineal = document.getElementsByClassName('Ibil');
for (var i = 0; i < bilineal.length; i++) {
    noUiSlider.create(bilineal[i], {
        start: 10,
        connect: "lower",
        orientation: "horizontal",
        tooltips: true,
        range: {
            'min': 10,
            'max': 255
        }
    });
    bilineal[i].noUiSlider.on('end', setValueBilineal);
}

function setValueBilineal() {
    jQuery.ajax({
        method: 'GET',
        url: '/realzado-imagen/redimensionar-bilineal',
        data: {'alto': parseInt(bilineal[0].noUiSlider.get()), 'ancho': parseInt(bilineal[1].noUiSlider.get())}
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
}

var traspuesta = document.getElementById('traspuesta');
noUiSlider.create(traspuesta, {
    start: 0,
    range: {'min': 0, 'max': 270},
    tooltips: true,
    step: 90
});

traspuesta.noUiSlider.on('end', function (values) {
   jQuery.ajax({
        method: 'get',
        url: '/realzado-imagen/traspuesta',
        data: {angle: parseInt(values)}
    }).success(function (result) {
        //document.getElementById('imagen').innerHTML = '<img class="img img-responsive" src="data:images/jpeg;base64,' + result + '">'
       console.log(result)
    })
});

/**********************Nueva interpolación bilineal **************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/
/****************************AGREGAR ESTO ************************************/


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
    console.log('Efecto polar.');
    jQuery.get('/realzado-imagen/polar', function (result) {
        console.log('Efecto polar success.');
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