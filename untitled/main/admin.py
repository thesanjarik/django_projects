from django.contrib import admin
from main.models import Product, Category, Tag, Review, ConfirmCode

admin.site.register(ConfirmCode)

class ReviewAdminInline(admin.StackedInline):
    model = Review

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = 'name tag_list category price is_active created_at updated_at'.split()
    search_fields = 'name description'.split()
    list_filter = 'category tags is_active price created_at'.split()
    list_editable = 'category price is_active'.split()
    readonly_fields = 'created_at updated_at'.split()
    list_per_page = 3
    inlines = [ReviewAdminInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Review)
