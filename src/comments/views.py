from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Comment
from Forum.models import Post
from Forum.views import detail_post_view

# Create your views here.

def comment_delete(request,id):
    print(id)
    # id = int(id)
    obj = get_object_or_404(Comment,id=id)
    template_name = 'delete.html'
    post_obj = None
    if request.method == 'POST':
        new_obj = obj
        print(Comment.get_content_type)
        print("##new_obj",new_obj,type(new_obj.content_type))
        print(obj.object_id,new_obj.object_id)
        # if obj.parent_id:
        #     new_obj = get_object_or_404(Comment,id=obj.object_id)
        #     print("####new_obj",new_obj)
        post_obj = get_object_or_404(Post,id=new_obj.object_id)
        print("##post_obj",post_obj)
        obj.delete()
        url = post_obj.get_absolute_url()
        messages.success(request,'Sucessfully Deleted')
        if post_obj:
            return redirect(url)
        else:
            return redirect("/forum")
    context = {
        "object" : f"comment of {obj.user}",
    }
    return render(request,template_name,context)

def comment_cancel(request,id):
    return redirect("/forum")