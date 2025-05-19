from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse # Import reverse
from .models import Album, Review
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def album_list(request):
    album_list = Album.objects.all().order_by('title')
    paginator = Paginator(album_list, 10) # Show 10 albums per page
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    return render(request, 'music_albums/album_list.html', {'albums': albums})

def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    review_list = album.reviews.all().order_by('-created_at') # Default sort: newest first

    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'rating_asc':
        review_list = review_list.order_by('rating', '-created_at')
    elif sort_by == 'rating_desc':
        review_list = review_list.order_by('-rating', '-created_at')
    elif sort_by == 'date_asc':
        review_list = review_list.order_by('created_at')
    # else default to -created_at (newest first)

    paginator = Paginator(review_list, 5) # Show 5 reviews per page
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.album = album
            review.save()
            # Redirect to the album detail page (first page of reviews)
            return redirect(reverse('album_detail', kwargs={'album_id': album.id}))
    else:
        form = ReviewForm()
    return render(request, 'music_albums/album_detail.html', {
        'album': album, 
        'reviews': reviews, 
        'form': form,
        'current_sort': sort_by
    })

def albums_by_genre(request, genre_name):
    album_list_genre = Album.objects.filter(genre__iexact=genre_name).order_by('title')
    paginator = Paginator(album_list_genre, 10) # Show 10 albums per page
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    return render(request, 'music_albums/albums_by_genre.html', {'albums': albums, 'genre_name': genre_name})
