
import webapp2 as webapp
import logging
import sys
import urllib2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import urlfetch


class Raspping():

    def sendSMS(self, state):
        '''
        Sends a SMS with the given state to my phone number
        TODO: Add Time
        '''

        user = ''
        pw = ''
        msg = 'SSH%20is%20' + state + '!'

        url = 'https://smsapi.free-mobile.fr/sendmsg?user=' + user + '&pass=' + pw + '&msg=' + msg

        urllib2.urlopen(url)

    def getState(self, host, port):
        '''
        Determines the current state of the given host and port.
        To check which ports are available check : 
        https://developers.google.com/appengine/docs/python/urlfetch/?csw=1#Python_Making_requests
        '''
        s = 'down'
        try:
            request = urllib2.Request('http://' + host + ':' + port)
            request.get_method = lambda: 'HEAD'

            response = urllib2.urlopen(request)
            s = 'up'
        except:
            if "An error occured while connecting to the server: Malformed HTTP reply received from server at URL" in str(sys.exc_info()[1]):
                s = 'up'
            else:
                s = 'down'

        return s


class Check(webapp.RequestHandler):

    def get(self):

        tools = Raspping()

        lastMemcacheState = memcache.get('state')
        currentState = tools.getState('', '')

        if (lastMemcacheState == None):
            if currentState == 'down':
                tools.sendSMS(currentState)
            memcache.set('state', currentState)
        else:
            if (currentState != lastMemcacheState):
                tools.sendSMS(currentState)
                memcache.set('state', currentState)

app = webapp.WSGIApplication([
    ('/', Check),
], debug=True)


def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
