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
    '/mejora-brillo', 'MejoraBrillo',
    '/mejora-contraste', 'MejoraContraste',
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


class MejoraBrillo:
    def GET(self):
        brillo = (float(web.input().brillo) + 100) / 100
        os.system('mpiexec -np %s python %s/brillo.py %s' % (p, algoritmos_path, brillo))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class MejoraContraste:
    def GET(self):
        contraste = (float(web.input().contraste) + 100) / 100
        os.system('mpiexec -np %s python %s/brillo.py %s' % (p, algoritmos_path, contraste))
        # os.system('mpiexec -np %s python %s/limpieza.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'regionEditada_0.jpg')
        _, data = cv2.imencode('.jpg', img)
        jpg_data = base64.b64encode(data.tostring())

        return jpg_data


class MejoraHDR:
    def GET(self):
        # funcion para borrar weas
        print os.getcwd()

        file = os.listdir(img_path + 'HDR/')[0]
        hdr_file = img_path + 'HDR/' + file
        os.system('unzip %s -d %s' % (hdr_file, img_path + 'HDR/'))
        # despues de descomprimir borrar el .zip

        img_list = os.listdir(img_path + 'HDR/')
        img = cv2.imread(img_path + 'HDR/' + img_list[0], cv2.IMREAD_COLOR)
        alt, ancho, canales = img.shape

        for i in range(1, len(img_list)):
            img_aux = cv2.imread(img_path + 'HDR/' + img_list[i], cv2.IMREAD_COLOR)
            aux_alt, aux_ancho, _ = img_aux.shape
            if alt == aux_alt and ancho == aux_ancho:
                pass
                if img_list[0].split('.')[-1] == img_list[i].split('.')[-1]:
                    pass
            else:
                return "NO OK"

        os.system('mpiexec -np %s python %s/hdr.py' % (p, algoritmos_path))

        img = cv2.imread(img_path + 'HDR/hdr.jpg', cv2.IMREAD_COLOR)
        _, data = cv2.imencode('.jpg', img)
        jpg_base64 = base64.b64encode(data.tostring())

        return jpg_base64

    def POST(self):
        x = web.input(myfile={})
        filedir = os.getcwd() + '/images/HDR'  # change this to the directory you want to store the file in.
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
