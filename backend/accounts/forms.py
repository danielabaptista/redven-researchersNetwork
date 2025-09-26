from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, StudentProfile, ResearcherProfile

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    user_type = forms.ChoiceField(
        choices=(("student","Estudiante"),("researcher","Investigador")),
        widget=forms.RadioSelect,
        label="Tipo de usuario"
    )

    # Student fields
    full_name = forms.CharField(max_length=200, label="Nombre y Apellido")
    city = forms.CharField(max_length=100, label="Ciudad")
    country = forms.CharField(max_length=100, label="País")
    university = forms.CharField(max_length=200, required=False,label="Universidad")
    bachelor_degree = forms.CharField(max_length=100,label="Pre-grado")

    # Researcher fields
    alma_mater = forms.CharField(max_length=200, required=False)
    current_university = forms.CharField(max_length=200, required=False, label="Universidad Actual")
    role = forms.ChoiceField(choices=ResearcherProfile.ROLE_CHOICES, required=False,label="Rol")

    class Meta:
        model = CustomUser
        fields = ("email", "user_type")  # only model fields here

    def clean(self):
        cleaned_data = super().clean()

        # Check passwords
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Passwords do not match")

        # Check required fields based on user_type
        user_type = cleaned_data.get("user_type")
        if user_type == "student":
            for field in ["full_name", "city", "country", "university", "bachelor_degree"]:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required")
        elif user_type == "researcher":
            for field in ["full_name", "city", "country", "alma_mater", "current_university", "bachelor_degree", "role"]:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required")

        return cleaned_data

    def save(self):
        data = self.cleaned_data
       # try:
        user = CustomUser.objects.create_user(
            email=data["email"],
            password=data["password1"],
            user_type=data["user_type"]
        )
        user.is_approved = False
        user.save()

        if data["user_type"] == "student":
            StudentProfile.objects.create(
                user=user,
                full_name=data["full_name"],
                city=data["city"],
                country=data["country"],
                university=data["university"],
                bachelor_degree=data["bachelor_degree"],
            )
            user.approved = False
            user.save()
        else:
            ResearcherProfile.objects.create(
                user=user,
                full_name=data["full_name"],
                city=data["city"],
                country=data["country"],
                alma_mater=data["alma_mater"],
                current_university=data["current_university"],
                bachelor_degree=data["bachelor_degree"],
                role=data["role"],
            )
            user.approved = False
            user.save()
        return user
        #except Exception as e:
         #   print("Error saving user:", e)
          #  return None



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
