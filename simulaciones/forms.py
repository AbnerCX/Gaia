from django import forms

class SimulacionForm(forms.Form):
    humedad = forms.DecimalField(max_digits=5, decimal_places=2, label="Humedad", required=True)
    temperatura = forms.DecimalField(max_digits=5, decimal_places=2, label="Temperatura", required=True)
    precipitacion = forms.DecimalField(max_digits=5, decimal_places=2, label="Precipitación", required=True)
