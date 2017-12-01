from .models import Product
from categories.models import Category


def make_product(file_path):
    file = open(file_path, 'r')
    for line in file:
        product_constraints = line.split(',')
        product = Product()

        product.id = product_constraints[0]
        product.name = product_constraints[1]
        product.type = product_constraints[2]
        product.price = product_constraints[3]
        product.upc = product_constraints[4]
        product.shipping = product_constraints[5]
        product.description = product_constraints[6]
        product.manufacturer = product_constraints[7]
        product.model = product_constraints[8]
        product.image = product_constraints[10]

        product.save()
    print('done')


def map_products_categories(file_path):
    file = open(file_path,'r')
    for line in file:
        map_ = line.rstrip().split(',')
        product = Product.objects.get_by_id(_id=map_[0]).first()
        category = Category.objects.get_by_id(_id=map_[1]).first()
        product.categories.add(category)
    print('done')
