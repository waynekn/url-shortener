from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Link
from .forms import LinkForm


def index(request):
    """
    Renders the home view displaying all available links.

    This view retrieves all links from the database and passes them 
    to the 'index.html' template for rendering.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML page with the list of links.
    """
    links = Link.objects.all()
    context = {
        'links': links,
    }
    return render(request, 'links/index.html', context)


def root_link(request, link_slug):
    """
    Redirects the user to the full URL associated with the given link slug.

    This view is invoked when a user clicks on a link slug. It retrieves the 
    corresponding URL from the database using the provided slug. If the slug is 
    valid, it increments the click count for the link and redirects the user to 
    the actual URL.

    Args:
        request (HttpRequest): The HTTP request object.
        link_slug (str): The slug used to identify the link in the database.

    Returns:
        HttpResponse: A redirect response to the full URL associated with the slug.
    """
    link = get_object_or_404(Link, slug=link_slug)
    link.increment_clicks()

    return redirect(link.url)


def add_link(request):
    """
    Handles the creation of a new link. 

    This view processes both GET and POST requests:
    - On a GET request, it displays a form for the user to input a new link.
    - On a POST request, it validates the submitted data. If valid, the link is saved, 
      and the user is redirected to the home page.

    Returns:
        HttpResponse: Renders the link creation form or redirects to the home page
        upon successful form submission.
    """
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = LinkForm()

    context = {
        'form': form
    }
    return render(request, 'links/create.html', context)
