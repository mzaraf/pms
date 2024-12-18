from django.contrib.auth.models import AbstractUser
from django.db import models
from django_fsm import FSMField, transition
import math
import pandas as pd
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, ippis_no, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not ippis_no:
            raise ValueError('The IPPIS number must be set')

        email = self.normalize_email(email)
        user = self.model(ippis_no=ippis_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ippis_no, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(ippis_no, email, password, **extra_fields)


class Usertype(models.Model):
    name = models.CharField(blank=True, max_length=50, db_index = True, unique = True,)
    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length = 100, blank = True, db_index = True, null = True,)
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length = 100, blank = True, db_index = True, null = True,)
    department = models.ForeignKey('Department', on_delete = models.SET_NULL, blank = True, null = True, db_index = True,)
    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):

    ROLE = (
        ('staff', 'Staff'),
        ('supervisor', 'Supervisor'),
        ('hod', 'HOD'),
        ('admin', 'Admin'),
    )

    LOCATION = (
        ('NASRDA HQ', 'NASRDA HQ'),
        ('CAR', 'CAR'),
        ('CSTP EPE', 'CSTP EPE'),
        ('CBSS NSUKKA', 'CBSS NSUKKA'),
        ('NCRS JOS', 'NCRS JOS'),
        ('CGG TORO', 'CGG TORO'),
        ('ARCSSTE-E', 'ARCSSTE-E'),
        ('AACELab GUSAU', 'AACELab GUSAU'),
        ('AAELab OKA', 'AAELab OKA'),
        ('ASCOLab ILLORIN', 'ASCOLab ILLORIN'),
        ('ASTAL UYO', 'ASTAL UYO'),
        ('AUAVL ABAKALIKI', 'AUAVL ABAKALIKI'),
        ('COPINE ILE-IFE', 'COPINE ILE-IFE'),
        ('ZASTAL KASHERE', 'ZASTAL KASHERE'),
        ('ZASTAL NDUFU ALIKE', 'ZASTAL NDUFU ALIKE'),
        ('ZASTAL LANGTANG', 'ZASTAL LANGTANG'),
        ('ZASTAL KANO', 'ZASTAL KANO'),
    )

    middle_name = models.CharField(max_length = 50, blank = True, db_index = True, null = True,)
    file_number = models.CharField(max_length = 50, blank = True, db_index = True, null = True,)
    designation = models.CharField(max_length = 50, blank = True, db_index = True, null = True,)
    date_of_birth = models.DateField(blank = True, db_index = True, null = True,)
    date_of_first_appointment = models.DateField(blank = True, db_index = True, null = True,)
    date_of_present_appointment = models.DateField(blank = True, db_index = True, null = True,)
    date_of_acting_appointment = models.DateField(blank = True, db_index = True, null = True,)
    phone = models.CharField(max_length=15, unique=True, null=True, db_index = True,)
    ippis_no=models.IntegerField(unique=True, null=True, db_index = True,)
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, blank = True, null = True, db_index = True,)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null = True, db_index = True,)
    qualification = models.CharField(max_length = 255, blank = True, db_index = True, null = True,)
    institution = models.CharField(max_length = 255, blank = True, db_index = True, null = True,)
    qualification_award_date = models.DateField(blank = True, db_index = True, null = True,)
    usertype = models.ForeignKey(Usertype, on_delete = models.SET_NULL, blank = True, null = True, db_index = True,)
    exam_location = models.CharField(choices=LOCATION, max_length=50, db_index = True, default='NASRDA HQ')
    objects = CustomUserManager()

    def get_full_name(self):
        # Check if middle_name is NaN or None
        if pd.isna(self.middle_name) or self.middle_name is None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    USERNAME_FIELD = 'ippis_no'

    def __str__(self):
        return str(self.ippis_no)
    
    
class Appraisal(models.Model):

    STATUS = (
        ('initiated', 'Initiated'),
        ('supervisor_review', 'Supervisor Review'),
        ('hod_review', 'HOD Review'),
        ('admin_review', 'Admin Review'),
        ('completed', 'Completed'),
    )

    APPRAISAL_TYPE = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]

    RATING_CHOICES = [
        (16, '5 - Excellent'),
        (13, '4 - Outstanding'),
        (10, '3 - Satisfactory'),
        (7, '2 - Needs improvement'),
        (5, '1 - Unacceptable'),
    ]

    RADIO_RATING_CHOICES = [
        (2, 'yes'),
        (0, 'no'),
    ]

    LEADERSHIP_RATING_CHOICES = [
        (2, '5 - Always'),
        (1.9, '4 - Often'),
        (1, '3 - Sometimes'),
        (0.9, '2 - Rarely'),
        (0.5, '1 - Never'),
    ]

    RADIO_CHOICES = [
        ('yes', 'YES'),
        ('no', 'NO'),
    ]

    TIMELINE_CHOICES = [
        ('DAILY', 'DAILY'),
        ('WEEKLY', 'WEEKLY'),
        ('MONTHLY', 'MONTHLY'),
        ('YEARLY', 'YEARLY'),
    ]

    OVERALL_PERFOMANCE_CHOICE = [
        ('Outstanding', 'A - Outstanding'),
        ('Very Good', 'B - Very Good'),
        ('Good', 'C - Good'),
        ('fair', 'D - Fair'),
        ('Poor', 'E - Poor'),
        ('Very Poor', 'F - Very Poor'),
    ]

    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    period_of_evaluation_from_date = models.DateField(null=True, db_index = True, blank=True)
    period_of_evaluation_to_date = models.DateField(null=True, db_index = True, blank=True)

    full_name = models.CharField(max_length = 100, blank = True, db_index = True, null = True,)
    date_of_birth = models.DateField(null=True, db_index = True, blank=True)
    date_of_first_appointment = models.DateField(null=True, db_index = True, blank=True)
    date_of_present_appointment = models.DateField(null=True, db_index = True, blank=True)
    date_of_acting_appointment = models.DateField(null=True, db_index = True, blank=True)
    file_number = models.CharField(max_length=50, null=True, db_index = True, blank=True)
    ippis_no=models.IntegerField(db_index = True, null=True)
    designation = models.CharField(max_length=50, null=True, db_index = True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null = True)

    qualification = models.CharField(max_length=255, null=True, db_index = True, blank=True)
    institution = models.CharField(max_length=255, null=True, db_index = True, blank=True)
    qualification_award_date = models.DateField(null=True, db_index = True, blank=True)

    main_duties_performed_by_staff = models.TextField(null=True, db_index = True, blank=True)
    joint_discussion_with_supervisor = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    staff_professionally_equipped = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    difficulties_achieving_target = models.TextField(null=True, db_index = True, blank=True)
    method_by_supervisor_to_resolve_difficulties = models.TextField(null=True, db_index = True, blank=True)
    target_review_with_supervisor = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    performance_measure_upto_standard_after_review = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    adhoc_duties_performed = models.TextField(null=True, db_index = True, blank=True)
    adhoc_duties_impact_real_duties = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    main_duties_performed_by_staff_from_date = models.DateField(null=True, db_index = True, blank=True)
    main_duties_performed_by_staff_to_date = models.DateField(null=True, db_index = True, blank=True)

    cost_project_assignment_responsibility_allowances = models.CharField(max_length=50, null=True, db_index = True, blank=True)
    project_assignment_responsibility_overhead_cost = models.CharField(max_length=50, null=True, db_index = True, blank=True)
    project_assignment_responsibility_capital_cost = models.CharField(max_length=50, null=True, db_index = True, blank=True)
    project_assigment_completion_time = models.CharField(max_length=50, choices=TIMELINE_CHOICES, null=True, db_index = True, blank=True)
    project_quantity_conformity_to_standard = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    project_quality_conformity_to_standard = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)

    quality_of_training_received = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)


    reporting_officer = models.CharField(max_length=100, null=True, db_index = True, blank=True)
    reporting_officer_from_date = models.DateField(null=True, db_index = True, blank=True)
    reporting_officer_to_date = models.DateField(null=True, db_index = True, blank=True)
    countersigning_officer = models.CharField(max_length=255, null=True, db_index = True, blank=True)
    countersigning_officer_from_date = models.DateField(null=True, db_index = True, blank=True)
    countersigning_officer_to_date = models.DateField(null=True, db_index = True, blank=True)

    staff_evaluation_date_submitted = models.DateField(db_index = True, auto_now_add=True)

    job_knowledge = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    quality_of_work = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    quantity_of_work = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    reliability = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    initiative_creativity = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    judgment = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    relationship_with_supervisor = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    working_with_others = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    relationship_with_subordinates = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    communication_skills = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    planning_and_organizing = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    directing_and_controlling = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    decision_making = models.IntegerField(choices=RATING_CHOICES, null=True, db_index = True, blank=True)
    
    commendation_for_outstanding_performance = models.IntegerField(choices=RADIO_RATING_CHOICES, null=True, db_index = True, blank=True)
    suggestions_that_contributed_to_changes = models.FloatField(choices=LEADERSHIP_RATING_CHOICES, null=True, db_index = True, blank=True)

    appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    total_appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    
    #q1_appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    #q2_appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    #q3_appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    #q4_appraisal_rating = models.FloatField(null=True, db_index = True, blank=True)
    

    def calculate_appraisal_rating(self):
        rating_fields = [
            self.job_knowledge,
            self.quality_of_work,
            self.quantity_of_work,
            self.reliability,
            self.initiative_creativity,
            self.judgment,
            self.relationship_with_supervisor,
            self.working_with_others,
            self.relationship_with_subordinates,
            self.communication_skills,
            self.planning_and_organizing,
            self.directing_and_controlling,
            self.decision_making
        ]
        # Filter out None values and 0 values
        valid_ratings = [field for field in rating_fields if field not in [None, 0]]
        
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return None

    def save(self, *args, **kwargs):
        self.appraisal_rating = self.calculate_appraisal_rating()

        # Calculate total_appraisal_rating as the sum of the relevant fields
        #self.total_appraisal_rating = math.ceil(
        #    (self.appraisal_rating or 0) +
        #    (self.commendation_for_outstanding_performance or 0) +
        #    (self.suggestions_that_contributed_to_changes or 0)
        #)

        # Sum the values and round to the first decimal place
        total = (
            (self.appraisal_rating or 0) +
            (self.commendation_for_outstanding_performance or 0) +
            (self.suggestions_that_contributed_to_changes or 0)
        )

        # Round the total to 1 decimal place
        self.total_appraisal_rating = round(total, 1)


        super(Appraisal, self).save(*args, **kwargs)

    #def calculate_quarterly_rating(self):
        #Calculates the rating for the current quarter based on performance fields
    #    rating_fields = [
    #        self.job_knowledge,
    #        self.quality_of_work,
    #        self.quantity_of_work,
    #        self.reliability,
    #        self.initiative_creativity,
    #        self.judgment,
    #        self.relationship_with_supervisor,
    #        self.working_with_others,
    #        self.relationship_with_subordinates,
    #        self.communication_skills
    #    ]
        # Filter out None values
    #    valid_ratings = [field for field in rating_fields if field is not None]
        
    #    if valid_ratings:
    #        return sum(valid_ratings) / len(valid_ratings)
    #    return None

    #def calculate_appraisal_rating(self):
    #    """Calculates the overall appraisal rating as the sum of quarterly ratings"""
    #    quarterly_ratings = [
    #        self.q1_appraisal_rating,
    #        self.q2_appraisal_rating,
    #        self.q3_appraisal_rating,
    #        self.q4_appraisal_rating
    #    ]
        # Filter out None values and sum the valid ratings
    #    valid_quarterly_ratings = [rating for rating in quarterly_ratings if rating is not None]

    #    if valid_quarterly_ratings:
    #        return sum(valid_quarterly_ratings)
    #    return None

    #def save(self, *args, **kwargs):
        # Calculate and assign the quarterly rating based on the appraisal period
    #    if self.appraisal_period == 'Q1':
    #        self.q1_appraisal_rating = self.calculate_quarterly_rating()
    #    elif self.appraisal_period == 'Q2':
    #        self.q2_appraisal_rating = self.calculate_quarterly_rating()
    #    elif self.appraisal_period == 'Q3':
    #        self.q3_appraisal_rating = self.calculate_quarterly_rating()
    #    elif self.appraisal_period == 'Q4':
    #        self.q4_appraisal_rating = self.calculate_quarterly_rating()

        # Update the overall appraisal rating (sum of all quarterly ratings)
    #    self.total_appraisal_rating = self.calculate_appraisal_rating()

    #    super(Appraisal, self).save(*args, **kwargs)
    
    details_of_commendation_for_outstanding_performance = models.TextField(blank = True, db_index = True, null = True,)
    sanction_discipline = models.CharField(max_length=50, choices=RADIO_CHOICES,null=True, db_index = True, blank=True)
    details_sanction_discipline = models.TextField(blank = True, db_index = True, null = True,)

    capacity_development_since_last_evaluation = models.TextField(blank = True, db_index = True, null = True,)
    accommplishments_since_last_evaluation = models.TextField(blank = True, db_index = True, null = True,)
    training_requirements_to_handle_responsibilities = models.TextField(blank = True, db_index = True, null = True,)
    skills_gap_requiring_improvement = models.TextField(blank = True, db_index = True, null = True,)
    missed_opportunities_reason = models.TextField(blank = True, db_index = True, null = True,)

    overall_performance_assessment = models.CharField(max_length=50, choices=OVERALL_PERFOMANCE_CHOICE, null=True, db_index = True, blank=True)
    promotability = models.CharField(max_length=50, choices=OVERALL_PERFOMANCE_CHOICE, null=True, db_index = True, blank=True)


    supervisor_comments = models.TextField(blank = True, db_index = True, null = True,)
    supervisor_date_of_evaluation = models.DateField(null=True, db_index = True, blank=True)
    
    head_of_department_comments = models.TextField(max_length = 255, blank = True, db_index = True, null = True,)
    head_of_department_date_of_evaluation = models.DateField(null=True, db_index = True, blank=True)
    appraisal_type = models.CharField(max_length=50, choices=[('staff', 'Staff'), ('supervisor', 'Supervisor')])
    # FSM status for workflow
    appraisal_status = FSMField(default='initiated', choices=STATUS)
    exam_location = models.CharField(max_length=50, db_index = True)

    @transition(field=appraisal_status, source='initiated', target='supervisor_review')
    def supervisor_review(self):
        pass

    @transition(field=appraisal_status, source='supervisor_review', target='hod_review')
    def hod_review(self):
        pass

    @transition(field=appraisal_status, source='hod_review', target='completed')
    def complete(self):
        pass

    
    def __str__(self):
        return f'{self.staff} - {self.full_name} - {self.appraisal_status}'
    

class JobDescription(models.Model):
    appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE, related_name='job_descriptions')
    activity_task = models.CharField(max_length=255, null=True, db_index = True, blank=True)
    overall_assessment_of_performance = models.TextField(null=True, db_index = True, blank=True)

    def __str__(self):
        return self.activity_task
    

class TrainingCourseSeminars(models.Model):
    appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE, related_name='training_course_seminars')
    training_program_type = models.TextField(null=True, db_index = True, blank=True)
    training_location = models.TextField(null=True, db_index = True, blank=True)
    training_from_date = models.DateField(null=True, db_index = True, blank=True)
    training_to_date = models.DateField(null=True, db_index = True, blank=True)

    def __str__(self):
        return self.training_program_type
