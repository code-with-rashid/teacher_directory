from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from directory.models import Teacher


@receiver(m2m_changed, sender=Teacher.subjects.through)
def subjects_changed(sender, **kwargs):
    if kwargs['instance'].subjects.count() > 5:
        raise ValidationError("You can't assign more than 5 subjects")


# m2m_changed.connect(subjects_changed, sender=BlogSite.regions.through)