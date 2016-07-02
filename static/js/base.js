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