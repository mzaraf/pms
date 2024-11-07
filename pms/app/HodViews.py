from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal, JobDescription, TrainingCourseSeminars
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from weasyprint import HTML


@login_required
def hod_dashboard(request):
    hod_department = request.user.department
    appraisals = Appraisal.objects.filter(department=hod_department)
    return render(request, 'hod_templates/hod_home.html', {'appraisals': appraisals})

@login_required
def hod_form(request):
    return render(request, 'hod_templates/hod_form.html')

def hod_view_appraisals(request):
    query = request.GET.get('q')
    hod_department = request.user.department
    appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='Completed').order_by('ippis_no')

    # Filter based on the search query if it exists
    if query:
        appraisals = appraisals.filter(
            Q(file_number__icontains=query) |
            Q(ippis_no__icontains=query) |
            Q(full_name__icontains=query) |
            Q(designation__icontains=query) |
            Q(department__name__icontains=query)
        )

    # Paginate the results
    items_per_page = 100
    paginator = Paginator(appraisals, items_per_page)
    show_pagination = paginator.count > items_per_page
    page_number = request.GET.get('page')
    appraisals = paginator.get_page(page_number)

    return render(request, 'hod_templates/hod_view_appraisals.html', {
        'appraisals': appraisals,
        'show_pagination': show_pagination,
    })

@login_required
def hod_result(request):
    hod_department = request.user.department

    complete_appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='Completed').order_by('-id')
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


def hod_download_appraisal(request):
    query = request.GET.get('q')
    hod_department = request.user.department
    appraisals = Appraisal.objects.filter(department=hod_department, appraisal_status='Completed').order_by('-id')

    if query:
        appraisals = appraisals.filter(
            Q(full_name__icontains=query) |
            Q(file_number__icontains=query) |
            Q(ippis_no__icontains=query) |
            Q(department__name__icontains=query) |
            Q(designation__icontains=query)
        )

    # Get selected fields from the form
    selected_fields = request.GET.getlist('fields')

    # Create a mapping for custom column names
    field_names_mapping = {
        'full_name': 'Full Name',
        'file_number': 'File Number',
        'ippis_no': 'IPPIS',
        'designation': 'Designation',
        'department': 'Department',
        'total_appraisal_rating': 'Score',
    }

    if 'all' in selected_fields:
        selected_fields = list(field_names_mapping.keys())

    # Collect data to be included in the PDF
    data = []
    for appraisal in appraisals:
        row = []
        if 'full_name' in selected_fields:
            row.append(appraisal.full_name)
        if 'file_number' in selected_fields:
            row.append(appraisal.file_number)
        if 'ippis_no' in selected_fields:
            row.append(appraisal.ippis_no)
        if 'designation' in selected_fields:
            row.append(appraisal.designation)
        if 'department' in selected_fields:
            row.append(appraisal.department.name if appraisal.department else '')
        if 'total_appraisal_rating' in selected_fields:
            row.append(appraisal.total_appraisal_rating)
        
        data.append(row)
    
    # Render the data to an HTML template for PDF conversion
    html_content = render_to_string('hod_templates/download_appraisal.html', {
        'appraisals': data,
        'selected_fields': selected_fields,
        'field_names_mapping': field_names_mapping,
        'department_name': hod_department.name,
        
    })

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=appraisal_report.pdf'
    
    # Use WeasyPrint to write the HTML content to the response as a PDF
    HTML(string=html_content).write_pdf(response)

    return response