import webapp2

from ufundy import basehandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world! This is amazing...')
        
class HomeHandler(basehandler.BaseHandler):
    def get(self):
        page_title = 'uFundy - The CrowdFunding Portal'
        page_description = 'uFundy - The CrowdFunding Portal'
        
        context = {'page_title': page_title, \
                    'page_description': page_description}
                    
        self.render_response('public/splash.html', **context)