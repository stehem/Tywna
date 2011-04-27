"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators, ValidationError
import os




def checkfile(form, field):
	if not field.file: 
		raise ValidationError('This field is required.') 





class PicUploadForm(wtf.Form):
    PicTitle = wtf.TextField('What you bought:', validators=[validators.Required()])
    PicImage = wtf.FileField('Picture of it:', validators=[checkfile])
    PicWhere = wtf.TextField('Where you bought it:', validators=[validators.Required()])
    PicPrice = wtf.TextField('How much you paid for it:', validators=[validators.Required()])
    PicPoster = wtf.TextField('Your name:', validators=[validators.Required()])

