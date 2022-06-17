from tortoise.models import Model
from tortoise import fields


class Installments(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    date = fields.DateField()
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync


class Attendance(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    institute = fields.ForeignKeyField('models.Institutes', null=True)
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync


class Branches(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Governorates(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Institutes(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Posters(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


# class Authorities(Model):
#     id = fields.IntField(pk=True)
#     name = fields.TextField()
#     state = fields.ForeignKeyField("models.States")


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.TextField()
    password = fields.TextField()
    unique_id = fields.TextField()
    name = fields.TextField(null=True)
    super = fields.IntField(default=0, null=True)
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync


class UserAuth(Model):
    id = fields.IntField(pk=True)
    state = fields.ForeignKeyField("models.States")
    user = fields.ForeignKeyField("models.Users")
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync

    class Meta:
        table = "user_auth"


class Students(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    photo = fields.TextField(null=True)
    qr = fields.TextField(null=True)
    school = fields.TextField(null=True)
    branch = fields.ForeignKeyField("models.Branches", null=True)
    governorate = fields.ForeignKeyField("models.Governorates", null=True)
    institute = fields.ForeignKeyField("models.Institutes", null=True)
    state = fields.ForeignKeyField("models.States", null=True)
    first_phone = fields.TextField(null=True)
    second_phone = fields.TextField(null=True)
    code_1 = fields.TextField(null=True)
    code_2 = fields.TextField(null=True)
    telegram_user = fields.TextField(null=True)
    created_at = fields.DateField(null=True)
    note = fields.TextField(null=True)
    total_amount = fields.FloatField(null=True)
    poster = fields.ForeignKeyField("models.Posters", null=True)
    remaining_amount = fields.FloatField(null=True)
    dob = fields.TextField(null=True)
    banned = fields.IntField(default=0)
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync


class StudentInstallments(Model):
    id = fields.IntField(pk=True)
    installment = fields.ForeignKeyField("models.Installments", null=True)
    date = fields.DateField(null=True)
    amount = fields.IntField(null=True)
    invoice = fields.IntField(null=True)
    received = fields.IntField(null=True)
    student = fields.ForeignKeyField("models.Students", null=True)
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync

    class Meta:
        table = "student_installments"


class StudentAttendance(Model):
    id = fields.IntField(pk=True)
    attendance = fields.ForeignKeyField("models.Attendance", null=True)
    attended = fields.IntField(null=True)
    student = fields.ForeignKeyField("models.Students", null=True)
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync

    class Meta:
        table = "student_attendance"


class States(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    unique_id = fields.TextField()
    delete_state = fields.IntField(default=0)  # 1 need to sync
    patch_state = fields.IntField(default=0)  # 1 need to sync
