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
)

app_operadores = web.application(urls, locals())

static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
algoritmos_path = os.path.abspath(os.path.dirname(__file__)) + '/algoritmos/operadores_m'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template/operadores_m'
img_path = os.getcwd() + '/images/'
htmlout = web.template.render(template_dir, base='layout')
render_plain = web.template.render('template/operadores_m')
global message
message = ''


def variables_locales():
    web.template.Template.globals['render'] = render_plain
    web.template.Template.globals['msg'] = message
    web.template.Template.globals['css'] = Layout_main().main_css
    web.template.Template.globals['js'] = Layout_main().main_js


app_operadores.add_processor(web.loadhook(variables_locales))


class helper:
    def GET(self):
        raise web.seeother('/')


class Index:
    def GET(self):
        return htmlout.index_om()
