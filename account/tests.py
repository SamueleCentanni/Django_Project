from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from .models import Profile, Contact



# questo test ha come obiettivo:
# - verificare che un utente non loggato non possa visualizzare nulla e venga rediretto alla pagina di Login -> OK
# - verificare che un utente correttamente loggato e che segue il nostro profilo PRIVATO, possa vedere tutto -> OK
# - verificare che un utente correttamente loggato e che NON segue il nostro profilo PRIVATO, possa vedere il profilo ma veda solamente la scritta
#   "Questo profilo è privarto" -> OK

class UserDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Creazione del profilo per l'utente
        self.profile = Profile.objects.create(user=self.user, date_of_birth='1990-01-01')
        
        self.url = reverse('user_detail', args=[self.user.username])

    def test_user_detail_view_private_profile(self):
        # Impostiamo il profilo come privato
        self.profile.private = True
        self.profile.save()

        # Utente non loggato non deve vedere il profilo privato: deve essere reinderizzato (alla pagina di login)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        # Utente loggato che segue l'utente può vedere il profilo privato
        self.client.force_login(self.user)
        follower = User.objects.create_user(username='follower', password='testpassword')
        Contact.objects.create(user_from=follower, user_to=self.user)  # follower segue self.user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user/detail.html')
        self.assertNotContains(response, '<h2>Questo profilo è privato</h2>')

        # Utente loggato che non segue l'utente non può vedere il profilo privato
        third_user = User.objects.create_user(username='thirduser', password='testpassword')
        self.client.force_login(third_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user/detail.html')
        self.assertInHTML('<h2>Questo profilo è privato</h2>', response.content.decode())
