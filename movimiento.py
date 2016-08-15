import cv2
import web, sys, os, base64

p = 4

include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main

urls = (
    '', 'helper',
    '/', 'Index',
    #  Urls ajax para el proceso de imagen
    '/suma', 'Suma'
)

app_movimiento = web.application(urls, locals())

static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
algoritmos_path = os.path.abspath(os.path.dirname(__file__)) + '/algoritmos/movimiento'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template/movimiento'
img_path = os.getcwd() + '/images/'
htmlout = web.template.render(template_dir, base='layout')
render_plain = web.template.render('template/movimiento')
global message
message = ''


def variables_locales():
    web.template.Template.globals['render'] = render_plain
    web.template.Template.globals['msg'] = message
    web.template.Template.globals['css'] = Layout_main().main_css
    web.template.Template.globals['js'] = Layout_main().main_js


app_movimiento.add_processor(web.loadhook(variables_locales))


class helper:
    def GET(self):
        raise web.seeother('/')


class Suma:
    def GET(self):
        alpha = float(web.input().value)
        os.system('mpiexec -np %s python %s/suma.py %s %s %s' % (p, algoritmos_path, img_path + '/movimiento/suma/001.jpg', img_path + '/movimiento/suma/002.jpg', alpha))

        list_img = os.listdir(img_path + '/movimiento/suma/')

        if 'OUTPUT_0.jpg' in list_img:
            try:
                img = cv2.imread(img_path + '/movimiento/suma/OUTPUT_0.jpg')
                _, data = cv2.imencode('.jpg', img)
                jpg_data = base64.b64encode(data.tostring())

                return jpg_data
            except:
                print "ERROR"
        elif 'OUTPUT_1.jpg' in list_img:
            try:
                img = cv2.imread(img_path + '/movimiento/suma/OUTPUT_1.jpg')
                _, data = cv2.imencode('.jpg', img)
                jpg_data = base64.b64encode(data.tostring())

                return jpg_data
            except:
                print "ERROR"

class Index:
    def GET(self):
        otros_path = img_path + '/movimiento/otros'

        os.system('unzip %s/%s -d %s' % (otros_path, os.listdir(otros_path)[0], otros_path))
        os.system('rm %s/*.zip' % otros_path)

        img_list = os.listdir(otros_path)
        img_list.sort()
        img_aux = cv2.imread(otros_path + '/' + img_list[0], cv2.IMREAD_COLOR)
        h, w, l = img_aux.shape
        count = 1

        for i in range(1, len(img_list)):
            aux = cv2.imread(otros_path + '/' + img_list[i], cv2.IMREAD_COLOR)
            alt, anch, lay = aux.shape
            if alt == h and anch == w:
                count += 1
            else:
                count -= 1
                raise web.seeother('/')

        if count == len(img_list):
            os.system('mpiexec -np %s python %s/bullet.py' % (p, algoritmos_path))
            os.system('mpiexec -np %s python %s/stop.py' % (p, algoritmos_path))
            os.system('mpiexec -np %s python %s/timelapse.py' % (p, algoritmos_path))
        else:
            os.system('rm %s/*.*' % otros_path)

        return htmlout.index_m()
