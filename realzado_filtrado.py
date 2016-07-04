import web, os, sys, numpy as np, cv2, base64

p = 4
include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main

urls = (
    '', 'helper',
    '/', 'Index',
    #  Urls ajax para el proceso de imagen
    '/autocorreccion', 'AutoCorreccion',
    '/invertir', 'Invertir',
    '/redimensionar', 'Redimensionar',
    '/convolucion', 'Convolucion',
    '/enfoque-desenfoque', 'EnfoqueDesenfoque',
    '/espejo', 'Espejo',
    '/luminosidad', 'Luminosidad',
    '/polar', 'Polar',
    '/bezier', 'Bezier',
    '/posicionar-bordes', 'PosicionarBordes',
    '/deformacion-malla', 'DeformacionMalla',
    '/inversion-colores', 'InversionColores',
    '/sepia', 'EfectoSepia',
    '/rgb', 'EfectoRgb',
    '/log', 'EfectoLog',
    '/efecto-3d-de-imagenes-2d', 'Efecto3Dsobre2D',
    '/zooming', 'EfectoZooming'

)

app_realzadoFiltrado = web.application(urls, locals())

algoritmos_path = os.path.abspath(os.path.dirname(__file__)) + '/algoritmos/realzado_mejora'
static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template/realzado_filtrado'
img_path = os.getcwd() + '/images/'
htmlout = web.template.render(template_dir, base='layout')
render_plain = web.template.render('template/realzado_filtrado')
global message
message = ''


def variables_locales():
    web.template.Template.globals['render'] = render_plain
    web.template.Template.globals['msg'] = message
    web.template.Template.globals['css'] = Layout_main().main_css
    web.template.Template.globals['js'] = Layout_main().main_js


app_realzadoFiltrado.add_processor(web.loadhook(variables_locales))


class helper:
    def GET(self):
        raise web.seeother('/')


########  Procesamiento de imagenes  ########

class AutoCorreccion:
    def GET(self):
        os.system('mpiexec -np %s python %s/automejora.py' % (p, algoritmos_path))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Invertir:
    def GET(self):
        os.system('mpiexec -np %s python %s/espejo.py' % (p, algoritmos_path))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Redimensionar:
    def GET(self):
        return NotImplemented


class Convolucion:
    def GET(self):
        os.system('mpiexec -np %s python %s/convolucion.py' % (p, algoritmos_path))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionConvolucion.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class EnfoqueDesenfoque:
    def GET(self):
        value = int(web.input().e_d)

        if value < 0:
            os.system('mpiexec -np %s python %s/sharp.py %s' % (p, algoritmos_path, abs(value)))
            # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))
        elif value > 0:
            os.system('mpiexec -np %s python %s/blur.py %s' % (p, algoritmos_path, abs(value)))
            # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Espejo:
    def GET(self):
        return NotImplemented


class Polar:
    def GET(self):
        return NotImplemented


class Bezier:
    def GET(self):
        return NotImplemented


class PosicionarBordes:
    def GET(self):
        return NotImplemented


class DeformacionMalla:
    def GET(self):
        return NotImplemented


class InversionColores:
    def GET(self):
        return NotImplemented


class EfectoSepia:
    def GET(self):
        return NotImplemented


class EfectoRGB:
    def GET(self):
        return NotImplemented


class EfectoLog:
    def GET(self):
        return NotImplemented


class Efecto3Dsobre2D:
    def GET(self):
        return NotImplemented


class EfectoZooming:
    def GET(self):
        return NotImplemented


########  Procesamiento de imagenes  ########


class Index:
    def GET(self):
        return htmlout.index_rf()
