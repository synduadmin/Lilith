def navigation(request):
    if request.user.is_authenticated:
        navigation_options = [
            {'name': 'Chatbot', 'url': '/chatbot/'},
            {'name': 'Todo', 'url': '/todo/'},
            {'name': 'Dev', 'url': '/dev/'},
            {'name': 'Studio', 'url': '/studio/'},
            {'name': 'Front-page', 'url': '/'},
            {'name': 'Blog', 'url': '/blog/'},
            {'name': 'Contact', 'url': '/contact/'},
            {'name': 'About', 'url': '/about/'},
            {'name': 'Terms', 'url': '/terms/'},
            {'name': 'Privacy', 'url': '/privacy/'},
        ]
    else:
        navigation_options = [
            {'name': 'Front-page', 'url': '/'},
            {'name': 'Blog', 'url': '/blog/'},
            {'name': 'Contact', 'url': '/contact/'},
            {'name': 'About', 'url': '/about/'},
            {'name': 'Terms', 'url': '/terms/'},
            {'name': 'Privacy', 'url': '/privacy/'},
        ]

    return {
        'navigation_options': navigation_options
    }
