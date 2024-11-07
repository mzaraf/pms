# views.py
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm
from .models import Unit
from django.http import JsonResponse


#def landing(request):
#    return render(request, 'landing.html')

def doLogin(request):

    if request.user.is_authenticated:
        user_type_id = request.user.usertype_id
        if user_type_id == 1:
            return redirect('admin')
        elif user_type_id == 2:
            return redirect('hod')
        elif user_type_id == 3:
            return redirect('supervisor')
        elif user_type_id == 4:
            return redirect('staff')

    if request.method == 'POST':
        ippis_no = request.POST['ippis_no']
        password = request.POST['password']
        user = authenticate(request, ippis_no=ippis_no, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, ('Login successsful!'))
            usertype_id = user.usertype_id

            if usertype_id == 1:
                return redirect('admin')
            elif usertype_id == 2:
                return redirect('hod')
            elif usertype_id == 3:
                return redirect('supervisor')
            elif usertype_id == 4:
                return redirect('staff')
            else:
                messages.error(request, 'Invalid username or password. Please retry...')
                return redirect('login')
        else:
            messages.error(request, 'Invalid IPPIS Number or Password! Please retry...')
            return redirect('login')
    else:
        return render(request, 'login.html')


def doLogout(request):
    logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # This will save the new password
            #update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully changed! Please login with the new password')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })

def get_units_by_department(request):
    department_id = request.GET.get('department_id')  # Get the department ID from the request
    units = Unit.objects.filter(department_id=department_id).values('id', 'name')  # Filter units by department
    units_list = list(units)  # Convert QuerySet to list
    return JsonResponse(units_list, safe=False)  # Return the units in JSON format