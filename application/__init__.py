"""
Initialize Flask app

"""
from google.appengine.ext import db
from google.appengine.api import users, images
from flask import Flask, render_template, redirect, request, make_response
from forms import PicUploadForm
import tzsearch





app = Flask(__name__)

class Purchase(tzsearch.SearchableModel):
    pic_title = db.StringProperty()
    pic_image_thumb = db.BlobProperty(default=None)
    pic_image_large = db.BlobProperty(default=None)
    pic_poster = db.StringProperty()
    pic_price = db.StringProperty()
    pic_where = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)


class Pagination:
	def __init__(self, page, collection):
		PER_PAGE = 30
		page = int(page)
		if page and page != 1:
			self.results = collection.fetch(PER_PAGE, (page - 1) * PER_PAGE)
			if self.has_more(collection, PER_PAGE, page) == True:
				self.next = page + 1
				self.previous = page - 1
			else:
				self.next = False
				self.previous = page - 1
		else:
			self.results = collection.fetch(PER_PAGE)
			page = 1
			if self.has_more(collection, PER_PAGE, page) == True:	
				self.next = page + 1
				self.previous = False
			else:
				self.next = False
				self.previous = False	
	def has_more(self, collection, PER_PAGE, page):
		if len(collection.fetch(PER_PAGE, (page - 1) * PER_PAGE)) < \
		   		    len(collection.fetch(PER_PAGE + 1, (page - 1) * PER_PAGE)):
			return True


@app.route('/', methods=['GET'])
def home():
	def render_home(purchases, search_query):
		pagination = Pagination(request.args.get('page') or 1, purchases)
		return render_template('home.html', purchases=pagination.results,\
								 previous=pagination.previous, next=pagination.next,\
									 query=search_query)
	if request.args.get('search'):
		searchword = request.args.get('search')
		return render_home(Purchase.all().search(searchword).order('-timestamp'),\
				 searchword)
	else:
		return render_home(Purchase.all().order('-timestamp'), None)




@app.route('/purchases/new', methods=['GET', 'POST'])
def new_purchase():
	form = PicUploadForm()
	if request.method == 'POST' and form.validate():
		image = request.files['PicImage'].read()
		Purchase(
					pic_title = request.form['PicTitle'],
					pic_image_thumb = db.Blob(images.resize(image, 200, 100)),
					pic_image_large = db.Blob(images.resize(image, 800, 800)),
					pic_poster = request.form['PicPoster'],
					pic_price = request.form['PicPrice'],
					pic_where = request.form['PicWhere']
				).put()
		return redirect('/')
	else:
		return render_template('new_purchase.html', form=form)



@app.route('/images/<size>/<id>', methods=['GET'])
def show(size, id):
	purchase = db.get(id)
	if size == "thumb":
		response = make_response(purchase.pic_image_thumb)
	elif size == "large":
		response = make_response(purchase.pic_image_large)
	response.headers['Content-Type'] = "image/jpeg"
	return response




app.secret_key = 'sdfdfsdnjjnk777828282JHKjsdqsdqs5656266'


if __name__ == '__main__':
    app.run()
