from django import forms


class ContactoForm(forms.Form):
    ASUNTO_CHOICES = [
        ("consulta", "Consulta General"),
        ("prensa", "Prensa / Medios"),
        ("derechos", "Derechos / Agente"),
        ("fan", "Fan Mail"),
    ]

    nombre = forms.CharField(label="Nombre", max_length=255)
    email = forms.EmailField(label="Email")
    asunto = forms.ChoiceField(label="Asunto", choices=ASUNTO_CHOICES)
    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea)

    # Honeypot: los humanos no deberían rellenarlo
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            # Si el honeypot tiene algo, asumimos bot y lanzamos error silencioso
            raise forms.ValidationError("Bot detectado.")
        return value
