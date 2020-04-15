from django.shortcuts import render
from .models import SearchQuery
from Forum.models import Post

# Create your views here.
def search_views(request):
    query = request.GET.get('q')
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = { "query": query}
    if query is not None:
        SearchQuery.objects.create(user=user,query=query)
        result_post = Post.objects.search(query=query)
        context['object_list'] = result_post
    return render(request,'search/view.html',context)