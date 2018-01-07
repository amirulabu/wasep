import os.path
import cherrypy
from cherrypy.lib.static import serve_file

class Wasep(object):
    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['number'] = vpath.pop()
            return self
        elif len(vpath) == 2:
            cherrypy.request.params['number'] = vpath.pop(0)
            cherrypy.request.params['text'] = vpath.pop(0)
            return self
        elif len(vpath) > 2:
            raise cherrypy.HTTPRedirect("/")
        return vpath

    @cherrypy.expose
    def index(self, number="none", text="none"):
        if(number != "none" and text == "none"):
            # There are 2 ways to use whatsapp api            
            # whatsapp://send?text=Hai!%20&phone=+60123456789
            # https://api.whatsapp.com/send?phone=60123456789&text=Hai!
            raise cherrypy.HTTPRedirect("https://api.whatsapp.com/send?phone=6%s" % number)
            return "Sending message to %s" % number
        elif(number != "none" and text != "none"):
            raise cherrypy.HTTPRedirect("https://api.whatsapp.com/send?phone=6%s&text=%s" % (number, text))
            return "Sending \"%s\" to %s" % (text,number)
        else:
            return serve_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'index.html'))

config = os.path.join(os.path.dirname(__file__), 'config.conf')

if __name__ == '__main__':
    cherrypy.quickstart(Wasep(), config=config)