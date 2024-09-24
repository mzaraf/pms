from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # If the user is authenticated
        if user.is_authenticated:
            usertype_id = user.usertype_id  # Fetch the user type from usertype_id

            # Allow access to the Django admin interface
            if modulename.startswith('django.contrib.admin') or request.path.startswith('/admin/'):
                return None

            # Admin (usertype_id == 1)
            if usertype_id == 1:
                if modulename in ['app.AdminViews', 'app.views', 'django.views.static']:
                    pass
                else:
                    return redirect('admin')
            # HOD (usertype_id == 2)
            elif usertype_id == 2:
                if modulename in ['app.HodViews', 'app.views', 'django.views.static']:
                    pass
                else:
                    return redirect('hod')
            # Supervisor (usertype_id == 3)
            elif usertype_id == 3:
                if modulename in ['app.SupervisorViews', 'app.views', 'django.views.static']:
                    pass
                else:
                    return redirect('supervisor')
            # Staff (usertype_id == 4)
            elif usertype_id == 4:
                if modulename in ['app.StaffViews', 'app.views', 'django.views.static']:
                    pass
                else:
                    return redirect('staff')
            else:
                messages.error(request, 'Invalid user type!')
                return redirect('login')
        
        # If the user is not authenticated
        else:
            if request.path == reverse('login') or modulename == 'django.contrib.auth.views':
                pass
            else:
                return redirect('login')