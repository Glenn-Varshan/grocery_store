from flask_restful import Api
from .resources import User,Item, SearchCat,SearchItem,Category,Cart,Infodownload,CategoryTask,ItemTask,UserTask,CartTask,Adminreq


api = Api(prefix = '/api')

api.add_resource(User, '/user')
api.add_resource(UserTask, '/user/<int:id>')

api.add_resource(Item, '/item')
api.add_resource(ItemTask, '/item/<int:id>')

api.add_resource(Category, '/category')
api.add_resource(CategoryTask, '/category/<int:id>')

api.add_resource(Cart, '/cart')
api.add_resource(CartTask, '/carttask')

api.add_resource(Adminreq, '/adminreq')

api.add_resource(Infodownload, '/infodownload')

api.add_resource(SearchCat,'/search/category')
api.add_resource(SearchItem,'/search/item')