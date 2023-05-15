from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View

import re
import json
import os
import openai
import spacy
import uuid
from textblob import TextBlob

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import AIConfiguration, AIInteraction
from urllib.parse import quote_plus


def dalle_wrapper(prompt, style):
    print(f"Engaging Dall-E2 Wrapper: {prompt}")
    config = AIConfiguration.objects.filter(name=style).first()
    print(f"Config is {config}")
    visual_prompt = config.prime + prompt
    print(f" The statement sent to Dall-e2 is {visual_prompt}")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.api_key}',
    }
    
    data = {
        "model": config.model,
        "prompt": visual_prompt,
        "num_images": 1
    }

    try:
        response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=json.dumps(data))
        print(response.json())
        image_url = response.json()['data'][0]['url']
        print(image_url)
        return image_url
    except:
        return ''


def openai_wrapper(prompt, config_name, context=None):
    print("Engaging OpenAI Wrapper")
    config = AIConfiguration.objects.filter(name=config_name).first()
    if (config != None):

        print(config)
        openai.organization = config.org_id 
        openai.api_key = config.api_key
        print(f"context is {context}")
        
        prompts = []
        if (config.prime != None): 
            prime = {"role":"system", "content":config.prime}
            prompts.append(prime)
        if (context != None and context != {}):
            for p in context:
                prompts.append({"role":p["role"], "content":p["content"]})
        if (isinstance(prompt, str)):
            prompts.append({"role":"user", "content":prompt})


        print("OpenAI Wrapper: LLM API LOOKUP")
        response = openai.ChatCompletion.create(
            model = config.model,
            messages=prompts,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        print("OpenAI Wrapper: LLM RESPONSE")
        print(response)

        message = response.choices[0].message.content
        print(f"OpenAI Wrapper: Core Response, before message wrappers, is {message}")
        result_json = response

        interaction = AIInteraction(
            configuration_id=config, 
            input=prompt, 
            output=message, 
            role="user",
            json=result_json
            )
        interaction.save()

        return {'status':'1', 'message': message}
    else:
        return {'status':'0', 'message': "Configuration not found"}

@csrf_exempt
def ai_interaction(request):
    if request.method == 'POST':
        # extract priming prompt and driver configuration from request body
        data = json.loads(request.body.decode('utf-8'))
        config_name = data.get('config_name')
        prompt = data.get('prompt')
        context = data.get('context')
    
        print(config_name)
        print(prompt)
        ai_response = openai_wrapper(prompt, config_name, context)
        print(ai_response)

        if ai_response['status'] == 1:
            # return a JSON response to acknowledge receipt of priming prompt
            return JsonResponse(ai_response, status=200)
        else:
            return JsonResponse(ai_response, status=400)
