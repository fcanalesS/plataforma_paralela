import web, os, sys, numpy as np, cv2, base64

p = 4
include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main, Opciones

urls = (
    '', 'helper',
    '/', 'Index',
    #  Urls ajax para el proceso de imagen
    '/autocorreccion', 'AutoCorreccion',
    '/invertir', 'Invertir',
    '/redimensionar-nearest', 'RedimensionarNearest',
    '/redimensionar-bicubic', 'RedimensionarBicubic',
    '/redimensionar-bilineal', 'RedimensionarBilineal',
    '/convolucion', 'Convolucion',
    '/enfoque-desenfoque', 'EnfoqueDesenfoque',
    '/espejo', 'Espejo',
    '/luminosidad', 'Luminosidad',
    '/polar', 'Polar',
    '/bezier', 'Bezier',
    '/posicionar-bordes', 'PosicionarBordes',
    '/deformacion-malla', 'DeformacionMalla',
    '/inversion-colores', 'InversionColores',
    '/escala-grises', 'EscalaGrises',
    '/sepia', 'EfectoSepia',
    '/rgb', 'EfectoRgb',
    '/log', 'EfectoLog',
    '/efecto-3d-de-imagenes-2d', 'Efecto3Dsobre2D',
    '/zooming', 'EfectoZooming',

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
    web.template.Template.globals['op1'] = Opciones().op1
    web.template.Template.globals['op2'] = Opciones().op2
    web.template.Template.globals['op3'] = Opciones().op3
    web.template.Template.globals['op4'] = Opciones().op4


app_realzadoFiltrado.add_processor(web.loadhook(variables_locales))


class helper:
    def GET(self):
        raise web.seeother('/')


########  Procesamiento de imagenes  ########

class AutoCorreccion:
    def GET(self):
        os.system('mpiexec -np %s python %s/automejora.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Invertir:
    def GET(self):
        os.system('mpiexec -np %s python %s/espejo.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class RedimensionarNearest:
    def GET(self):
        ancho, alto = int(web.input().ancho), int(web.input().ancho)
        os.system('mpiexec -np %s python %s/nearest.py %s %s' % (p, algoritmos_path, ancho, alto))
        # cambiar por 'mpirun -np %s --hostfile /home/paralelas/hostfile python %s/nearest.py %s %s' % (p, algoritmos_path, ancho, alto)

        try:
            img = cv2.imread(img_path + 'REDIMENCION_NEAREST.jpg')
            _, data = cv2.imencode('.jpg', img)
            jpg_data = base64.b64encode(data.tostring())

            return jpg_data
        except:
            print "ERROR"


class RedimensionarBicubic:
    def GET(self):
        ancho, alto = web.input().ancho, web.input().alto
        os.system('mpiexec -np %s python %s/bicubic.py %s %s' % (p, algoritmos_path, ancho, alto))
        # cambiar por 'mpirun -np %s --hostfile /home/paralelas/hostfile python %s/bicubic.py %s %s' % (p, algoritmos_path, ancho, alto)

        try:
            img = cv2.imread(img_path + 'REDIMENCION_BICUBIC.jpg')
            _, data = cv2.imencode('.jpg', img)
            jpg_data = base64.b64encode(data.tostring())

            return jpg_data
        except:
            print "ERROR"


class RedimensionarBilineal:
    def GET(self):
        ancho, alto = web.input().ancho, web.input().alto
        os.system('mpiexec -np %s python %s/bilineal.py %s %s' % (p, algoritmos_path, ancho, alto))
        #cambiar por 'mpirun -np %s --hostfile /home/paralelas/hostfile python %s/bilineal.py %s %s' % (p, algoritmos_path, ancho, alto)

        try:
            img = cv2.imread(img_path + 'REDIMENCION_BILINEAL.jpg')
            _, data = cv2.imencode('.jpg', img)
            jpg_data = base64.b64encode(data.tostring())

            return jpg_data
        except:
            print "ERROR"


class Convolucion:
    def GET(self):
        os.system('mpiexec -np %s python %s/convolucion.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class EnfoqueDesenfoque:
    def GET(self):
        value = int(web.input().e_d)

        if value < 0:
            os.system('mpiexec -np %s python %s/sharp.py %s' % (p, algoritmos_path, abs(value)))
            os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))
        elif value > 0:
            os.system('mpiexec -np %s python %s/blur.py %s' % (p, algoritmos_path, abs(value)))
            os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Espejo:
    def GET(self):
        os.system('mpiexec -np %s python %s/mirror.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))
        # limpiar

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Polar:
    def GET(self):
        os.system('mpiexec -np %s python %s/polar.py' % (p, algoritmos_path))

        #limpiar

        img = cv2.imread(img_path + 'polar.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class Bezier:
    def GET(self):
        return NotImplemented


class PosicionarBordes:
    def GET(self):
        os.system('mpiexec -np %s python %s/bordes.py' % (p, algoritmos_path))

        try:
            img = cv2.imread(img_path + 'BORDE_PARALELO.jpg')
            _, data = cv2.imencode('.jpg', img)
            jpg_data = base64.b64encode(data.tostring())

            return jpg_data
        except:
            print "ERROR"


class DeformacionMalla:
    def GET(self):
        return NotImplemented


class InversionColores:
    def GET(self):
        os.system('mpiexec -np %s python %s/negativo.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class EscalaGrises:
    def GET(self):
        os.system('mpiexec -np %s python %s/grises.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class EfectoSepia:
    def GET(self):
        os.system('mpiexec -np %s python %s/sepia.py' % (p, algoritmos_path))
        os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class EfectoRgb:
    def GET(self):
        os.system('mpiexec -np %s python %s/rgb.py' % (p, algoritmos_path))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        try:
            img = cv2.imread(img_path + 'rgbout.jpg')
            _, data = cv2.imencode('.jpg', img)
            jpg_data = base64.b64encode(data.tostring())

            return jpg_data
        except:
            print "ERROR"


class EfectoLog:
    def GET(self):
        os.system('mpiexec -np %s python %s/log_ri.py' % (p, algoritmos_path))
        img = cv2.imread(img_path + 'Logfinal.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


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
