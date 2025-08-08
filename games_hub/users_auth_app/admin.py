from django.contrib import admin
from users_auth_app.models import CustomUser, Order,Voucher,OrderItem
# Register your models here.
admin.site.register(CustomUser)

class OrderItemInline(admin.TabularInline):  # Or use admin.StackedInline if you prefer
    model = OrderItem
    extra = 0  # Don't show extra blank rows
    readonly_fields = ['quantity', 'price', 'item_price']  # Make them readonly if you prefer
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'order_status', 'order_date']
    list_filter = ['order_status', 'order_date','order_id']
    search_fields = ['order_id', 'user__email']
    readonly_fields = ['total_price','order_id']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)



class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'created_at', 'expiration_date', 'usage_limit', 'used_count')
    list_filter = ('created_at','code')  # ✅ Enables filtering by date in admin
    readonly_fields = ('used_count', 'created_at')  # Prevent manual changes
    search_fields = ['code']
    actions = ['delete_selected']  # Default action for bulk delete
admin.site.register(Voucher, VoucherAdmin)
