from django.contrib import admin
from Users.models import Category, Page, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class UserAdmin(admin.ModelAdmin):
    # list_display = ('username', 'fname', 'lname', 'userEmail', 'get_services')
    list_display = ('username', 'fname', 'lname', 'userEmail', 'get_services')



# Register models here
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile, UserAdmin)

