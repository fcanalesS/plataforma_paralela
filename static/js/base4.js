var suma = document.getElementById('suma');
noUiSlider.create(suma, {
    start: 1,
    range: {'min': 0, 'max': 100},
    step: 1
});

suma.noUiSlider.on('end', function (values) {
    jQuery.ajax({
        method: 'GET',
        url: '/movimiento/suma',
        data: {value: parseInt(values)}
    }).success(function (result) {
        if (result == 'None'){
            jQuery('#imagen1').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('#imagen1').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});