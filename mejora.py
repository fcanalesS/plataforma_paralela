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
    '/mejora-brillo-contraste', 'MejoraBrilloContraste',
    '/mejora-hdr', 'MejoraHDR'
)

app_mejora = web.application(urls, locals())

static_dir = os.path.abspath(os.path.dirname(__file__)) + '/static'
algoritmos_path = os.path.abspath(os.path.dirname(__file__)) + '/algoritmos/mejora'
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/template/mejora'
img_path = os.getcwd() + '/images/'
htmlout = web.template.render(template_dir, base='layout')
render_plain = web.template.render('template/mejora')
global message
message = ''


def variables_locales():
    web.template.Template.globals['render'] = render_plain
    web.template.Template.globals['msg'] = message
    web.template.Template.globals['css'] = Layout_main().main_css
    web.template.Template.globals['js'] = Layout_main().main_js


app_mejora.add_processor(web.loadhook(variables_locales))


class helper:
    def GET(self):
        raise web.seeother('/')


class MejoraBrilloContraste:
    def GET(self):

        brillo = (float(web.input().brillo) + 100) / 100
        contraste = (float(web.input().contraste) + 100) / 100

        print brillo, contraste

        os.system('mpiexec -np %s python %s/bc.py %s %s' % (p, algoritmos_path, contraste, brillo))

        img = cv2.imread(img_path + 'regionEditada_0.jpg', cv2.IMREAD_COLOR)

        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64decode(data.tostring())

        return jpg_data

class MejoraHDR:
    def POST(self):
        x = web.input(myfile={})
        filedir = os.getcwd() + '/images'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            if filename.split('.')[-1] == 'zip':
                fout = open(filedir + '/' + filename, 'w')  # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
                fout.close()  # closes the file, upload complete.
                raise web.seeother('/')
            else:
                global message
                message = 'Error, no se puede trabajar con el formato <strong> %s </strong>' % filename.split('.')[-1]
                raise web.seeother('/')


class Index:
    def GET(self):
        return htmlout.index_m()
