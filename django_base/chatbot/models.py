from django.db import models
from django.conf import settings 
import uuid
from simple_history.models import HistoricalRecords
#from .signals import short_term_memory

IntentType = (
    (0,"Conversation"),
    (1,"Blog")
)

class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    prime = models.TextField(null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    max_tokens = models.IntegerField(null=True, blank=True)
    top_p = models.FloatField(null=True, blank=True)
    top_k = models.IntegerField(null=True, blank=True)
    frequency_penalty = models.FloatField(null=True, blank=True)
    presence_penalty = models.FloatField(null=True, blank=True)
    stop = models.CharField(max_length=200, null=True, blank=True)
    default_depth = models.IntegerField(null=True, blank=True)
    api_key = models.CharField(max_length=200, null=True, blank=True)
    org_id = models.CharField(max_length=200, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='session_author')
    session_name = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return self.session_name
    
class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    previous_msg_id = models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE, related_name='previous_msg_id_rel')
    session_id = models.ForeignKey(ChatSession, 
                                   on_delete= models.CASCADE, 
                                   related_name='session_id', 
                                   null=True, 
                                   blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='message_author', null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    json = models.JSONField(null=True, blank=True)
    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        try:
            if self.pk is None:
                super().save(*args, **kwargs)  # Call the "real" save() method.
                #short_term_memory.send(sender=self)
        except Exception as e:
            print("something went wrong with sending the signal")
            
    def __str__(self):
        return self.message if self.message else "Unnamed instance"
    
class Sentence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    chat_message_id = models.ForeignKey(ChatMessage,
                                        on_delete= models.CASCADE,
                                        related_name='sentence_chat_message_id',
                                        null=True,
                                        blank=True
                                        )
    sentence = models.TextField(null=True, blank=True)
    sentiment = models.FloatField(null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    session_id = models.ForeignKey(ChatSession, 
                                   on_delete= models.CASCADE, 
                                   related_name='sentence_session_id', 
                                   null=True, 
                                   blank=True)
    position = models.IntegerField(null=True, blank=True)
    class Meta:
        ordering = ['chat_message_id','position']

    def __str__(self):
        return self.sentence
    
class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    position = models.IntegerField(null=True, blank=True)
    sentence_id = models.ForeignKey(Sentence,
                                    on_delete= models.CASCADE,
                                    related_name='token_sentence_id',
                                    null=True,
                                    blank=True
                                    )
    token = models.TextField(null=True, blank=True)
    pos = models.TextField(null=True, blank=True)
    dep = models.TextField(null=True, blank=True)
    entity = models.TextField(null=True, blank=True)
    stop_word = models.BooleanField(null=True, blank=True)
    lemma = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['sentence_id','position']

    def __str__(self):
        return self.token

class Intent(models.Model):
    id = models.IntegerField(primary_key=True)
    intent_name = models.CharField(max_length=200, null=True, blank=True)
    intent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['intent_name']

    def __str__(self):
        return self.intent