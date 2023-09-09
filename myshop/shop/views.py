from itertools import product
from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Create your views here.


def product_list(request,category_slug=None):
    
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    cart_product_form = CartAddProductForm()
    
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category)
        
    context = {
        'categories':categories,
        'category':category,
        'products':products,
        'form':cart_product_form,
    }
    
    return render(request,'shop/product/list.html',context)
    
    
def product_detail(request,id,slug):
    
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    category = product.category
    cart_product_form = CartAddProductForm()
    
    r = Recommender()
    recommended_products = r.suggest_products_for([product],2)
    
    context={
        'product':product,
        'category':category,
        'form':cart_product_form,
        'recommended_products':recommended_products,
    }
    
    return render(request,'shop/product/detail.html',context)        