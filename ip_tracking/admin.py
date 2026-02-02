from django.contrib import admin
from .models import RequestLog, BlockedIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'country', 'city', 'timestamp')
    list_filter = ('country', 'city', 'timestamp')
    search_fields = ('ip_address', 'path', 'country', 'city')
    readonly_fields = ('ip_address', 'path', 'country', 'city', 'timestamp')
    
    # Show newest first
    ordering = ('-timestamp',)
    
    # Adjust how many logs show per page
    list_per_page = 50

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'created_at')
    search_fields = ('ip_address',)