from .models import Category


def create_subcategories(file_path):
    file = open(file_path, 'r')
    for line in file:
        row = line.rstrip().split(',')
        category = Category.objects.all().filter(categoryId__iexact=row[0]).first()
        subcategory = Category.objects.all().filter(categoryId__iexact=row[1]).first()
        category.subcategories.add(subcategory)
    print('done')


def create_category_path(file_path):
    file = open(file_path, 'r')
    for line in file:
        row = line.rstrip().split(',')
        category = Category.objects.all().filter(categoryId__iexact=row[0]).first()
        category_path = Category.objects.all().filter(categoryId__iexact=row[1]).first()
        category.category_path.add(category_path)
    print('done')
