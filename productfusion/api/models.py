from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=255, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name

class User(models.Model):
    email = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    profile = models.JSONField(default=dict, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    organisations = models.ManyToManyField(Organisation, through='Member', related_name='users')

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=True)
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='members')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='members')
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return f"{self.user.email} in {self.organisation.name} as {self.role.name}"
