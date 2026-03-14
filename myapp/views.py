from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import models
from .models import Studymaterial
from .models import profile as Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

# Create your views here.

SECRET_TEACHER_CODE='TEACHER123'

## home page
def index(request):
    return render(request,"index.html")

@login_required(login_url='login')
def dashboardf(request):
    user=request.user
    if hasattr(user,'profile')and user.profile.role=='teacher':
        materials=Studymaterial.objects.filter(uploaded_by=user)
    else:
        materials=None
        
    context={ 
            'materials':materials
            }
    
    return render(request,"dashboard.html",context)

## MATERIAL DELETE FROME TEACHER DASHBOARD
def delete_material(request, id):
    print("delete called")
    material=get_object_or_404(Studymaterial, id=id)
    material.delete()
    return redirect('dashboard')
## for text show 
def view_text(request, id):
    
    material=get_object_or_404(Studymaterial,  id=id)
    return render(request, 'view_text.html', {'material': material})
   


@login_required(login_url='login')
def formstu(request):
    print("form page accesseed by :",request.user)
    return render(request,"forms.html")
    
def logint(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile=Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request,"profile not found")
                return redirect('login')
            
            if profile.role=='teacher':
                return redirect('form')
            else:
                return redirect('forms')
        else:
            messages.error(request,'invalid username or password')
    return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect('login')

def signupt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        role=request.POST.get('role')
        Accessbox=request.POST.get('Accessbox')
        
        existing_user=User.objects.filter(username=username).first()
        if existing_user:
            profile=Profile.objects.filter(user=existing_user).first()
            if profile:
                if profile.role!=role:
                    messages.error(request,"this username is already exist")
                    return redirect('signup')
                else:
                    messages.error(request,"username already exist choose another")
                    return redirect('signup')
           
            else:
                messages.error(request,"username exist but profile is missing")
                return redirect('signup')
        
            
        
        if role=='teacher':
            if Accessbox!=SECRET_TEACHER_CODE:
                messages.error(request,"invalid code")
                return redirect('signup')
        
            
            

        user = User.objects.create_user(username=username, email=email, password=password1)
        
        user.is_active= False
        user.save()

        
        if role=='teacher':
            Profile.objects.create(user=user, role='teacher', accessbox=Accessbox)
            messages.success(request, "teacher signup")
        else:
            Profile.objects.create(user=user,role='student')
            messages.success(request, "student signup")
        
        uid= urlsafe_base64_encode(force_bytes(user.pk))
        token= default_token_generator.make_token(user)
        
        verification_link=f"http://127.0.1:8000/verify/{uid}/{token}/",
       
        #send mail to user
        send_mail("verify your email",
           f"click the link to verify your email:\n{verification_link}",
            settings.EMAIL_HOST_USER,
            [email],
        )
        messages.success(request, "signup successfull plz verify your email ")
        return redirect('login')
    return render(request,'signup.html')

def verify_email(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except:
        user= None
    if user and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return HttpResponse(" email verified")
    return HttpResponse("invalid link")

@login_required(login_url='login')
def formupload(request, id=None):
    profile=getattr(request.user,'profile', None)
    if not profile or profile.role!='teacher':
        messages.error(request,"access denied")
        return redirect('login')
    material=None
    if id:
        material=Studymaterial.objects.get(id=id)
    if request.method=="POST":
        materialtype=request.POST.get('materialtype')
        subject=request.POST.get('subject')
        batch=request.POST.get('batch')
        course=request.POST.get('course')
        file=request.FILES.get('file')
        text=request.POST.get('text')
        uploaded_by =request.user
        
        errors = []

        if not materialtype or not subject :
            errors.append("All fields are required")

        # file required only for create, not update
        if not materialtype or not file or not subject:
            errors.append("File and material type required")
        
        

        if errors:
            messages.error(request, errors[0])   # bas ek message show karna
            return redirect('form')




        
        if material:
            material.materialtype=materialtype
            material.subject=subject
            material.batch=batch
            material.course=course
            if file:
                material.file=file
            material.text=text
            material.save()
            messages.success(request,"study material updated successfully!")
        
        else:
            Studymaterial.objects.create(materialtype=materialtype, subject=subject, batch=batch, course=course, file=file, uploaded_by=uploaded_by, text=text)
            messages.success(request, "Study material uploaded successfully! ✅")
            return redirect('form')
        
        return redirect('dashboard')
        
        
    return render(request,'form.html',{'item':material})

def materials(request, type):
    type = type.lower()

    mapping = {
        "assignment": "assignment",
        "notes": "note",
        "other": "other",
        "timetable": "time"
    }

    key = mapping.get(type)

    if not key:
        materials = Studymaterial.objects.none()
    else:
        materials = Studymaterial.objects.filter(
            materialtype__icontains=key
        ).order_by('-uploaded_at')

    return render(request, "materials.html", {"materials": materials, "type": type})


