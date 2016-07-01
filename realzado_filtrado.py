import web, os, sys, numpy as np, cv2

include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main

urls = (
    '', 'helper',
    '/', 'Index'
)

app_realzadoFiltrado = web.application(urls, locals())

static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template/realzado_filtrado'
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

    def POST(self):
        return web.input()


class Index:
    def GET(self):
        return htmlout.index_rf()
