
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from secretary import Renderer

class MoustacheRender(Renderer):
    def __init__(self, environment=None, **kwargs):
        Renderer.__init__(self, environment=None, **kwargs)
        self.environment.filters['mydate'] = self.mydate
        self.environment.filters['dateformat'] = self.dateFormat

    def mydate(self,value):
        return value


    def dateFormat(self, value, format):
        dt = datetime(2007, 4, 1, 15, 30)
        format_datetime(dt, "yyyyy.MMMM.dd GGG hh:mm a", locale='en')
        #return format_datetime(value, "EEEE, d.M.yyyy", locale='fr')
        #return babel.dates.format_datetime(value, format)
        #return "toto"




    # filtre date

    # nombre en lettre  https://github.com/savoirfairelinux/num2words
    # format de nombre (sépateur espace) cf stringformat python
    #
