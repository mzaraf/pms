from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal, CustomUser, JobDescription,TrainingCourseSeminars
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

@login_required
def supervisor_dashboard(request):
    staff_user = request.user
    appraisals = Appraisal.objects.filter(staff=staff_user)
    return render(request, 'supervisor_templates/supervisor_home.html', {'appraisals': appraisals})

@login_required
def supervisor_form(request):
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
    return render(request, 'supervisor_templates/supervisor_form.html', context)

def supervisor_view_appraisals(request):
    appraisals = Appraisal.objects.all()

    supervisor_unit = request.user.unit 

    appraisals = Appraisal.objects.filter(unit=supervisor_unit, appraisal_status='Supervisor Review')
    return render(request, 'supervisor_templates/supervisor_view_appraisals.html', {'appraisals': appraisals})


@login_required
def supervisor_result(request):
    supervisor_unit = request.user.unit

    # Fetching appraisals for the supervisor
    # 1. Supervisor's own completed appraisals
    complete_appraisals = Appraisal.objects.filter(staff=request.user, appraisal_status='Completed').order_by('-id')
    
    # 2. Supervisor's own appraisals in HoD Review stage
    hod_review_appraisals = Appraisal.objects.filter(staff=request.user, appraisal_status='HoD Review').order_by('-id')

    # 3. In-progress appraisals for the staff under the supervisor's unit
    in_progress_appraisals = Appraisal.objects.filter(unit=supervisor_unit, appraisal_status='Supervisor Review').order_by('id')

    # Set the number of items per page
    items_per_page = 20

    # Pagination for complete appraisals
    complete_paginator = Paginator(complete_appraisals, items_per_page)
    complete_show_pagination = complete_paginator.count > items_per_page
    complete_page_number = request.GET.get('complete_page')
    complete_appraisals_paginated = complete_paginator.get_page(complete_page_number)

    # Pagination for appraisals in HoD Review (supervisor's own)
    hod_review_paginator = Paginator(hod_review_appraisals, items_per_page)
    hod_review_show_pagination = hod_review_paginator.count > items_per_page
    hod_review_page_number = request.GET.get('hod_review_page')
    hod_review_appraisals_paginated = hod_review_paginator.get_page(hod_review_page_number)

    # Pagination for in-progress appraisals
    in_progress_paginator = Paginator(in_progress_appraisals, items_per_page)
    in_progress_show_pagination = in_progress_paginator.count > items_per_page
    in_progress_page_number = request.GET.get('in_progress_page')
    in_progress_appraisals_paginated = in_progress_paginator.get_page(in_progress_page_number)

    context = {
        'complete_appraisals': complete_appraisals_paginated,
        'in_progress_appraisals': in_progress_appraisals_paginated,
        'hod_review_appraisals': hod_review_appraisals_paginated,
        'show_complete_pagination': complete_paginator.count > items_per_page,
        'show_hod_review_pagination': hod_review_show_pagination,
        'show_in_progress_pagination': in_progress_paginator.count > items_per_page,
        'complete_show_pagination': complete_show_pagination,
        'in_progress_show_pagination': in_progress_show_pagination,
    }
    
    return render(request, 'supervisor_templates/supervisor_result.html', context)



@login_required
def supervisor_review(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)

    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }
    return render(request, 'supervisor_templates/supervisor_review.html', context)

@login_required
def supervisor_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)

    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }
    return render(request, 'supervisor_templates/supervisor_view.html', context)



@login_required
def supervisor_rating(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)

    # Ensure the appraisal is in 'supervisor_review' status
    if appraisal.appraisal_status != 'Supervisor Review':
        messages.error(request, 'This appraisal is not available for review.')
        return HttpResponseRedirect(reverse('supervisor_result'))
    
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

        appraisal.supervisor_comments = request.POST['supervisor_comments']
        appraisal.supervisor_date_of_evaluation = request.POST['supervisor_date_of_evaluation']
        appraisal.appraisal_status = 'HoD Review'
        appraisal.save()
        messages.success(request, 'Appraisal submitted for HOD review.')
        return redirect('supervisor_result')
    return render(request, 'supervisor_templates/supervisor_home.html', {'appraisal': appraisal})



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
def supervisor_initiate_appraisal(request):
    if request.method == 'POST':

        # Your existing code for getting form data
        period_of_evaluation_from_date = request.POST.get('period_of_evaluation_from_date')
        

        # Convert the string to a date object
        period_of_evaluation_from_date = timezone.datetime.strptime(period_of_evaluation_from_date, '%Y-%m-%d').date()

        # Check for existing appraisal for the current year
        existing_appraisal = Appraisal.objects.filter(staff=request.user, period_of_evaluation_from_date__year=period_of_evaluation_from_date.year).first()
        if existing_appraisal:
            messages.error(request, 'An appraisal for this year has already been initiated.')
            return render(request, 'supervisor_templates/supervisor_form.html', {'appraisal': existing_appraisal})

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
            #countersigning_officer = request.POST.get('countersigning_officer'),
            #countersigning_officer_from_date = request.POST.get('countersigning_officer_from_date'),
            #countersigning_officer_to_date = request.POST.get('countersigning_officer_to_date'),

            exam_location = request.POST.get('exam_location'),

            appraisal_type = 'supervisor',
            appraisal_status = 'HoD Review')
        
        staff_obj.save()

       # Handle job descriptions and training records
        _save_job_descriptions(staff_obj, request.POST.getlist('activity_task[]'), request.POST.getlist('overall_assessment_of_performance[]'))
        _save_training_records(staff_obj, request.POST.getlist('training_program_type[]'), 
                                   request.POST.getlist('training_location[]'), 
                                   request.POST.getlist('training_from_date[]'), 
                                   request.POST.getlist('training_to_date[]'))

        messages.success(request, 'Appraisal Initiated Successfully')
        return HttpResponseRedirect(reverse('supervisor_result'))

    else:
        messages.error(request, 'Failed to Initiate Appraisal. Please try again.')

    return HttpResponseRedirect(reverse('supervisor_form'))