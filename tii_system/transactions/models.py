import os
import uuid
import base64
import time
from datetime import date
from django.db import models
from .validators import validate_file_size

''' <-------------------------- Function Upload ---------------------------> '''
def path_and_rename_cgs(instance, filename):
    upload_to   = date.today().strftime('documents/Certificate of Good Standing/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'CGS-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_ca(instance, filename):
    upload_to   = date.today().strftime('documents/Contractual Agreement/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'CA-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_pa(instance, filename):
    upload_to   = date.today().strftime('documents/Prospectus Agreement/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'PA-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_loi(instance, filename):
    upload_to   = date.today().strftime('documents/loi/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'LOI-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_loa(instance, filename):
    upload_to   = date.today().strftime('documents/loa/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'LOA-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_los(instance, filename):
    upload_to   = date.today().strftime('documents/los/%Y/%m/%d/')
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'LOS-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)

def path_and_rename_documents(instance, filename):
    upload_to   = date.today().strftime('documents/attachment/%Y/%m/%d/')
    name        = filename.split('.')[0]
    ext         = filename.split('.')[-1]
    timestamp   = time.time()
    enc_name    = base64.b64encode(f'{instance.trans_id.registration_code}|{timestamp}'.encode('ascii')).decode()
    filename    = f'{name}-{enc_name}.{ext}'
    return os.path.join(upload_to, filename)
''' <------------------------ End Function Upload -------------------------> '''


''' <--------------------------- Django Models ----------------------------> '''
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
''' <------------------------- End Django Models --------------------------> '''

''' <------------------------------- Models -------------------------------> '''
class Documents(models.Model):
    docs_id         = models.UUIDField(default=uuid.uuid4, primary_key=True)
    date_generated  = models.DateTimeField(blank=True, null=True)
    file_location   = models.FileField(upload_to=path_and_rename_documents, validators=[validate_file_size], max_length=200, blank=True, null=True)
    trans_id        = models.ForeignKey('Transaction', models.DO_NOTHING, db_column='trans_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'


class Logs(models.Model):
    trans_id    = models.OneToOneField('Transaction', models.DO_NOTHING, db_column='trans_id', primary_key=True)
    key         = models.CharField(max_length=50, blank=True, null=True)
    old         = models.CharField(max_length=100, blank=True, null=True)
    new         = models.CharField(max_length=100, blank=True, null=True)
    user_id     = models.BigIntegerField(blank=True, null=True)
    timestamps  = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class MstTracking(models.Model):
    track_id    = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name        = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_active   = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_tracking'


class Trackings(models.Model):
    timestamps  = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    trans_id    = models.OneToOneField('Transaction', models.DO_NOTHING, db_column='trans_id', primary_key=True)
    track_id    = models.ForeignKey(MstTracking, models.DO_NOTHING, db_column='track_id')

    class Meta:
        managed = False
        db_table = 'trackings'
        unique_together = (('trans_id', 'track_id'),)


class Transaction(models.Model):
    trans_id                = models.UUIDField(default=uuid.uuid4, primary_key=True)
    trans_type_id           = models.ForeignKey('TransactionTypes', models.DO_NOTHING, db_column='trans_type_id', blank=True, null=True)
    status                  = models.CharField(max_length=20, blank=True, null=True)
    approval_id             = models.IntegerField(blank=True, null=True)
    approval_name           = models.CharField(max_length=50, blank=True, null=True)
    approval_date           = models.DateField(max_length=50, blank=True, null=True)
    submit_date             = models.DateField(max_length=50, blank=True, null=True)
    comp_us_name            = models.CharField(max_length=100, blank=True, null=True)
    comp_us_president       = models.CharField(max_length=100, blank=True, null=True)
    comp_us_website         = models.CharField(max_length=45, blank=True, null=True)
    comp_us_legal_status    = models.CharField(max_length=25, blank=True, null=True)
    comp_us_establishment   = models.IntegerField(blank=True, null=True)
    comp_us_address         = models.CharField(max_length=100, blank=True, null=True)
    comp_us_city            = models.CharField(max_length=35, blank=True, null=True)
    comp_us_state           = models.CharField(max_length=35, blank=True, null=True)
    comp_us_zip             = models.CharField(max_length=10, blank=True, null=True)
    comp_us_phone           = models.CharField(max_length=25, blank=True, null=True)
    comp_us_fax             = models.CharField(max_length=25, blank=True, null=True)
    comp_us_email           = models.EmailField(max_length=45, blank=True, null=True)
    cert_good_standing      = models.FileField(upload_to=path_and_rename_cgs, validators=[validate_file_size], max_length=100, blank=True, null=True)
    line_of_business        = models.CharField(max_length=100, blank=True, null=True)
    product_offering        = models.CharField(max_length=100, blank=True, null=True)
    hs_code                 = models.CharField(max_length=50, blank=True, null=True)
    comp_idn_name           = models.CharField(max_length=100, blank=True, null=True)
    comp_idn_president      = models.CharField(max_length=100, blank=True, null=True)
    comp_idn_address        = models.CharField(max_length=100, blank=True, null=True)
    comp_idn_city           = models.CharField(max_length=35, blank=True, null=True)
    comp_idn_province       = models.CharField(max_length=35, blank=True, null=True)
    comp_idn_zip            = models.CharField(max_length=10, blank=True, null=True)
    comp_idn_phone          = models.CharField(max_length=25, blank=True, null=True)
    comp_idn_fax            = models.CharField(max_length=25, blank=True, null=True)
    comp_idn_email          = models.EmailField(max_length=45, blank=True, null=True)
    comp_idn_website        = models.CharField(max_length=100, blank=True, null=True)
    comp_idn_nationality    = models.CharField(max_length=100, blank=True, null=True)
    comp_idn_idnumber       = models.CharField(max_length=45, blank=True, null=True)
    comp_idn_rep_officer    = models.CharField(max_length=100, blank=True, null=True)
    term                    = models.CharField(max_length=25, blank=True, null=True)
    term_unit               = models.CharField(max_length=25, blank=True, null=True)
    type                    = models.CharField(max_length=25, blank=True, null=True)
    type_agency             = models.CharField(max_length=25, blank=True, null=True)
    cid                     = models.CharField(max_length=45, blank=True, null=True)
    applicant_name          = models.CharField(max_length=100, blank=True, null=True)
    applicant_position      = models.CharField(max_length=100, blank=True, null=True)
    applicant_city          = models.CharField(max_length=45, blank=True, null=True)
    registration_code       = models.CharField(max_length=45, blank=True, null=True, unique=True)
    renewal_type            = models.CharField(max_length=50, blank=True, null=True)
    contractual_agreement   = models.FileField(upload_to=path_and_rename_ca, validators=[validate_file_size], max_length=100, blank=True, null=True)
    prospectus_agreement    = models.FileField(upload_to=path_and_rename_pa, validators=[validate_file_size], max_length=100, blank=True, null=True)
    loi                     = models.FileField(upload_to=path_and_rename_loi, validators=[validate_file_size], max_length=100, blank=True, null=True)
    loa                     = models.FileField(upload_to=path_and_rename_loa, validators=[validate_file_size], max_length=100, blank=True, null=True)
    los                     = models.FileField(upload_to=path_and_rename_los, validators=[validate_file_size], max_length=100, blank=True, null=True)
    notes                   = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class TransactionTypes(models.Model):
    trans_type_id   = models.AutoField(primary_key=True)
    code            = models.CharField(max_length=20, blank=True, null=True)
    description     = models.CharField(max_length=200, blank=True, null=True)
    is_active       = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_types'
''' <------------------------------- Models -------------------------------> '''
