var brillo = document.getElementById('brillo');
noUiSlider.create(brillo, {
    start: 1,
    range: {'min': -100, 'max': 100},
    tooltips: true,
    step: 1
});

brillo.noUiSlider.on('end', function (values) {
   jQuery.ajax({
        method: 'get',
        url: '/mejora/mejora-brillo',
        data: {brillo: parseInt(values)}
    }).success(function (result) {
        document.getElementById('imagen').innerHTML = '<img class="img img-responsive" src="data:images/jpeg;base64,' + result + '">'
       //jQuery('.imagen').html(result)
    })
});


var contraste = document.getElementById('contraste');
noUiSlider.create(contraste, {
    start: 1,
    range: {'min': -100, 'max': 100},
    tooltips: true,
    step: 1
});

contraste.noUiSlider.on('end', function (values) {
   jQuery.ajax({
        method: 'get',
        url: '/mejora/mejora-contraste',
        data: {contraste: parseInt(values)}
    }).success(function (result) {
        document.getElementById('imagen').innerHTML = '<img class="img img-responsive" src="data:images/jpeg;base64,' + result + '">'
    })
});

jQuery('#hdr').click(function () {
    jQuery.get('/mejora/mejora-hdr', function (result) {
        var newWin = window.open("", "Imágen HDR", "width=800, height=600, scrollbars=yes, resizable=yes, tooblar=no");
        newWin.document.write('<img class="img img-responsive" src="data:images/jpeg;base64,' + result + '">');
        //document.getElementById('imagen').innerHTML = '<img class="img img-responsive" src="data:images/jpeg;base64,' + result + '">'
    });
});


