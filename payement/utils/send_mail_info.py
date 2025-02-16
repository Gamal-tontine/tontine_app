from django.core.mail import send_mail
mymail = 'dounoh0@gmail.com'

def sender_mail_for_info(email,subject,message):
    try:
        send_mail(subject=subject,message=message,from_email=mymail,recipient_list=[email],fail_silently=False)
        return True
    except ValueError:
        return False