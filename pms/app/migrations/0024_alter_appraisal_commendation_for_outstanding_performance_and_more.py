# Generated by Django 5.0.1 on 2024-09-20 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_rename_q1_appraisal_rating_appraisal_appraisal_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='commendation_for_outstanding_performance',
            field=models.CharField(blank=True, choices=[('yes', 'YES'), ('no', 'NO')], db_index=True, default='no', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='overall_performance_assessment',
            field=models.CharField(blank=True, choices=[('Outstanding', 'A - Outstanding'), ('Very Good', 'B - Very Good'), ('Good', 'C - Good'), ('fair', 'D - Fair'), ('Poor', 'E - Poor'), ('Very Poor', 'F - Very Poor')], db_index=True, default='Good', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='project_assigment_completion_time',
            field=models.CharField(blank=True, choices=[('DAILY', 'DAILY'), ('WEEKLY', 'WEEKLY'), ('MONTHLY', 'MONTHLY'), ('YEARLY', 'YEARLY')], db_index=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='promotability',
            field=models.CharField(blank=True, choices=[('Outstanding', 'A - Outstanding'), ('Very Good', 'B - Very Good'), ('Good', 'C - Good'), ('fair', 'D - Fair'), ('Poor', 'E - Poor'), ('Very Poor', 'F - Very Poor')], db_index=True, default='Good', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='sanction_discipline',
            field=models.CharField(blank=True, choices=[('yes', 'YES'), ('no', 'NO')], db_index=True, default='no', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='suggestions_that_contributed_to_changes',
            field=models.CharField(blank=True, choices=[('yes', 'YES'), ('no', 'NO')], db_index=True, default='no', max_length=5, null=True),
        ),
    ]
