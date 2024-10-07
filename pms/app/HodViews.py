from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal, JobDescription, TrainingCourseSeminars
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def hod_dashboard(request):
    hod_department = request.user.department
    appraisals = Appraisal.objects.filter(department=hod_department)
    return render(request, 'hod_templates/hod_home.html', {'appraisals': appraisals})

@login_required
def hod_form(request):
    return render(request, 'hod_templates/hod_form.html')

def hod_view_appraisals(request):
    appraisals = Appraisal.objects.all()

    hod_department = request.user.department

    appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='HoD Review')
    return render(request, 'hod_templates/hod_view_appraisals.html', {'appraisals': appraisals})

@login_required
def hod_result(request):
    hod_department = request.user.department

    complete_appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='Completed').order_by('-')
    in_progress_appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='HoD Review').order_by('id')

    # Set the number of items per page
    items_per_page = 20

    # Pagination for complete appraisals
    complete_paginator = Paginator(complete_appraisals, items_per_page)
    complete_show_pagination = complete_paginator.count > items_per_page
    complete_page_number = request.GET.get('complete_page')
    complete_appraisals_paginated = complete_paginator.get_page(complete_page_number)

    # Pagination for in-progress appraisals
    in_progress_paginator = Paginator(in_progress_appraisals, items_per_page)
    in_progress_show_pagination = in_progress_paginator.count > items_per_page
    in_progress_page_number = request.GET.get('in_progress_page')
    in_progress_appraisals_paginated = in_progress_paginator.get_page(in_progress_page_number)

    context = {
        'complete_appraisals': complete_appraisals_paginated,
        'in_progress_appraisals': in_progress_appraisals_paginated,
        'show_complete_pagination': complete_paginator.count > items_per_page,
        'show_in_progress_pagination': in_progress_paginator.count > items_per_page,
        'complete_show_pagination': complete_show_pagination,
        'in_progress_show_pagination': in_progress_show_pagination
    }
    
    return render(request, 'hod_templates/hod_result.html', context)


@login_required
def staff_hod_review(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'hod_templates/staff_hod_review.html', context)

@login_required
def staff_hod_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'hod_templates/staff_hod_view.html', context)

@login_required
def supervisor_hod_review(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'hod_templates/supervisor_hod_review.html', context)

@login_required
def supervisor_hod_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'hod_templates/supervisor_hod_view.html', context)

@login_required
def staff_hod_rating(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)

    # Ensure the appraisal is in 'supervisor_review' status
    if appraisal.appraisal_status != 'HoD Review':
        messages.error(request, 'This appraisal is not available for review.')
        return HttpResponseRedirect(reverse('hod_result'))
    
    if request.method == 'POST':
        appraisal.head_of_department_comments = request.POST['head_of_department_comments']
        appraisal.head_of_department_date_of_evaluation = request.POST['head_of_department_date_of_evaluation']
        appraisal.appraisal_status = 'Completed'
        appraisal.save()
        messages.success(request, 'Appraisal Completed. Thank You for your time.')
        return redirect('hod_result')
    return render(request, 'hod_templates/hod_result.html', {'appraisal': appraisal})


@login_required
def supervisor_hod_rating(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)

    # Ensure the appraisal is in 'supervisor_review' status
    if appraisal.appraisal_status != 'HoD Review':
        messages.error(request, 'This appraisal is not available for review.')
        return HttpResponseRedirect(reverse('hod_result'))
    
    if request.method == 'POST':

        appraisal.job_knowledge = int(request.POST['job_knowledge'])
        appraisal.quality_of_work = int(request.POST['quality_of_work'])
        appraisal.quantity_of_work = int(request.POST['quantity_of_work'])
        appraisal.reliability = int(request.POST['reliability'])
        appraisal.initiative_creativity = int(request.POST['initiative_creativity'])
        appraisal.judgment = int(request.POST['judgment'])
        appraisal.relationship_with_supervisor = int(request.POST['relationship_with_supervisor'])
        appraisal.working_with_others = int(request.POST['working_with_others'])
        appraisal.relationship_with_subordinates = int(request.POST['relationship_with_subordinates'])
        appraisal.communication_skills = int(request.POST['communication_skills'])
        appraisal.planning_and_organizing = int(request.POST['planning_and_organizing'])
        appraisal.directing_and_controlling = int(request.POST['directing_and_controlling'])
        appraisal.decision_making = int(request.POST['decision_making'])

        appraisal.commendation_for_outstanding_performance = int(request.POST['commendation_for_outstanding_performance'])
        appraisal.details_of_commendation_for_outstanding_performance = request.POST['details_of_commendation_for_outstanding_performance']
        appraisal.suggestions_that_contributed_to_changes = float(request.POST['suggestions_that_contributed_to_changes'])
        appraisal.sanction_discipline = request.POST['sanction_discipline']
        appraisal.details_sanction_discipline = request.POST['details_sanction_discipline']

        appraisal.capacity_development_since_last_evaluation = request.POST['capacity_development_since_last_evaluation']
        appraisal.accommplishments_since_last_evaluation = request.POST['accommplishments_since_last_evaluation']
        appraisal.training_requirements_to_handle_responsibilities = request.POST['training_requirements_to_handle_responsibilities']
        appraisal.skills_gap_requiring_improvement = request.POST['skills_gap_requiring_improvement']
        appraisal.missed_opportunities_reason = request.POST['missed_opportunities_reason']

        appraisal.overall_performance_assessment = request.POST['overall_performance_assessment']
        appraisal.promotability = request.POST['promotability']

        appraisal.head_of_department_comments = request.POST['head_of_department_comments']
        appraisal.head_of_department_date_of_evaluation = request.POST['head_of_department_date_of_evaluation']
        appraisal.appraisal_status = 'Completed'
        appraisal.save()
        messages.success(request, 'Appraisal Completed. Thank You for your time.')
        return redirect('hod_result')
    return render(request, 'hod_templates/hod_home.html', {'appraisal': appraisal})

