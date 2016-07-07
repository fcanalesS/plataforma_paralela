import os, sys, web
from realzado_filtrado import app_realzadoFiltrado
from mejora import app_mejora
from op_mate import app_operadores

include_dirs = ['paquetes']

for dirname in include_dirs:
    sys.path.append(os.path.dirname(__file__) + '/' + dirname)

from layout import Layout_main, Formularios

urls = (
    '/', 'Index',
    '/form2', 'Form2',
    '/realzado-imagen', app_realzadoFiltrado,
    '/mejora', app_mejora,
    '/operadores-matematicos', app_operadores,
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
    web.template.Template.globals['js'] = Layout_main().main_js
    web.template.Template.globals['integrantes'] = Layout_main().integrantes
    web.template.Template.globals['form1'] = Formularios().form1
    web.template.Template.globals['form2'] = Formularios().form2


app.add_processor(web.loadhook(variables_locales()))


class MyApp(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('127.0.0.1', port))  # La magia


class Index:
    def GET(self):
        return htmlout.index()

    def POST(self):
        x = web.input(imagen={})
        filedir = static_dir + '/img'  # change this to the directory you want to store the file in.
        if 'imagen' in x:  # to check if the file-object is created
            filepath = x.imagen.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            if filename.split('.')[-1] == 'jpg' or filename.split('.')[-1] == 'png':
                filename1 = '001.jpg'
                fout = open(filedir + '/' + filename1, 'w')  # creates the file where the uploaded file should be stored
                fout.write(x.imagen.file.read())  # writes the uploaded file to the newly created file.
                fout.close()  # closes the file, upload complete.
                os.system('mv ' + filedir + '/' + filename1 + ' ' + filedir + '/' + '001.jpg')
                if x.imagen1 == 'realzado-filtrado':
                    raise web.seeother('/realzado-imagen/')
                elif x.imagen1 == 'mejora':
                    raise web.seeother('/mejora/')
                elif x.imagen1 == 'matematica':
                    raise web.seeother('/operadores-matematicos/')
            else:
                global message
                message = 'No se acepta este tipo de archivos, intente nuevamente ! ! !'
                raise web.seeother('/')

if __name__ == '__main__':
    app = MyApp(urls, globals())
    app.run()
