import web, os

template_dir = os.path.abspath(os.path.dirname(__file__)) + '/../template'
template_dir_rf = os.path.abspath(os.path.dirname(__file__)) + '/../template/realzado_filtrado'

class Layout_main:
    def main_css(self):
        out = web.template.frender(template_dir + '/css.html')
        return out()

    def main_js(self):
        out = web.template.frender(template_dir + '/js.html')
        return out()

    def integrantes(self):
        out = web.template.frender(template_dir + '/integrantes.html')
        return out()


class Formularios:
    def form1(self):
        out = web.template.frender(template_dir + '/form1.html')
        return out()

    def form2(self):
        out = web.template.frender(template_dir + '/form2.html')
        return out()

class Opciones:
    def op1(self):
        out = web.template.frender(template_dir_rf + '/op1.html')
        return out()

    def op2(self):
        out = web.template.frender(template_dir_rf + '/op2.html')
        return out()

    def op3(self):
        out = web.template.frender(template_dir_rf + '/op3.html')
        return out()

class Layout_rf:
    def main_css(self):
        return "<hr>HOLA<hr>"

