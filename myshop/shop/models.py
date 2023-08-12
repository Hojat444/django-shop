from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    name = models.CharField(_("name"),max_length=200,db_index=True)
    slug = models.SlugField(_("slug"),max_length=200,db_index=True)
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
        
    def __str__(self):
        return self.name
    
    

class Product(models.Model):
    category = models.ForeignKey(Category,related_name="products" ,on_delete=models.CASCADE,)
    name = models.CharField(_("name"),max_length=200,db_index=True)
    slug = models.SlugField(_("slug"),max_length=200,db_index=True)
    image = models.ImageField(_("image"),upload_to='products/%Y/%m/%d', blank =True)
    description = models.TextField(_("description"),blank =True)
    price = models.PositiveIntegerField(_("price"))
    available = models.BooleanField(_("available"),default=True)
    created = models.DateField(_("created"),auto_now_add=True)
    updated = models.DateField(_("updated"),auto_now=True)
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id,self.slug])
    
    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)
        
    def __str__(self):
        return self.name    
        
    
        
