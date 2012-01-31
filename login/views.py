from django.shortcuts import HttpResponse,HttpResponseRedirect,render_to_response
from login.forms import login_form
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from svn_admin.svn_admin_conf import *
from  svn_manage.models import * 
 
def login_page(request):
   form=login_form()
   return render_to_response('login/login.html',{'form':form},context_instance=RequestContext(request))
   

def login_to(request):
   if request.method=='POST':
      form=login_form(request.POST)
      if form.is_valid():
         user=form.cleaned_data['username']
         username=user
         passw=form.cleaned_data['password']
         user=authenticate(username=user,password=passw)
         
         if user is not None:
            login(request,user)   
            try:
               pro = user.get_profile()
               privillege=pro.privillege
            except:
               privillege=3
               
            return HttpResponseRedirect("/login/home?privillege=%s&username=%s" %(privillege,username))
            
         else:
            return render_to_response('login/login.html',{'form':form,'message':'Check your username or password'},context_instance=RequestContext(request))
      else:
         return render_to_response('login/login.html',{'form':form},context_instance=RequestContext(request))
   else:
         return HttpResponseRedirect('/login/')

def logout(request):
   del request.session['privillege']
   logout(request)
   return HttpResponseRedirect('/login/')

@login_required   
def home(request,*args,**kwargs):
   if request.GET.has_key('privillege'):
      privillege=request.GET.get('privillege')
   elif request.session.has_key('privillege'):
      privillege=request.session['privillege']
   else:
      privillege=3
   
   if request.session.has_key('user_name'):
      username=request.session['user_name']
   else:
      username=request.GET.get('username')
      request.session['user_name']=username
      
   if privillege == '1':   
      sv=SvnRepo('/home/svn/config_file.conf')
      sv_repos=sv.get_all_repo()
      details=[]
      for i in sv_repos:
               admns=sv.get_admins(i)
               user_count=sv.get_total_users(i)
               try:
                  obj=Repos.objects.get(repo_name=i)
                  admin=obj.repo_admin
                  created=obj.created_on
                  manager=obj.repo_manager
                  status=obj.status
               except:
                  admin=''
                  created=''
                  manager=''
                  status=''
                  
               details.append( {'repo':i,'admins':admin,'users':user_count,'date':created,'manager':manager,'status':status} )
      request.session['privillege']=privillege  
      return render_to_response('home.html',{'privillege':privillege,'details':details},context_instance=RequestContext(request))
   elif privillege =='2':
      
      sv=SvnRepo('/home/svn/config_file.conf')
     
      
      all=sv.get_all_repo()
      sv_repos=[]
      
      for repo in all:
            for u in sv.get_repo_users(repo):
                if u[0] == username: 
                   sv_repos.append(repo)

      details=[]
      for i in sv_repos:
               admns=sv.get_admins(i)
               user_count=sv.get_total_users(i)
               try:
                  obj=Repos.objects.get(repo_name=i)
                  admin=obj.repo_admin
                  created=obj.created_on
                  manager=obj.repo_manager
                  status=obj.status
               except:
                  admin=''
                  created=''
                  manager=''
                  status=''
               details.append( {'repo':i,'admins':admin,'users':user_count,'date':created,'manager':manager,'status':status} )
      request.session['privillege']=privillege         
      return render_to_response('home.html',{'privillege':privillege,'details':details},context_instance=RequestContext(request))
   else:
      sv=SvnRepo('/home/svn/config_file.conf')
      sv_repos=sv.get_all_repo()
      details=[]
      all=sv.get_all_repo()
      sv_repos=[]
      for repo in all:
            for u in sv.get_repo_users(repo):
                if u[0] == username: 
                   sv_repos.append((repo,u[1]))
      details=sv_repos
      request.session['privillege']=privillege         
      return render_to_response('home.html',{'privillege':privillege,'details':details},context_instance=RequestContext(request))
      
      
      
   
   
   
   
   
   
   
   
   
      
   
