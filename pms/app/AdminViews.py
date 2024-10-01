from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appraisal,JobDescription, TrainingCourseSeminars
from django.core.paginator import Paginator
from .models import CustomUser, Department, Unit, Usertype
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings
import os

def admin_dashboard(request):
    staff_user = request.user
    appraisals = Appraisal.objects.filter(staff=staff_user)
    return render(request, 'admin_templates/admin_home.html', {'appraisals': appraisals})


def staff_list(request):
    query = request.GET.get('q')
    staff_members = CustomUser.objects.all().order_by('ippis_no')

    # Filter based on the search query if it exists
    if query:
        staff_members = staff_members.filter(
            Q(file_number__icontains=query) |
            Q(ippis_no__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(designation__icontains=query) |
            Q(department__name__icontains=query)  # Assuming department is a ForeignKey
        )

    # Paginate staff members list
    items_per_page = 100

    paginator = Paginator(staff_members, items_per_page)
    show_pagination = paginator.count > items_per_page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'staff_members': page_obj,
        'show_pagination': show_pagination,
    }

    return render(request, 'admin_templates/staff_list.html', context)

def add_staff_info(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_first_appointment = request.POST.get('date_of_first_appointment')
        date_of_present_appointment = request.POST.get('date_of_present_appointment')
        date_of_acting_appointment = request.POST.get('date_of_acting_appointment')
        file_number = request.POST.get('file_number')
        ippis_no = request.POST.get('ippis_no')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        unit = request.POST.get('unit')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        qualification = request.POST.get('qualification')
        institution = request.POST.get('institution')
        qualification_award_date = request.POST.get('qualification_award_date')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')

        username = f"{first_name.lower()}.{last_name.lower()}"
        # Create new staff member
        try:
            new_staff = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                date_of_first_appointment=date_of_first_appointment,
                date_of_present_appointment=date_of_present_appointment,
                date_of_acting_appointment=date_of_acting_appointment,
                file_number=file_number,
                ippis_no=ippis_no,
                designation=designation,
                department_id=department,
                unit_id=unit,
                email=email,
                phone=phone,
                qualification=qualification,
                institution=institution,
                qualification_award_date=qualification_award_date,
                password=password,
                usertype_id=usertype,
            )
            new_staff.save()

             # Send email to the new staff with their login details
            #send_mail(
            #    subject='NASRDA PMS: Login Credentials',
            #    message=f'Dear {first_name},\n\nYour account has been created successfully on the NASRDA PMS. Below are your login details:\n\n'
            #            f'IPPIS Number: your ippis number\n'
            #            f'Password: {password}\n'
            #            f'Link: pe.nasrda.gov.ng\n\n'
            #            f'Please change your password after your first login.\n\n'
            #            f'Thank you.',
                #from_email=settings.DEFAULT_FROM_EMAIL,
            #    from_email = os.getenv('DEFAULT_FROM_EMAIL'),
            #    recipient_list=[email],
            #    fail_silently=False,
            #)
            messages.success(request, f"Staff member {first_name} {last_name} has been added successfully, and login credentials have been sent to their email.")
            return redirect('staff_list')  # Redirect to a success page or another view
        
        except Exception as e:
            messages.error(request, f"An error occurred while adding staff details: {str(e)}")

            departments = Department.objects.all()
            units = Unit.objects.all()
            user_types = Usertype.objects.all()
            return render(request, 'admin_templates/add_staff.html', {
                'departments': departments,
                'units': units,
                'user_types': user_types,
            })
    else:
        departments = Department.objects.all()
        units = Unit.objects.all()
        user_types = Usertype.objects.all()
        
        return render(request, 'admin_templates/add_staff.html', {
            'departments': departments,
            'units': units,
            'user_types': user_types,
        })



#def update_staff_info(request, user_id):
#    staff = get_object_or_404(CustomUser, id=user_id)

#    if request.method == 'POST':
        # Update staff fields with POST data
#        staff.first_name = request.POST.get('first_name')
#        staff.middle_name = request.POST.get('middle_name')
#        staff.last_name = request.POST.get('last_name')
#        staff.date_of_birth = request.POST.get('date_of_birth')
#        staff.date_of_first_appointment = request.POST.get('date_of_first_appointment')
#        staff.date_of_present_appointment = request.POST.get('date_of_present_appointment')
#        staff.date_of_acting_appointment = request.POST.get('date_of_acting_appointment')
#        staff.file_number = request.POST.get('file_number')
#        staff.ippis_no = request.POST.get('ippis_no')
#        staff.designation = request.POST.get('designation')
#        staff.department_id = request.POST.get('department')
#        staff.unit_id = request.POST.get('unit')
#        staff.usertype_id = request.POST.get('usertype')
#        staff.email = request.POST.get('email')
#        staff.phone = request.POST.get('phone')
#        staff.qualification = request.POST.get('qualification')
#        staff.institution = request.POST.get('institution')
#        staff.qualification_award_date = request.POST.get('qualification_award_date')

#        staff.save()
#        messages.success(request, 'Details Updated Successfully')
#        return redirect('staff_list')

#    context = {
#        'user_id': staff.id,
#        'departments': Department.objects.all(),
#        'units': Unit.objects.all(),
#        'user_types': Usertype.objects.all(),
#        'user': staff,
#    }
#    return render(request, 'admin_templates/update_details.html', context)


# Define a ModelForm for the CustomUser model
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'middle_name', 'last_name', 'date_of_birth', 'date_of_first_appointment',
            'date_of_present_appointment', 'date_of_acting_appointment', 'file_number', 'ippis_no',
            'designation', 'department', 'unit', 'usertype', 'email', 'phone', 'qualification',
            'institution', 'qualification_award_date'
        ]

def update_staff_info(request, user_id):
    staff = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=staff)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Updated Successfully')
            return redirect('staff_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = CustomUserForm(instance=staff)

    context = {
        'form': form,
        'user_id': staff.id,
        'departments': Department.objects.all(),
        'units': Unit.objects.all(),
        'usertypes': Usertype.objects.all(),
        'user': staff,
    }
    
    return render(request, 'admin_templates/update_details.html', context)


def get_units_by_department(request):
    department_id = request.GET.get('department_id')  # Get the department ID from the request
    units = Unit.objects.filter(department_id=department_id).values('id', 'name')  # Filter units by department
    units_list = list(units)  # Convert QuerySet to list
    return JsonResponse(units_list, safe=False)  # Return the units in JSON format

def download_staff_data(request):
    query = request.GET.get('q')
    staff_members = CustomUser.objects.all().order_by('ippis_no')

    if query:
        staff_members = staff_members.filter(
            Q(file_number__icontains=query) |
            Q(ippis_no__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(designation__icontains=query) |
            Q(department__name__icontains=query)
        )

    # Get selected fields from the form
    selected_fields = request.GET.getlist('fields')

    if 'all' in selected_fields:
        selected_fields = ['file_number', 'ippis_no', 'first_name', 'last_name', 'middle_name', 'designation', 'department']

    
    data = []
    for staff in staff_members:
        row = {}
        if 'file_number' in selected_fields:
            row['File Number'] = staff.file_number
        if 'ippis_no' in selected_fields:
            row['IPPIS Number'] = staff.ippis_no
        if 'first_name' in selected_fields:
            row['First Name'] = staff.first_name
        if 'last_name' in selected_fields:
            row['Last Name'] = staff.last_name
        if 'middle_name' in selected_fields:
            row['Middle Name'] = staff.middle_name
        if 'designation' in selected_fields:
            row['Designation'] = staff.designation
        if 'department' in selected_fields:
            row['Department'] = staff.department.name if staff.department else ''
        data.append(row)
    
    df = pd.DataFrame(data)

    # Create a response object to send the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=staff_data.xlsx'

    # Use the `pandas` ExcelWriter to write the DataFrame to an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Staff')

    return response


def admin_view_results(request):
    query = request.GET.get('q')
    appraisals = Appraisal.objects.filter(appraisal_status='Completed').order_by('ippis_no')

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

    return render(request, 'admin_templates/admin_result.html', {
        'appraisals': appraisals,
        'show_pagination': show_pagination,
    })


@login_required
def admin_staff_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'admin_templates/admin_staff_view.html', context)

@login_required
def admin_supervisor_view(request, appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    job_descriptions = JobDescription.objects.filter(appraisal=appraisal)
    training_seminars = TrainingCourseSeminars.objects.filter(appraisal=appraisal)

    context = {
        'appraisal': appraisal,
        'job_descriptions': job_descriptions,
        'training_seminars': training_seminars
    }

    return render(request, 'admin_templates/admin_supervisor_view.html', context)

def download_appraisal_data(request):
    query = request.GET.get('q')
    appraisals = Appraisal.objects.all()
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

    if 'all' in selected_fields:
        selected_fields = [
            'period_of_evaluation_from_date', 'period_of_evaluation_to_date',
            'full_name', 'date_of_birth', 'date_of_first_appointment', 
            'date_of_present_appointment', 'date_of_acting_appointment',
            'file_number', 'ippis_no', 'designation', 'department', 
            'unit', 'qualification', 'institution', 'qualification_award_date',
            'main_duties_performed_by_staff', 'joint_discussion_with_supervisor',
            'staff_professionally_equipped', 'difficulties_achieving_target',
            'method_by_supervisor_to_resolve_difficulties', 
            'target_review_with_supervisor', 'performance_measure_upto_standard_after_review',
            'adhoc_duties_performed', 'adhoc_duties_impact_real_duties',
            'main_duties_performed_by_staff_from_date', 
            'main_duties_performed_by_staff_to_date',
            'cost_project_assignment_responsibility_allowances',
            'project_assignment_responsibility_overhead_cost',
            'project_assignment_responsibility_capital_cost',
            'project_assigment_completion_time', 'project_quantity_conformity_to_standard',
            'project_quality_conformity_to_standard', 'reporting_officer',
            'reporting_officer_from_date', 'reporting_officer_to_date',
            'countersigning_officer', 'countersigning_officer_from_date',
            'countersigning_officer_to_date', 'staff_evaluation_date_submitted',
            'job_knowledge', 'quality_of_work', 'quantity_of_work', 
            'reliability', 'initiative_creativity', 'judgment', 
            'relationship_with_supervisor', 'working_with_others', 
            'relationship_with_subordinates', 'communication_skills', 
            'planning_and_organizing', 'directing_and_controlling', 
            'decision_making', 'commendation_for_outstanding_performance',
            'suggestions_that_contributed_to_changes', 'appraisal_rating',
            'total_appraisal_rating', 'details_of_commendation_for_outstanding_performance',
            'sanction_discipline', 'details_sanction_discipline',
            'capacity_development_since_last_evaluation',
            'accommplishments_since_last_evaluation', 
            'training_requirements_to_handle_responsibilities',
            'skills_gap_requiring_improvement', 'missed_opportunities_reason',
            'overall_performance_assessment', 'promotability', 
            'supervisor_comments', 'supervisor_date_of_evaluation', 
            'head_of_department_comments', 'head_of_department_date_of_evaluation',
            'appraisal_type', 'appraisal_status'
        ]

    # Create a DataFrame from the appraisal data
    data = []
    for appraisal in appraisals:
        row = {}
        if 'period_of_evaluation_from_date' in selected_fields:
            row['Period of Evaluation From'] = appraisal.period_of_evaluation_from_date
        if 'period_of_evaluation_to_date' in selected_fields:
            row['Period of Evaluation To'] = appraisal.period_of_evaluation_to_date
        if 'full_name' in selected_fields:
            row['Full Name'] = appraisal.full_name
        if 'date_of_birth' in selected_fields:
            row['Date of Birth'] = appraisal.date_of_birth
        if 'date_of_first_appointment' in selected_fields:
            row['Date of First Appointment'] = appraisal.date_of_first_appointment
        if 'date_of_present_appointment' in selected_fields:
            row['Date of Present Appointment'] = appraisal.date_of_present_appointment
        if 'date_of_acting_appointment' in selected_fields:
            row['Date of Acting Appointment'] = appraisal.date_of_acting_appointment
        if 'file_number' in selected_fields:
            row['File Number'] = appraisal.file_number
        if 'ippis_no' in selected_fields:
            row['IPPIS Number'] = appraisal.ippis_no
        if 'designation' in selected_fields:
            row['Designation'] = appraisal.designation
        if 'department' in selected_fields:
            row['Department'] = appraisal.department.name if appraisal.department else ''
        if 'unit' in selected_fields:
            row['Unit'] = appraisal.unit.name if appraisal.unit else ''
        if 'qualification' in selected_fields:
            row['Qualification'] = appraisal.qualification
        if 'institution' in selected_fields:
            row['Institution'] = appraisal.institution
        if 'qualification_award_date' in selected_fields:
            row['Qualification Award Date'] = appraisal.qualification_award_date
        if 'main_duties_performed_by_staff' in selected_fields:
            row['Main Duties Performed'] = appraisal.main_duties_performed_by_staff
        if 'joint_discussion_with_supervisor' in selected_fields:
            row['Joint Discussion with Supervisor'] = appraisal.joint_discussion_with_supervisor
        if 'staff_professionally_equipped' in selected_fields:
            row['Staff Professionally Equipped'] = appraisal.staff_professionally_equipped
        if 'difficulties_achieving_target' in selected_fields:
            row['Difficulties Achieving Target'] = appraisal.difficulties_achieving_target
        if 'method_by_supervisor_to_resolve_difficulties' in selected_fields:
            row['Method to Resolve Difficulties'] = appraisal.method_by_supervisor_to_resolve_difficulties
        if 'target_review_with_supervisor' in selected_fields:
            row['Target Review with Supervisor'] = appraisal.target_review_with_supervisor
        if 'performance_measure_upto_standard_after_review' in selected_fields:
            row['Performance Measure After Review'] = appraisal.performance_measure_upto_standard_after_review
        if 'adhoc_duties_performed' in selected_fields:
            row['Adhoc Duties Performed'] = appraisal.adhoc_duties_performed
        if 'adhoc_duties_impact_real_duties' in selected_fields:
            row['Adhoc Duties Impact'] = appraisal.adhoc_duties_impact_real_duties
        if 'main_duties_performed_by_staff_from_date' in selected_fields:
            row['Duties From'] = appraisal.main_duties_performed_by_staff_from_date
        if 'main_duties_performed_by_staff_to_date' in selected_fields:
            row['Duties To'] = appraisal.main_duties_performed_by_staff_to_date
        if 'cost_project_assignment_responsibility_allowances' in selected_fields:
            row['Cost Project Assignment Allowances'] = appraisal.cost_project_assignment_responsibility_allowances
        if 'project_assignment_responsibility_overhead_cost' in selected_fields:
            row['Project Assignment Overhead Cost'] = appraisal.project_assignment_responsibility_overhead_cost
        if 'project_assignment_responsibility_capital_cost' in selected_fields:
            row['Project Assignment Capital Cost'] = appraisal.project_assignment_responsibility_capital_cost
        if 'project_assigment_completion_time' in selected_fields:
            row['Project Completion Time'] = appraisal.project_assigment_completion_time
        if 'project_quantity_conformity_to_standard' in selected_fields:
            row['Quantity Conformity to Standard'] = appraisal.project_quantity_conformity_to_standard
        if 'project_quality_conformity_to_standard' in selected_fields:
            row['Quality Conformity to Standard'] = appraisal.project_quality_conformity_to_standard
        if 'quality_of_training_received' in selected_fields:
            row['Quality of Training Received'] = appraisal.quality_of_training_received
        if 'reporting_officer' in selected_fields:
            row['Reporting Officer'] = appraisal.reporting_officer
        if 'reporting_officer_from_date' in selected_fields:
            row['Reporting Officer From'] = appraisal.reporting_officer_from_date
        if 'reporting_officer_to_date' in selected_fields:
            row['Reporting Officer To'] = appraisal.reporting_officer_to_date
        if 'countersigning_officer' in selected_fields:
            row['Countersigning Officer'] = appraisal.countersigning_officer
        if 'countersigning_officer_from_date' in selected_fields:
            row['Countersigning Officer From'] = appraisal.countersigning_officer_from_date
        if 'countersigning_officer_to_date' in selected_fields:
            row['Countersigning Officer To'] = appraisal.countersigning_officer_to_date
        if 'staff_evaluation_date_submitted' in selected_fields:
            row['Evaluation Date Submitted'] = appraisal.staff_evaluation_date_submitted
        if 'job_knowledge' in selected_fields:
            row['Job Knowledge'] = appraisal.job_knowledge
        if 'quality_of_work' in selected_fields:
            row['Quality of Work'] = appraisal.quality_of_work
        if 'quantity_of_work' in selected_fields:
            row['Quantity of Work'] = appraisal.quantity_of_work
        if 'reliability' in selected_fields:
            row['Reliability'] = appraisal.reliability
        if 'initiative_creativity' in selected_fields:
            row['Initiative & Creativity'] = appraisal.initiative_creativity
        if 'judgment' in selected_fields:
            row['Judgment'] = appraisal.judgment
        if 'relationship_with_supervisor' in selected_fields:
            row['Relationship with Supervisor'] = appraisal.relationship_with_supervisor
        if 'working_with_others' in selected_fields:
            row['Working with Others'] = appraisal.working_with_others
        if 'relationship_with_subordinates' in selected_fields:
            row['Relationship with Subordinates'] = appraisal.relationship_with_subordinates
        if 'communication_skills' in selected_fields:
            row['Communication Skills'] = appraisal.communication_skills
        if 'planning_and_organizing' in selected_fields:
            row['Planning & Organizing'] = appraisal.planning_and_organizing
        if 'directing_and_controlling' in selected_fields:
            row['Directing & Controlling'] = appraisal.directing_and_controlling
        if 'decision_making' in selected_fields:
            row['Decision Making'] = appraisal.decision_making
        if 'commendation_for_outstanding_performance' in selected_fields:
            row['Commendation for Performance'] = appraisal.commendation_for_outstanding_performance
        if 'suggestions_that_contributed_to_changes' in selected_fields:
            row['Suggestions for Change'] = appraisal.suggestions_that_contributed_to_changes
        if 'appraisal_rating' in selected_fields:
            row['Appraisal Rating'] = appraisal.appraisal_rating
        if 'total_appraisal_rating' in selected_fields:
            row['Total Appraisal Rating'] = appraisal.total_appraisal_rating
        if 'details_of_commendation_for_outstanding_performance' in selected_fields:
            row['Details of Commendation'] = appraisal.details_of_commendation_for_outstanding_performance
        if 'sanction_discipline' in selected_fields:
            row['Sanction Discipline'] = appraisal.sanction_discipline
        if 'details_sanction_discipline' in selected_fields:
            row['Details of Sanction'] = appraisal.details_sanction_discipline
        if 'capacity_development_since_last_evaluation' in selected_fields:
            row['Capacity Development'] = appraisal.capacity_development_since_last_evaluation
        if 'accommplishments_since_last_evaluation' in selected_fields:
            row['Accomplishments'] = appraisal.accommplishments_since_last_evaluation
        if 'training_requirements_to_handle_responsibilities' in selected_fields:
            row['Training Requirements'] = appraisal.training_requirements_to_handle_responsibilities
        if 'skills_gap_requiring_improvement' in selected_fields:
            row['Skills Gap'] = appraisal.skills_gap_requiring_improvement
        if 'missed_opportunities_reason' in selected_fields:
            row['Missed Opportunities'] = appraisal.missed_opportunities_reason
        if 'overall_performance_assessment' in selected_fields:
            row['Overall Assessment'] = appraisal.overall_performance_assessment
        if 'promotability' in selected_fields:
            row['Promotability'] = appraisal.promotability
        if 'supervisor_comments' in selected_fields:
            row['Supervisor Comments'] = appraisal.supervisor_comments
        if 'supervisor_date_of_evaluation' in selected_fields:
            row['Supervisor Evaluation Date'] = appraisal.supervisor_date_of_evaluation
        if 'head_of_department_comments' in selected_fields:
            row['HoD Comments'] = appraisal.head_of_department_comments
        if 'head_of_department_date_of_evaluation' in selected_fields:
            row['HoD Evaluation Date'] = appraisal.head_of_department_date_of_evaluation
        if 'appraisal_type' in selected_fields:
            row['Appraisal Type'] = appraisal.appraisal_type
        if 'appraisal_status' in selected_fields:
            row['Appraisal Status'] = appraisal.appraisal_status
        
        data.append(row)

    df = pd.DataFrame(data)

    # Create a response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=appraisal_data.xlsx'
    
    # Save the DataFrame to the response as an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Appraisals')

    return response


