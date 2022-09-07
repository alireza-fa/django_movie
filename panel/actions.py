from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from core.models import Contact


def user_action(request, action, pk=None):
    if action:
        if not pk:
            pass

        else:
            user = get_object_or_404(get_user_model(), pk=pk)
            if action == 'change_status':
                if not user.is_superuser and (request.user.is_superuser or not user.is_admin):
                    bool_active = user.is_active
                    if bool_active:
                        user.is_active = False
                    else:
                        user.is_active = True
                    user.save()
            elif action == 'delete':
                if not user.is_superuser and (request.user.is_superuser or not user.is_admin):
                    user.delete()


def contact_action(request, action, pk=None):
    if action:
        if not pk:
            if action == 'delete_all_read_contact':
                Contact.objects.filter(is_read=True).delete()
        else:
            contact = get_object_or_404(Contact, id=pk)
            if action == 'delete':
                contact.delete()
            elif action == 'is_read':
                contact.is_read = True
                contact.save()
