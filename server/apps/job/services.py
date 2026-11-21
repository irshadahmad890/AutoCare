from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.parts.models import Part
from .models import Estimate, EstimateStatus, Job, JobStatus


@transaction.atomic
def send_estimate(job_id, notes=''):
    job = Job.objects.select_for_update().get(pk=job_id)
    if job.status in [JobStatus.COMPLETED, JobStatus.CANCELLED]:
        raise ValidationError({'job': 'Cannot estimate a completed or cancelled job.'})
    estimate, _ = Estimate.objects.select_for_update().get_or_create(job=job)
    if estimate.status == EstimateStatus.APPROVED:
        raise ValidationError({'estimate': 'An approved estimate cannot be sent again.'})
    estimate.status = EstimateStatus.SENT
    estimate.notes = notes
    estimate.sent_at = timezone.now()
    estimate.responded_at = None
    estimate.approved_by = None
    estimate.save(update_fields=['status', 'notes', 'sent_at', 'responded_at', 'approved_by', 'updated_at'])
    job.status = JobStatus.AWAITING_APPROVAL
    job.save(update_fields=['status', 'updated_at'])
    return estimate


@transaction.atomic
def respond_to_estimate(job_id, customer, approve):
    job = Job.objects.select_for_update().select_related('vehicle__customer').get(pk=job_id)
    if job.vehicle.customer.user_id != customer.id:
        raise ValidationError({'job': 'This job does not belong to you.'})
    try:
        estimate = Estimate.objects.select_for_update().get(job=job)
    except Estimate.DoesNotExist:
        raise ValidationError({'estimate': 'No estimate has been sent for this job.'})
    if estimate.status != EstimateStatus.SENT:
        raise ValidationError({'estimate': 'Only a sent estimate can be answered.'})

    estimate.responded_at = timezone.now()
    if not approve:
        estimate.status = EstimateStatus.REJECTED
        estimate.save(update_fields=['status', 'responded_at', 'updated_at'])
        job.status = JobStatus.PENDING
        job.save(update_fields=['status', 'updated_at'])
        return estimate

    # Lock every involved part before validating stock so concurrent approvals
    # cannot oversell inventory. F() performs the deduction in the same transaction.
    job_parts = list(job.used_parts.select_related('part').order_by('part_id'))
    locked_parts = {part.id: part for part in Part.objects.select_for_update().filter(
        id__in=[item.part_id for item in job_parts]
    )}
    for item in job_parts:
        if locked_parts[item.part_id].stock < item.quantity:
            raise ValidationError({'parts': f'Insufficient stock for {item.part.name}.'})
    for item in job_parts:
        Part.objects.filter(pk=item.part_id).update(stock=F('stock') - item.quantity)

    estimate.status = EstimateStatus.APPROVED
    estimate.approved_by = customer
    estimate.stock_deducted = True
    estimate.save(update_fields=['status', 'approved_by', 'responded_at', 'stock_deducted', 'updated_at'])
    job.status = JobStatus.APPROVED
    job.save(update_fields=['status', 'updated_at'])
    return estimate


@transaction.atomic
def transition_job(job_id, new_status):
    job = Job.objects.select_for_update().get(pk=job_id)
    allowed = {
        JobStatus.PENDING: {JobStatus.AWAITING_APPROVAL, JobStatus.CANCELLED},
        JobStatus.AWAITING_APPROVAL: {JobStatus.PENDING, JobStatus.CANCELLED},
        JobStatus.APPROVED: {JobStatus.IN_PROGRESS, JobStatus.CANCELLED},
        JobStatus.IN_PROGRESS: {JobStatus.COMPLETED, JobStatus.CANCELLED},
    }
    if new_status not in allowed.get(job.status, set()):
        raise ValidationError({'status': f'Cannot transition from {job.status} to {new_status}.'})
    job.status = new_status
    job.save(update_fields=['status', 'updated_at'])
    return job
