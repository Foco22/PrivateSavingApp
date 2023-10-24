from django.db import models

class DataBanks(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.TextField(null=True, default=None)
    description = models.TextField(null=True, default=None)
    amount = models.IntegerField(null=True, default=None)
    date = models.DateField(null=True, default=None)
    type_expenses = models.TextField(null=True, default=None)
    account_name = models.TextField(null=True, default=None)
    account_number = models.TextField(null=True, default=None)
    category_description = models.TextField(null=True, default=None)
    indicator_not_category = models.BooleanField(default=False)

    def __str__(self):
        return str(self.description)
    
class SavingTarget(models.Model):
    saving_target = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 

class ClassifiedData(models.Model):
    Fecha = models.DateField()
    Descripción = models.CharField(max_length=255)
    Cuenta = models.CharField(max_length=255)
    Moneda = models.CharField(max_length=50)
    Monto = models.DecimalField(max_digits=20, decimal_places=2)
    Tipo = models.CharField(max_length=50)
    SubCategoría = models.CharField(max_length=50)
    TipoUsuario = models.CharField(max_length=50)
    SubCategoriaUsuario = models.CharField(max_length=50)
