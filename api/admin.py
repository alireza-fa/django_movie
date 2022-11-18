from django.contrib import admin
from .models import OutstandingToken, BlacklistedToken


admin.site.register(OutstandingToken)
admin.site.register(BlacklistedToken)
