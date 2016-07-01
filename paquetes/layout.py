import web, os

template_dir = os.path.abspath(os.path.dirname(__file__)) + '/../template'

class Layout_main:
    def main_css(self):
        out = web.template.frender(template_dir + '/css.html')
        return out()

    def integrantes(self):
        out = web.template.frender(template_dir + '/integrantes.html')
        return out()


class Layout_rf:
    def main_css(self):
        return "<hr>HOLA<hr>"
