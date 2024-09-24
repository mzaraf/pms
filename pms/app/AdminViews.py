from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal,JobDescription, TrainingCourseSeminars
from django.core.paginator import Paginator


def admin_dashboard(request):
    staff_user = request.user
    appraisals = Appraisal.objects.filter(staff=staff_user)
    return render(request, 'admin_templates/admin_home.html', {'appraisals': appraisals})

def admin_view_results(request):
    appraisals = Appraisal.objects.filter(appraisal_status='Completed').order_by('ippis_no')

    items_per_page = 50
    paginator = Paginator(appraisals, items_per_page)
    show_pagination = paginator.count > items_per_page

    page_number = request.GET.get('page')
    appraisals = paginator.get_page(page_number)
    
    return render(request, 'admin_templates/admin_result.html', {'appraisals': appraisals,  'show_pagination': show_pagination,})


@login_required
def admin_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'admin_templates/admin_view.html', context)


