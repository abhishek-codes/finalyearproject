from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.contrib import messages
from django.core.mail import send_mail

def home_page(request):
    # template_name = "home.html"
    # template_obj = get_template(template_name)
    # print("##debug",request.user)
    # print("##debug2",request.user.get_profile_pic())
    return redirect('/forum')
 
def contact(request):
    template_name = "contactus.html"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')
        message = "{0} \n\n form {1}".format(msg,name)
        send_mail(subject,message,email,['abhishek73knp@gmail.com'],fail_silently=False)
        messages.success(request,'Successfully Send')
        return redirect('/contactus')
    return render(request,template_name)
