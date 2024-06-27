from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone

# creo un azione in maniera automatica specificando anche il target
# aggiungo solo azioni nuove, non quelle ripetute più volte dallo stesso utente nel giro di poco tempo (un minuto)
def create_action(user, verb, target=None):
    # guardo se qualcuno ha fatto la stessa azione entro un minuto
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)
    
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        # salvo l'azione
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    
    return False