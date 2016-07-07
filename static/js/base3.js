jQuery('#fft').click(function () {
    jQuery.get('/operadores-matematicos/fft', function (result) {
        if (result == 'None'){
            jQuery('#imagen').html('<div class="alert alert-danger text-center" role="alert">' +
                'Ha ocurrido un error en la plataforma paralela. ' +
                '<strong>No se ha podido procesar la imagen</strong>' +
                '</div>')
        }
        else{
            jQuery('#imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
        }
    })
});

jQuery('#laplace').click(function () {
   jQuery.get('/operadores-matematicos/log', function (result) {
        jQuery('#imagen').html('<img class="img img-responsive" src="data:images/jpeg;base64,'+ result + '" alt="">')
    })
});