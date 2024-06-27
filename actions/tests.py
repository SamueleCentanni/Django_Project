from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Action
from .utils import create_action

class CreateActionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_action_account_created(self):
        # Testa che l'azione "ha creato un account" venga registrata correttamente
        result = create_action(self.user, 'ha creato un account')
        self.assertTrue(result)
        self.assertEqual(Action.objects.count(), 1)
        action = Action.objects.first()
        self.assertEqual(action.user, self.user)
        self.assertEqual(action.verb, 'ha creato un account')
        self.assertIsNone(action.target)
    
    def test_create_action_no_duplicate_within_one_minute(self):
        # Crea un'azione "ha creato un account"
        create_action(self.user, 'ha creato un account')
        
        Action.objects.update(created=timezone.now() - timedelta(minutes=0, seconds=10))

        # Prova a creare una seconda azione identica entro un minuto
        result = create_action(self.user, 'ha creato un account')
        self.assertFalse(result)
        self.assertEqual(Action.objects.count(), 1)
    
    def test_create_action_after_one_minute(self):
        # Crea un'azione "ha creato un account"
        create_action(self.user, 'ha creato un account')
        
        # Simula il passaggio di un minuto
        Action.objects.update(created=timezone.now() - timedelta(minutes=1, seconds=1))
        
        # Prova a creare una seconda azione identica dopo un minuto
        result = create_action(self.user, 'ha creato un account')
        self.assertTrue(result)
        self.assertEqual(Action.objects.count(), 2)
