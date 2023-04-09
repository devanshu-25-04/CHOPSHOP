import os
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CustomerRegistration
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from .models import customer,employee
import random, uuid
import smtplib
import pickle
from .models import employee, appointment, shopapointment
from django.contrib.auth.models import User

def home(request):
    context={'name':'Devasnhu', 'course':'Django'}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def about2(request):
    return render(request, 'about2.html')

def project(request):
    return render(request, 'project.html')

def project2(request):
    return render(request, 'project2.html')

def contact(request):
    if(request.method=='POST'):
        print(request.GET)
        result=request.POST
        name=result.get("Name",'null')
        print(name)
        email=result.get("Email")
        msg=result.get("Message",'null')
        print(email)  
        if contact_mail(name,email,msg):
            messages.success(request, 'your query was successfully sent')
        return render(request, 'contact.html')
    return render(request, 'contact.html')

def contact_mail(name,email,msg):
    msg = f'Hi {name}, thank you for contacting us. We will reply to your query "{msg}" shortly.'
    send_mail(email, msg)
    print('EMAIL SENT')
    return True

def send_mail(id,msg):
    print(id)
    from_id='redrondoofdeath@gmail.com'
    conn =smtplib.SMTP('smtp.gmail.com',587)  
    type(conn)  
    conn.ehlo()  
    conn.starttls()  
    message = MIMEMultipart("alternative")
    message["Subject"] = "Thank You for contacting chopshop"
    message["From"] = from_id
    message["To"] = id
    text=msg
    msg = MIMEText(text, "plain")
    message.attach(msg)
    conn.login(from_id,'bapeockmyuxkvnnq')  
    conn.sendmail(from_id,id,message.as_string())  
    conn.quit()

class signup(View):
    def get(self,request):
        form = CustomerRegistration()
        return render(request,'signup.html',{'form':form})
    def post(self,request):
        form = CustomerRegistration(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations!! registered successfully')
            form.save()
        return render(request,'signup.html',{'form':form}) 

def login(request):
    return render(request,'login.html')

def home2(request):
    return render(request,'home2.html')

def EmployerReg(request):
    if request.method == "POST":
        print(request.POST)
        user = request.user
        name = request.POST.get("name")
        address = request.POST.get("address")
        services = request.POST.getlist("services[]")
        print(services)
        email=request.POST.get("email")
        haircutting =False
        styling = False
        threading = False
        waxing = False
        manicure = False
        pedicure = False
        rates=request.POST.get("rates")
        image = request.POST.get("picture")
        print(image)
        empService = ""
        for service in services:
            print(service)
            empService += service + ","
            if service == "haircutting":
                haircutting=True
            if service == "styling":
                styling=True
            if service == "threading":
                threading=True
            if service == "waxing":
                waxing=True
            if service == "manicure":
                manicure=True
            if service == "pedicure":
                pedicure=True
        print(haircutting, styling, threading, 
                waxing, manicure, pedicure)
        msg1="user added successfully !!"
        # Check if employee already exists for the user
        if not employee.objects.filter(user=user).exists():
        
            emp1 = employee.objects.create(user=user, name=name, address=address, services=empService,
                haircutting=haircutting, styling=styling, threading=threading, 
                waxing=waxing, manicure=manicure, pedicure=pedicure,rates=rates, image=image)
            emp1.save()
            print (emp1.name)
        else:
            msg1="user already exists!!"  
        print(id)
        msg = f'Hi {name}, thank you for contacting us. Your Salon was added to the site.'
        from_id='redrondoofdeath@gmail.com'
        conn =smtplib.SMTP('smtp.gmail.com',587)  
        type(conn)  
        conn.ehlo()  
        conn.starttls()  
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{name} has been successfully added to the site!"
        message["From"] = from_id
        message["To"] = email
        text=msg
        msg = MIMEText(text, "plain")
        message.attach(msg)
        conn.login(from_id,'bapeockmyuxkvnnq')  
        conn.sendmail(from_id,email,message.as_string())  
        conn.quit()
        messages.success(request, msg1)
        return render(request, 'EmployerReg.html')
    return render(request, 'EmployerReg.html')

def employee_list(request):
    employees = employee.objects.all()
    context = {'employees': employees}
    return render(request, 'employee_list.html', context)

def shopmenu(request):
    if request.method== "POST":
        print(request)
        user=request.user
        employee1_name=request.POST.get("employee")
        employee1=employee.objects.filter(name=employee1_name).first()
        print(employee1)
        time=request.POST.get("time","null")
        services=request.POST.get("services","null")
        
        shopappoint=shopapointment.objects.filter(user=user).first()
       
        shopappoint=shopapointment.objects.create(user=user,employee=employee1, time=time, services=services)
        shopappoint.save()
        shopapointment1={"shopapointment":shopapointment}
        print(shopappoint)
        return render(request,'confirmationpage.html',shopapointment1)
               
    employee_list=employee.objects.all() 
    employee_list_new = []
    for emp in employee_list:
        rates = emp.rates.split("\r")
        emp_dict = {
            "id": emp.id,
            "name": emp.name,
            "address": emp.address,
            "services": emp.services,
            "haircutting": emp.haircutting,
            "styling": emp.styling,
            "threading": emp.threading,
            "waxing": emp.waxing,
            "manicure": emp.manicure,
            "pedicure": emp.pedicure,
            "rates": rates,
            "image": emp.image
        }
        employee_list_new.append(emp_dict)
        print(emp_dict["rates"])
        
    employee_list = {
        "emps":employee_list_new
    }
    if request.user.is_authenticated:
        user = request.user
        name = request.user.username
        email = request.user.email
        msg1="Successful" 
        print(id)
        msg = f'Hi {name}, Your Booking has been Confirmed'
        from_id='redrondoofdeath@gmail.com'
        conn =smtplib.SMTP('smtp.gmail.com',587)  
        type(conn)  
        conn.ehlo()  
        conn.starttls()  
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Confirmation of Booking"
        message["From"] = from_id
        message["To"] = email
        text=msg
        msg = MIMEText(text, "plain")
        message.attach(msg)
        conn.login(from_id,'bapeockmyuxkvnnq')  
        conn.sendmail(from_id,email,message.as_string())  
        conn.quit()
        messages.success(request, msg1)
    return render(request,'shopmenu.html',employee_list)

def confirmationpage(request):
    return render(request,'confirmationpage.html')

def appointmentcheck(request):
    return render(request,'appointmentcheck.html')

def drappoint(request):
    if request.method=="POST":
        user=request.user
        time=request.POST.get("time")
        email=request.POST.get("email")
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        
        appoint=appointment.objects.filter(user=user).first()
        if not appoint:
            appoint=appointment.objects.create(user=user, time=time, email=email,name=name,phone=phone)
            print(appointment)
        else:
            appoint.time = time
            appoint.email = email
            appoint.name = name
            appoint.phone = phone
            appoint.save()
            print(appoint) 
        if send_mail_drappoint(name,email):
            messages.success(request, 'your appointment request was successfully sent')
        return render(request, 'drappoint.html')
    return render(request,'drappoint.html')

def send_mail_drappoint(name,id):
    print(id)
    msg = f'Hi {name}, thank you for contacting us. Your Booking was confirmed.'
    from_id='redrondoofdeath@gmail.com'
    conn =smtplib.SMTP('smtp.gmail.com',587)  
    type(conn)  
    conn.ehlo()  
    conn.starttls()  
    message = MIMEMultipart("alternative")
    message["Subject"] = "Doctor Appointment confirmed"
    message["From"] = from_id
    message["To"] = id
    text=msg
    msg = MIMEText(text, "plain")
    message.attach(msg)
    conn.login(from_id,'bapeockmyuxkvnnq')  
    conn.sendmail(from_id,id,message.as_string())  
    conn.quit()
    return True

def getPredictionsHairloss(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12):
    module_dir = os.path.dirname(__file__)  
    
    model1 = pickle.load(open(os.path.join(module_dir,"savedModels",'Hairloss.pkl'),'rb'))
    model2 = pickle.load(open(os.path.join(module_dir,"savedModels",'GreyHair.pkl'),'rb'))
    model3 = pickle.load(open(os.path.join(module_dir,"savedModels",'Dandruff.pkl'),'rb'))
    
    predictHairloss=model1.predict([[c1,c2,c3,c4]])
    predictGreyHair=model2.predict([[c5,c6,c7,c8,c9]])
    predictDandruff=model3.predict([[c10,c11,c12]])
    if(predictDandruff==0 and predictGreyHair ==0 and predictHairloss==0):
        return 0
    elif(predictDandruff==0 and predictGreyHair ==0 and predictHairloss==1):
        return 1
    elif(predictDandruff==0 and predictGreyHair ==1 and predictHairloss==0):
        return 2
    elif(predictDandruff==0 and predictGreyHair ==1 and predictHairloss==1):
        return 3
    elif(predictDandruff==1 and predictGreyHair ==0 and predictHairloss==0):
        return 4
    elif(predictDandruff==1 and predictGreyHair ==0 and predictHairloss==1):
        return 5
    elif(predictDandruff==1 and predictGreyHair ==1 and predictHairloss==0):
        return 6
    else:
        return 7
   
def product(request):
    if request.method == "POST":
        print("enetrinh post ...")
        hl1=request.POST.get('q1',"no")
        hl2=request.POST.get('q2',"no")
        hl3=request.POST.get('q3',"no")
        hl4=request.POST.get('q4',"no")
        gh5=request.POST.get('q5',"no")
        gh6=request.POST.get('q6',"no")
        gh7=request.POST.get('q7',"no")
        gh8=request.POST.get('q8',"no")
        gh9=request.POST.get('q9',"no")
        df10=request.POST.get('q10',"no")
        df11=request.POST.get('q11',"no")
        df12=request.POST.get('q12',"no")
        c1=0
        c2=0
        c3=0
        c4=0
        c5=0
        c6=0
        c7=0
        c8=0
        c9=0
        c10=0
        c11=0
        c12=0
        if hl1 == "yes":
            c1=1
        else:
            c1=0
        if hl2 == "yes":
            c2=1
        else:
            c2=0
        if hl3 == "yes":
            c3=1
        else:
            c3=0
        if hl4 == "yes":
            c4=1
        else:
            c4=0
        if gh5 == "yes":
            c5=1
        else:
            c5=0
        if gh6 == "yes":
            c6=1
        else:
            c6=0
        if gh7 == "yes":
            c7=1
        else:
            c7=0
        if gh8 == "yes":
            c8=1
        else:
            c8=0
        if gh9 == "yes":
            c9=1
        else:
            c9=0
        if df10 == "yes":
            c10=1
        else:
            c10=0
        if df11 == "yes":
            c11=1
        else:
            c11=0
        if df12 == "yes":
            c12=1
        else:
            c12=0
        print(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12)
        res = getPredictionsHairloss(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12)
        print(res)
        
        if res==0:
            return render(request,'noprobs.html')
        if res==1:
            return render(request,'hairloss.html')
        if res==2:
            return render(request,'greyhair.html')
        if res==3:
            return render(request,'fallgrey.html')
        if res==4:
            return render(request,'dandruff.html')
        if res==5:
            return render(request,'dandruffall.html')
        if res==6:
            return render(request,'greydand.html')
        if res==7:
            return render(request,'allthree.html')        
    return render(request,'product.html')