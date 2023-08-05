from django.db import models


class PersonName(models.Model):

    # ## name_type:coded_text:optional
    # suggested values from CKM are
    NAME_TYPE_CHOICES = (
        ('REGISTERED',   'Registered name [The name by which the subject is officially registered.]'),
        ('PREVIOUS',     'Previous name [Name previously used by this person.]'),
        ('BIRTH',        'Birth name [Name given to this person at birth.]'),
        ('AKA',          'AKA [Person also known as.]'),
        ('ALIAS',        'Alias [Other name used by this person.]'),
        ('MAIDEN',       'Maiden Name [Name used by this persion before marriage.]'),
        ('PROFESSIONAL', 'Professional name [The name used by the subject for business or professional purposes.]'),
        ('REPORTING',    'Reporting name [The subject’s name as it is to be used for reporting, when used with a specific identifier.]'),
    )
    name_type = models.CharField(
        max_length=255,
        choices=NAME_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="The type of name described"
    )

    # ## preferred_name
    # boolean
    # optional
    preferred_name = models.NullBooleanField(
        null=True,
        blank=True,
        help_text="Indicates that this is the name by which a person chooses to be identified."
    )

    # unstructured_name:text:optional
    unstructured_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Name in free text unstructured format."
    )

    # ## Structured name ## #
    # cluster:optional:Minimum of 2 items
    # Name in structured format.

    # title:text:optional
    # no canonical list of titles was suggested in the archetype
    # FHIR, NHS data dictionary also do not have a canonical list
    TITLE_CHOICES = (
        ('DR', 'Dr.'),
        ('MRS', 'Mrs.'),
        ('MR', 'Mr.'),
        ('MISS', 'Miss'),
        ('MS', 'Ms.'),
        ('PROF', 'Prof.'),
        ('SIR', 'Sir'),
        ('REV', 'Rev'),
    )

    title = models.CharField(
        max_length=20,
        choices=TITLE_CHOICES,
        null=True,
        blank=True,
        help_text="The prefix or title used by the subject, e.g. Mr, Mrs, Ms, Dr, Lord"
    )

    # text:mandatory
    given_name = models.CharField(
        null=True,  # nullable on DB to avoid a default value
        max_length=255,
        help_text="Given / personal / first name."
    )

    # middle_name:text:optional:repeating
    # 'Coded Text' in the UK CKM but I don't think they really mean that
    middle_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Middle name or names."
    )

    # family_name:text:mandatory
    family_name = models.CharField(
        null=True,  # nullable on DB to avoid a default value
        max_length=255,
        help_text="Family name or Surname.")

    # suffix:text:optional
    suffix = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Additional term used following a person name, e.g. 'Snr'")

    # validity_period:interval_of_date/time:optional
    validity_period_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date from which this name was valid."
    )
    validity_period_to = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date until which this name was valid."
    )

    def __str__(self):
        if (self.given_name and self.given_name):
            return self.given_name + ' ' + self.family_name
        elif self.unstructured_name:
            return self.unstructured_name
        else:
            return 'anonymous'
