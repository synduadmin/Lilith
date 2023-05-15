# BLOG APP - signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from urllib.parse import quote_plus

from chatbot.models import ChatMessage, Sentence, Token
from core.views import openai_wrapper, dalle_wrapper
from files_core.models import UploadedFile
from .models import Post, Category
from django.utils.safestring import mark_safe
from files_core.utility import download_file
from core.models import AIConfiguration
from uuid import uuid4
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

# Import create_asset function and Provider, Style classes
from studio.assets import create_asset
from studio.models import AssetProvider, Asset

def blog_illustrate(post):
    logger.debug("in blog illustrate function")
    try:
        logger.debug(f"in blog illustrate for the prompt: {post.content}")
        visual_prompt = openai_wrapper(post.content, 'VisualPrompt') # return a json
        prompt = visual_prompt["message"]

        # Fetch the provider and style
        provider = AssetProvider.objects.get(name='Dall-E2')
        style = 'Dall-E2-Studio-Ukiyo-E'
        style_config = AIConfiguration.objects.filter(name=style).first()

        # Assuming a user model exists and we use the first user for this example
        user = post.author

        # Call create_asset with 'image' as first argument
        asset = create_asset(user, 'image', prompt,  provider, style_config)

        # Return the URL of the file and the prompt
        return asset.file.url, prompt

    except Exception as e:
        logger.debug(f"Error in blog illustrate : {e}")
        return ''

@receiver(post_save, sender=ChatMessage)
def blog_talent(sender, instance, created, **kwargs):
    # Do something asynchronously when the signal is received
    logger.debug(f"the short term memory (stm) signal has been received {instance.message}, {kwargs}")
    logger.debug(f"the chat message role is {instance.role}")
    if instance is None or instance.role == 'assistant':
        if instance.role == 'assistant':
            logger.debug('we do not let lilith go into a wrong self loop')
            logger.debug(f'instance message is {instance.message}')
        return

    # first we check if this is a blog request by invoking the new interactions module
    is_blog_request = openai_wrapper(instance.message, 'BlogRequest')
    logger.debug(f"the result of is blog request is {is_blog_request}")

    if (is_blog_request['status'] == '1' and is_blog_request['message'] == 'True'):
        logger.debug("this is a blog request")
        # Start creating a blog post 
        # get the cardinal value of the number of messages required for context:

        # there are two types of blog requests:
        # 1. one which is a standalone statement which states which topic I wish Lilith to write about
        # 2. the second one is a context-based request, which asks to review the conversation.
        # the second request can be of two types:
        # 2.1. a request to review the conversation and format it as is, as a log of the conversation
        # 2.2. a request to review the conversation and format it as a blog post, summarizing key themes and ideas
        # 3. the third one is for the entire session, which is a request to review the entire session and format it as a blog post

        post = Post()

        # why don't i create a cognitive function which determines what kind of blog request is desired?
        blog_request_type = openai_wrapper(instance.message, 'blogRequestTypeClassifier')
        logger.debug (f"blog request type is {blog_request_type['message']}")

        if 'TOPIC' in blog_request_type['message']:
            logger.debug("the system went into the first type of blog request")
            # this is a standalone blog request
            # we check if the blog post needs a body
            blogBodyRequest = openai_wrapper(instance.message, 'BlogBodyRequest')
            # we check if the blog post needs a title
            post.content = blogBodyRequest["message"]

        elif 'LOG' in blog_request_type['message']:
            blogContextRequest = openai_wrapper(instance.message, 'ContextRequest')

            conversation = []
            if blogContextRequest['message'] == 'False':
                depth = 10
            else:
                depth = int(blogContextRequest['message'])

            logger.debug(f"depth is {depth}")
            try:
                depth = int(depth)
                if depth > 0:
                    logger.debug("inside context extraction for blog post")
                    recent_history = ChatMessage.objects.all().filter(author=instance.author).order_by('-timestamp')[:depth]
                    recent_history = recent_history[::-1]
                    logger.debug(f"recent history is {recent_history}")
                    for prompt_message in recent_history:
                        prompt = {"role":prompt_message.role, "content":prompt_message.message}
                        conversation.append(prompt)

            except Exception as e:
                logger.debug(f"line 80: error retrieving recent history: {e} :for depth {depth}")
        
            try:
                blogBodyConversationRequest = openai_wrapper(instance.message, 'BlogBodyRequest', conversation)
                post.content = blogBodyConversationRequest["message"]
                for message in conversation:
                    # format the message for publication based on the role of the speaker
                    formatted_message = ""
                    logger.debug("in signals.py line 88")
                    logger.debug(message["role"])
                    if message["role"] == "user":
                        str = message["content"]
                        post.content += '<div class="message user_message">'+str+'</div>'
                    if message["role"] == "assistant":
                        str = message["content"]
                        post.content += '<div class="message assistant_message">'+str
                        img, alt_image = blog_illustrate(formatted_message["message"])
                        post.content += f'<img src="{img["message"]}" alt="{mark_safe(alt_image["message"])}" class="img-fluid"/>'
                        post.content += '</div>'
            except Exception as e:
                logger.debug(f"line 98: error formatting conversation: {e} :for depth {depth}")
        
        elif 'SUMMARY' in blog_request_type['message']:
            blogContextRequest = openai_wrapper(instance.message, 'ContextRequest')

            conversation = []
            if blogContextRequest['message'] == 'False':
                depth = 10
            else:
                depth = int(blogContextRequest['message'])

            logger.debug(f"depth is {depth}")
            try:
                depth = int(depth)
                if depth > 0:
                    logger.debug(f"inside context extraction for summarized blog post {depth}")
                    recent_history = ChatMessage.objects.all().filter(author=instance.author).order_by('-timestamp')[:depth]
                    recent_history = recent_history[::-1]

                    for prompt_message in recent_history:
                        prompt = {"role":prompt_message.role, "content":prompt_message.message}
                        conversation.append(prompt)

            except Exception as e:
                logger.debug(f"line 109: error retrieving recent history: {e} : for depth {depth}")
        
            blogBodyRequest = openai_wrapper(instance.message, 'BlogBodyRequest', conversation)
            post.content = blogBodyRequest["message"]
        else:
            logger.debug(f"blog type request classifier returned the following label: {blog_request_type['message']}")
            return

        logger.debug("finished structuring the body of the post")

        blogTitleRequest = openai_wrapper(post.content, 'BlogTitleRequest')

        # compute a unique title for the blog post
        post.title = blogTitleRequest["message"]
        post.title = post.title.strip('"')
        # check that the title of the blog post is unique
        is_unique = Post.objects.filter(title=post.title).count()
        # as long as the title is not unique, loop
        while is_unique > 0:
            blogTitleRequest = openai_wrapper(post.content, 'BlogTitleRequest')
            post.title = blogTitleRequest["message"]
            post.title = post.title.strip('"')
            is_unique = Post.objects.filter(title=post.title).count()
        
        logger.debug("finished structuring the title of the post")
        # if the title contains title: or Title: or TITLE: then we remove it
        try:
            if post.title.startswith('title:') or post.title.startswith('Title:') or post.title.startswith('TITLE:'):
                post.title = post.title[6:]
        except Exception as e:
            logger.debug(f"error in title formatting: {e}")

        content = openai_wrapper(post.content, 'EditText')
        post.content = content["message"]
        logger.debug(post.content)

        post.slug = slugify(blogTitleRequest["message"])
        post.status = 0
        post.author = instance.author
        # compute an image for the blog post using dall-e2

        logger.debug("invoking blog_illustrate")

        post.featured_image, post.alt_image = blog_illustrate(post)
        if settings.ENVIRONMENT == 'development':
            post.featured_image = 'http://localhost:8000' + post.featured_image

        logger.debug(post.featured_image, post.alt_image )

        # then we check if the blog post needs a category / multiple categories
        blogCategoryRequest = openai_wrapper(post.content, 'ContentCategoryCreate')
        postCategory = blogCategoryRequest["message"]
        logger.debug(f"post category is {postCategory}")
        categories_to_set = []
        # if the category doesn't exist, create the category
        if Category.objects.filter(name=postCategory).count() == 0:
            category = Category(name=postCategory)
            category.slug = slugify(postCategory)
            category.save()
        else:
            category = Category.objects.filter(name=postCategory).first()
        categories_to_set.append(category)

        post.save()
        logger.debug("finished saving the post first time")
        # persist category data which has a many to many relationship with the post
        post.categories.set(categories_to_set)

        try:
            # autonomously publish
            post.status = 1
            post.save()
            logger.debug("finished saving the post second time")
                # Send a message to a group
            room_group_name = "chat_" + instance.session_id.session_name

            '''blog_post = quote_plus("Here's the text: " + post.content)
            logger.debug(f"sending the blog post to the channel layer via room_group_name  {room_group_name} ")
            async_to_sync(channel_layer.group_send)(
                room_group_name,  # Group name
                {"type": "chat_message", "message": blog_post},
            )'''
            return
        except Exception as e:
            logger.debug(f"error in publishing the post: {e}")


    pass
