from django.core.mail import send_mail
mail = ''

def send_payment_notification(self, recipient, amount):
        # Préparer et envoyer un email ou une autre notification
        subject = "Paiement de la tontine"
        message = f"Bonjour {recipient.first_name},\n\nVous avez reçu un paiement de {amount} dans le cadre de la tontine {self.name}.\n\nMerci pour votre participation !"
        recipient_email = recipient.email

        # Envoi de l'email (ou SMS ou autre méthode)
        send_mail(subject, message, 'mail', [recipient_email])

        