from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal, CustomUser, Department, Usertype, Unit, JobDescription, TrainingCourseSeminars
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def staff_dashboard(request):
    staff_user = request.user
    appraisals = Appraisal.objects.filter(staff=staff_user)
    return render(request, 'staff_templates/staff_home.html', {'appraisals': appraisals})

# Define a ModelForm for the CustomUser model
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
             'department', 'unit',
        ]

def staff_update_details(request, user_id):
    staff = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=staff)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Updated Successfully')
            return redirect('staff')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = CustomUserForm(instance=staff)

    context = {
        'form': form,
        'user_id': staff.id,
        'departments': Department.objects.all(),
        'units': Unit.objects.all(),
        'user': staff,
    }
    
    return render(request, 'staff_templates/staff_update_details.html', context)

def staff_get_units_by_department(request):
    department_id = request.GET.get('department_id')  # Get the department ID from the request
    units = Unit.objects.filter(department_id=department_id).values('id', 'name')  # Filter units by department
    units_list = list(units)  # Convert QuerySet to list
    return JsonResponse(units_list, safe=False)  # Return the units in JSON format

@login_required
def staff_view_appraisal(request):
    staff_user = request.user
    appraisals = Appraisal.objects.filter(staff=staff_user)
    return render(request, 'staff_templates/staff_view_appraisal.html', {'appraisals': appraisals})

@login_required
def staff_result(request):
    staff_user = request.user

    complete_appraisals = Appraisal.objects.filter(staff=staff_user, appraisal_status='Completed').order_by('-id')
    in_progress_appraisals = Appraisal.objects.filter(staff=staff_user).filter(Q(appraisal_status='Supervisor Review') | Q(appraisal_status='HoD Review')).order_by('id')

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
    
    return render(request, 'staff_templates/staff_result.html', context)


@login_required
def staff_review(request, appraisal_id):
    try:
        # Retrieve the appraisal by its ID
        appraisal = Appraisal.objects.get(id=appraisal_id, staff=request.user)

        # Retrieve the job descriptions related to this appraisal
        job_descriptions = JobDescription.objects.filter(appraisal=appraisal)

        # Retrieve the trainings and seminars related to this appraisal
        training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    except Appraisal.DoesNotExist:
        messages.error(request, "Appraisal not found.")
        return HttpResponseRedirect(reverse('staff'))

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars,
    }

    return render(request, 'staff_templates/staff_review.html', context)


@login_required
def staff_form(request):
    user = request.user

    # Fetch the supervisors in the same department and unit
    supervisors = CustomUser.objects.filter(
        usertype__name='supervisor', 
        department=user.department, 
        unit=user.unit
    )

    # Fetch the HODs in the same department
    hods = CustomUser.objects.filter(
        usertype__name='hod', 
        department=user.department
    )

    context = {
        'supervisors': supervisors,
        'hods': hods,
    }
    return render(request, 'staff_templates/staff_form.html', context)

def _save_job_descriptions(appraisal, activity_tasks, overall_assessments):
    # Save each new job description
    for task, assessment in zip(activity_tasks, overall_assessments):
        JobDescription.objects.create(
            appraisal=appraisal,
            activity_task=task,
            overall_assessment_of_performance=assessment,
        )

def _save_training_records(appraisal, training_program_type, training_location, training_from_date, training_to_date):
    
    # Save each new training record
    for t_type, location, from_date, to_date in zip(training_program_type, training_location, training_from_date, training_to_date):
        
        from_date = from_date if from_date else None
        to_date = to_date if to_date else None
        if t_type and location:
            TrainingCourseSeminars.objects.create(
                appraisal=appraisal,
                training_program_type=t_type,
                training_location=location,
                training_from_date=from_date,
                training_to_date=to_date,
                )


@login_required
def staff_initiate_appraisal(request):
    if request.method == 'POST':

        # Your existing code for getting form data
        period_of_evaluation_from_date = request.POST.get('period_of_evaluation_from_date')
        

        # Convert the string to a date object
        period_of_evaluation_from_date = timezone.datetime.strptime(period_of_evaluation_from_date, '%Y-%m-%d').date()

        # Check for existing appraisal for the current year
        existing_appraisal = Appraisal.objects.filter(staff=request.user, period_of_evaluation_from_date__year=period_of_evaluation_from_date.year).first()
        if existing_appraisal:
            messages.error(request, 'An appraisal for this year has already been initiated.')
            return render(request, 'staff_templates/staff_form.html', {'appraisal': existing_appraisal})

        # Create or update the appraisal
        staff_obj = Appraisal(
            staff=request.user, 
            department = request.user.department, 
            unit = request.user.unit,

            # Set other fields and save
            period_of_evaluation_from_date = period_of_evaluation_from_date,
            period_of_evaluation_to_date = request.POST.get('period_of_evaluation_to_date'),
            full_name = request.POST.get('full_name'),
            date_of_birth = request.POST.get('date_of_birth'),
            date_of_first_appointment = request.POST.get('date_of_first_appointment'),
            date_of_present_appointment = request.POST.get('date_of_present_appointment'),
            date_of_acting_appointment = request.POST.get('date_of_acting_appointment'),
            file_number = request.POST.get('file_number'),
            ippis_no = request.POST.get('ippis_no'),
            designation = request.POST.get('designation'),

            qualification = request.POST.get('qualification'),
            institution = request.POST.get('institution'),
            qualification_award_date = request.POST.get('qualification_award_date'),

            main_duties_performed_by_staff = request.POST.get('main_duties_performed_by_staff'),
            joint_discussion_with_supervisor = request.POST.get('joint_discussion_with_supervisor'),
            staff_professionally_equipped = request.POST.get('staff_professionally_equipped'),
            difficulties_achieving_target = request.POST.get('difficulties_achieving_target'),
            method_by_supervisor_to_resolve_difficulties= request.POST.get('method_by_supervisor_to_resolve_difficulties'),
            target_review_with_supervisor = request.POST.get('target_review_with_supervisor'),
            performance_measure_upto_standard_after_review = request.POST.get('performance_measure_upto_standard_after_review'),
            adhoc_duties_performed = request.POST.get('adhoc_duties_performed'),
            adhoc_duties_impact_real_duties = request.POST.get('adhoc_duties_impact_real_duties'),
            main_duties_performed_by_staff_from_date = request.POST.get('main_duties_performed_by_staff_from_date'),
            main_duties_performed_by_staff_to_date = request.POST.get('main_duties_performed_by_staff_to_date'),

            cost_project_assignment_responsibility_allowances = request.POST.get('cost_project_assignment_responsibility_allowances'),
            project_assignment_responsibility_overhead_cost = request.POST.get('project_assignment_responsibility_overhead_cost'),
            project_assignment_responsibility_capital_cost = request.POST.get('project_assignment_responsibility_capital_cost'),
            project_assigment_completion_time = request.POST.get('project_assigment_completion_time'),
            project_quantity_conformity_to_standard = request.POST.get('project_quantity_conformity_to_standard'),
            project_quality_conformity_to_standard = request.POST.get('project_quality_conformity_to_standard'),

            quality_of_training_received = request.POST.get('quality_of_training_received'),


            reporting_officer = request.POST.get('reporting_officer'),
            reporting_officer_from_date = request.POST.get('reporting_officer_from_date'),
            reporting_officer_to_date = request.POST.get('reporting_officer_to_date'),
            countersigning_officer = request.POST.get('countersigning_officer'),
            countersigning_officer_from_date = request.POST.get('countersigning_officer_from_date'),
            countersigning_officer_to_date = request.POST.get('countersigning_officer_to_date'),

            appraisal_type = 'staff',
            appraisal_status = 'Supervisor Review')
        
        staff_obj.save()

       # Handle job descriptions and training records
        _save_job_descriptions(staff_obj, request.POST.getlist('activity_task[]'), request.POST.getlist('overall_assessment_of_performance[]'))
        _save_training_records(staff_obj, request.POST.getlist('training_program_type[]'), 
                                   request.POST.getlist('training_location[]'), 
                                   request.POST.getlist('training_from_date[]'), 
                                   request.POST.getlist('training_to_date[]'))

        messages.success(request, 'Appraisal Initiated Successfully')
        return HttpResponseRedirect(reverse('staff_result'))

    else:
        messages.error(request, 'Failed to Initiate Appraisal. Please try again.')

    return HttpResponseRedirect(reverse('staff_form'))