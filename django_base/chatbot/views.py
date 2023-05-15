import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.dispatch import Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

import re
import json
import os
import openai
import spacy
import uuid
from textblob import TextBlob
from .models import Configuration, ChatMessage , ChatSession, Sentence, Token, Intent, IntentType
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import openai_wrapper, dalle_wrapper


class chatbot(LoginRequiredMixin, View):
    def config(self, id):
        config = Configuration.objects.get(id=id)
        return config

    def get(self, request):
        #create a session
        return render(request, 'chatbot.html')
    
    def interact(self, role, user, message, session, json_data):
        print("CHATBOT:interact")
        print(f"CHATBOT: user : {user}")
        print(message)
        intent = self.cog_primary_intent(message)
        print(f"intent is {intent}")
        
        chat_message = self.save_message(message, role, user, session)

        try:
            if intent:
                if 'INSTRUCT' in intent:
                    # handle dialog intent
                    message = "I'm on it"
                    return JsonResponse({'response': message})
                else:
                    print(f"CHATBOT: in final intent else : {intent}")
                    return( self.cog_dialog(chat_message, session))
                
        except Exception as e:
            print(e)
            return JsonResponse({'response': 'I am sorry, I do not understand.'})
        
        return JsonResponse({'response': 'I am sorry, I do not understand.'})

    def cog_dialog(self, chat_message, session):
        print("CHATBOT: in cog_dialog")
  
        message = chat_message.message

        # check if we need to get context or if this is a standalone statement
        intent = self.cog_primary_intent(message)
        print(f"intent is {intent}")

        conversation = []
        contextRequest = openai_wrapper(message,'ContextRequest')

        if contextRequest['message'] == 'False':
            depth = 3 # min depth
        else:

            depth = int(contextRequest['message'])
            print(f"depth is {depth}")
        
        print(f'CHATBOT: the current session is {session.session_name}')
        recent_history = ChatMessage.objects.filter(session_id=session).order_by('-timestamp')[:depth]
        print("CHATBOT: RECENT_HISTORY")

        recent_history = recent_history[::-1]
        previous_msg_id = None

        for prompt_message in recent_history:
            print(f"PROMPT_MESSAGE {prompt_message}")
            prompt = {"role":prompt_message.role, "content":prompt_message.message}
            conversation.append(prompt)
            previous_msg_id = prompt_message

        print("CHATBOT: POST CONTEXT PROCESSING")
        prompt = {"role":chat_message.role, "content":chat_message.message}
        conversation.append(prompt)
        
        response = openai_wrapper(prompt, 'Lilith', conversation)
        
        print("CHATBOT: LLM RESPONSE")
        print(response)

        # print the response from the API to the console for debugging
        cm_bot = self.save_message(response["message"], 'assistant', session.author, session, json = response , previous_msg_id=previous_msg_id)
        codify = self.convert_markdown_to_html(cm_bot.message)

        return JsonResponse({'response': codify})

    def save_message(self, message, role, user, session, json = None, previous_msg_id = None ):        
        # create a new chat message object
        cm = ChatMessage.objects.create(author=user, 
                                        session_id = session, 
                                        previous_msg_id = previous_msg_id,
                                        message=message,
                                        role=role,
                                        json=json)

        nlp = spacy.load("en_core_web_sm")
        print(f"ROLE: {role}")


        # save the object
        cm.save()
        nlp_message = nlp(cm.message)
        position = 0
        for sent in nlp_message.sents:
            sentence_id = str(uuid.uuid4())
            position += 1
            sentence = sent.text.strip()
            blob = TextBlob(sentence)
            sentiment_score = blob.sentiment.polarity
            sentence = Sentence.objects.create(id=sentence_id,
                                                  sentence=sentence,
                                                    sentiment=sentiment_score,
                                                    session_id=session,
                                                    position=position, 
                                                    role = role,
                                                    chat_message_id=cm)
            sentence.save()
            token_pos = 0
            for token in sent:
                token_pos += 1
                # print(token.text, token.pos_, token.dep_)
                # check if the token is an entity and determine the entity type
                if token.ent_type_:
                    entity = token.ent_type_
                else:
                    entity = None
                
                token = Token.objects.create(id=str(uuid.uuid4()),
                                                position=token_pos,
                                                sentence_id=sentence,
                                                token=token.text,
                                                pos=token.pos_,
                                                dep=token.dep_,
                                                entity=entity,
                                                stop_word=token.is_stop,
                                                lemma=token.lemma_)
                token.save()
        
        return cm
    
    def cog_primary_intent(self, message):
        print("CHATBOT: in cog_primary_intent")
        intent = openai_wrapper(message,'PrimeIntent')
        return intent["message"]
    

    def convert_markdown_to_html(self, text):   
         # Replace ``` start and end tags with <pre><code> and </pre></code> tags\n    
         pattern = re.compile(r'```(.*?)```', re.DOTALL)
         text = re.sub(pattern, r'<pre><code>\1</code></pre>', text)    
         return text
    
    def convert_slash_n_to_br(self, text):   
         # Replace \n to <br> tags
         text = text.replace('\n', '<br>')
         return text
