import os
import sys

import web

from blog import app_blog
from realzado_filtrado import app_realzadoFiltrado

include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main

urls = (
    '/', 'Index',
    '/blog', app_blog,
    '/realzado-imagen', app_realzadoFiltrado
)

app = web.application(urls, locals())

static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template'
htmlout = web.template.render(template_dir, base='layout')
render_plain = web.template.render('template/')

global message
message = ''


def variables_locales():
    web.config.debug = True
    web.template.Template.globals['render'] = render_plain
    web.template.Template.globals['msg'] = message
    web.template.Template.globals['css'] = Layout_main().main_css
    web.template.Template.globals['integrantes'] = Layout_main().integrantes


app.add_processor(web.loadhook(variables_locales()))


class MyApp(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('127.0.0.1', port))  # La magia


class Index:
    def GET(self):
        print web.ctx.status
        return htmlout.index()


if __name__ == '__main__':
    app = MyApp(urls, globals())
    app.run()
