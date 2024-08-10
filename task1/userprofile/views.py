from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def  regist(request):
    if request.method=='POST':
        data= request.POST
        print(data)
    
        nameUser = data.get('namee')
        email=data.get('emailUser')
        address=data.getlist('addressUser')
        password=data.get('passwordUser')
        sameuser=User.objects.filter(username=nameUser)
        if sameuser:
            messages.info(request, "same user")
        else:
            print(sameuser)
            user =User.objects.create(
                username=nameUser,
                email=email,
                
            )
            
            user.set_password(password)
            user.save()

            deletebutton.objects.create(
                user=user,
                )
            


            for addr in address:
                userprofilee.objects.create(
                user=user,
                addressUser=addr
                )
            for addr in address:
                print(addr)


            messages.info(request, "login done")
            return redirect('loginn')
       
    return render(request,'regist.html')
    
@login_required(login_url='loginn')
def profile(request):

    user = request.user
    print(request.user)
    
   
   

    user_profiles = userprofilee.objects.filter(user=user)
   
         
         
    for profile in user_profiles:
      print(profile.addressUser) 
      context = {
        'user': user,
        'user_profiles': user_profiles,
    }

    return render(request, 'profilee.html', context)
     





def loginn(request):

    if request.method=='POST':
            data= request.POST
            nameUser = data.get('namee')
            
            passw=data.get('passwordUser')
            
            user = authenticate(username=nameUser,password=passw)

            if user is None:
                  messages.info(request, "password or username is incorrect")
                  
                  return redirect('loginn')
              
            else:
                try:
                    user_profile = deletebutton.objects.get(user=user)
                    
                    if user_profile.deleteq:
                        messages.info(request, " deactivated")
                       
                        return redirect('loginn')  
                        
                except deletebutton.DoesNotExist:
                    messages.error(request, "User profile not found.")
                  
                    return redirect('loginn')
                   


               
    
        
                login(request,user)
                messages.info(request, "login sussesful")

                return redirect('profile')
            

                 


    return render(request,'login.html')



@login_required(login_url='loginn')
def deletereq(request,id):
    deel = User.objects.get(id=id)
    userdel = deletebutton.objects.get(user=deel)
    userdel.deleteq = True
    
    
    userdel.save()
    print(userdel)
    return redirect('loginn')


def log_out(request):
    logout(request)
    return redirect('loginn')

