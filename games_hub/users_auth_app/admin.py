from django.contrib import admin
from users_auth_app.models import CustomUser, Order,Voucher
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Order)


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'created_at', 'expiration_date', 'usage_limit', 'used_count')
    list_filter = ('created_at','code')  # ✅ Enables filtering by date in admin
    readonly_fields = ('used_count', 'created_at')  # Prevent manual changes
    actions = ['delete_selected']  # Default action for bulk delete
    autocomplete_fields = ['games']
admin.site.register(Voucher, VoucherAdmin)
