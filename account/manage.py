from django.contrib.auth.models import BaseUserManager

class CustomeUser(BaseUserManager):
    def create_user(self,first_name,last_name, email, password, **extrat_fields):
        if not email:
            raise ValueError('le champ mail ne peut pas etre vide')
        user = self.model(
                            first_name = first_name,
                            last_name = last_name,
                            email=email,
                            **extrat_fields
                          )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,first_name,last_name, email, password,**extrat_fields):
        extrat_fields.setdefault('is_staff', True)
        extrat_fields.setdefault('is_active', True)
        extrat_fields.setdefault('is_superuser', True)
        return self.create_user(first_name=first_name,
                                last_name= last_name,
                                email=email,
                                password=password,
                                **extrat_fields)