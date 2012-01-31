from django.shortcuts import HttpResponse,HttpResponseRedirect,render_to_response
from svn_admin.svn_admin_conf import *
from django.template import RequestContext
from svn_manage.forms import *
import ldap
import datetime
from svn_manage.models import *
import simplejson as json


def detailed_view(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    
    repo=request.POST['repo_name']
    groups=sv.get_repo_groups(repo)
    users=sv.get_repo_users(repo)
    admins=sv.get_admins(repo)
    user_count=sv.get_total_users(repo)
    try:
        repo_obj=Repos.objects.get(repo_name=repo)
    except:
        repo_obj=''
    try:
        usrs_list=[]
        de=Deactivated.objects.get(repo_name=repo)
        jsonDec = json.decoder.JSONDecoder()
        de_users=jsonDec.decode(de.users)
        de_groups=jsonDec.decode(de.groups)
        de_on=de.deactiveted_on
    except:
        de_users=''
        de_groups=''
        de_on=''
    
    return render_to_response('svn_manage/detailed_view.html',{'de_on':de_on,'de_groups':de_groups,'de_users':de_users,'repo':repo,'groups':groups,'users':users,'admins':admins,'repo_obj':repo_obj,'user_count':user_count},context_instance=RequestContext(request))

def repo_deactivate(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    repo=request.POST['repo_name']
    if request.POST['activate'] == 'Activate':
        #try:
            try:       
                repo_obj=Repos.objects.get(repo_name=repo)
            except:
                now = datetime.datetime.now()
                repo_obj=Repos(repo_name=repo,created_on=now)
                
            repo_obj.status=1
            repo_obj.save()
            try:
                obj=Deactivated.objects.get(repo_name=repo)
                jsonDec = json.decoder.JSONDecoder()
                users=jsonDec.decode(obj.users)
                groups=jsonDec.decode(obj.groups)
                print users
                for u in users:
                    print repo
                    print u
                    sv.add_repo_user(repo,u[0],u[1])
                
                for g in groups:
                    sv.add_repo_group(repo,g[0],g[1])
            
                Deactivated.objects.filter(repo_name=repo).delete()
            except:
                de_save=Deactivated(repo_name=repo,deactiveted_on=datetime.datetime.now())
                de_save.save()
            
            
        #except:
            #pass
    else:
        #try:
            repo_obj=Repos.objects.get(repo_name=repo)
            repo_obj.status=0
            repo_obj.save()
            repo_users=json.dumps(sv.get_repo_users(repo))
            repo_groups=json.dumps(sv.get_repo_groups(repo))
            for u in sv.get_repo_users(repo):
                    sv.delete_repo_user(repo,u[0])
            for g in sv.get_repo_groups(repo):
                sv.delete_repo_group(repo,g[0])

            
            try:
                Deactivated.objects.get(repo_name=repo)
            except:
                save_deactivated_repo=Deactivated(repo_name=repo,users=repo_users,groups=repo_groups,deactiveted_on=datetime.datetime.now())
                save_deactivated_repo.save()
        #except:
            #pass
        
    return HttpResponseRedirect('/login/home')
    
def new_repo_direct(request):
    form=newrepo_form()
    return render_to_response('svn_manage/new_repo.html',{'form':form},context_instance=RequestContext(request))
    
def create_repo(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    
    if request.method =='POST':
        form=newrepo_form(request.POST)
        if form.is_valid():
            repo_name=form.cleaned_data['reponame']
            admin=form.cleaned_data['admin']
            if sv.create_repo(repo_name,admin):
                now = datetime.datetime.now()
                repo_save=Repos(repo_name=repo_name,repo_admin=admin,created_on=now,status=1)
                repo_save.save()
            return HttpResponseRedirect('/login/home')
        else:
            return render_to_response('svn_manage/new_repo.html',{'form':form},context_instance=RequestContext(request))
    else:
        form=newrepo_form()
        return render_to_response('svn_manage/new_repo.html',{'form':form,'message':'Error.....'},context_instance=RequestContext(request))

def user_manage(request,*args,**kwargs):
  
   sv=SvnRepo('/home/svn/config_file.conf')
   svg=SvnGroup('/home/svn/config_file.conf')
   
   grp_list=svg. get_all_groups()
   gr_mmbr=[]
   
   for gr in grp_list:
    
        gr_repos=[]
        gr_members=svg.get_group_members(gr)
        
        for repo in sv.get_all_repo():
            repo_grps=sv.get_repo_groups(repo)
            
            for grs in repo_grps:
                if gr == grs[0]:
                    gr_repos.append(repo)
                
        gr_mmbr.append( { 'group':gr,'group_members':gr_members,'group_repos':gr_repos })
   
   group=svg.get_all_groups()
   grp_list=[]
   grp_list.append(('Select','Select'))
   for g in group:
        grp_list.append((g,g))
   
   ld=get_users_ldap()
   usr_list=[]
   usr_list.append(('Select','Select'))
   for usr in ld:
       usr_list.append((usr,usr))
   
   
   mng_list=[]
   m=Managers.objects.all()
   for usr in m:
            mng_list.append((usr.name,usr.name))
            
   form1=new_user_form(grp_list,usr_list)
   form2=new_group_form()
   form3=set_manager_form(usr_list)
   form4=set_manager_form(mng_list)
   
   man=Managers.objects.all()
   manager_list=[]
   all=sv.get_all_repo()
   for m in man:
        manager_repos=[]
        for repo in all:
            for u in sv.get_repo_users(repo):
                if u[0] == m.name: 
                   manager_repos.append(repo)
        manager_list.append((m,manager_repos))
            
   
   privillege=request.session['privillege']
   if request.GET.has_key('message'):
        message=request.GET.get('message')
        return render_to_response('svn_manage/user_manage.html',{'gr_mmbr':sorted(gr_mmbr),'form1':form1,'form2':form2,'form3':form3,'form4':form4,'message':message,'manager_list':manager_list,'privillege':privillege},context_instance=RequestContext(request))
   elif request.GET.has_key('message1') :
        message1=request.GET.get('message1')
        return render_to_response('svn_manage/user_manage.html',{'gr_mmbr':sorted(gr_mmbr),'form1':form1,'form2':form2,'form3':form3,'form4':form4,'message1':message1,'manager_list':manager_list,'privillege':privillege},context_instance=RequestContext(request))
   else:
        return render_to_response('svn_manage/user_manage.html',{'gr_mmbr':sorted(gr_mmbr),'form1':form1,'form2':form2,'form3':form3,'form4':form4,'manager_list':manager_list,'privillege':privillege},context_instance=RequestContext(request))

def create_user(request):
    svg=SvnGroup('/home/svn/config_file.conf')
    if request.method == 'POST':
        group=svg.get_all_groups()
        grp_list=[]
        grp_list.append(('Select','Select'))
        for g in group:
          grp_list.append((g,g))
   
        ld=get_users_ldap()
        usr_list=[]
        usr_list.append(('Select','Select'))
        for usr in ld:
            usr_list.append((usr,usr))
        form=new_user_form(grp_list,usr_list,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            group_name=form.cleaned_data['group_name']
            if username == 'Select' or group_name == 'Select':
                message='Select username and groupname'
            else:
                if svg.set_group_member(username,group_name):
                    message='User added successfully..'
                else:
                    message='Please check username or group name'
            
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
        else:
            message='Form error:Please fill both username and group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
    else:
        return HttpResponseRedirect("/svn_manage/user_manage")

def delete_user(request):
    svg=SvnGroup('/home/svn/config_file.conf')
    if request.method == 'POST':
        group=svg.get_all_groups()
        grp_list=[]
        grp_list.append(('Select','Select'))
        for g in group:
          grp_list.append((g,g))
   
        ld=get_users_ldap()
        usr_list=[]
        usr_list.append(('Select','Select'))
        for usr in ld:
            usr_list.append((usr,usr))
        form=new_user_form(grp_list,usr_list,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            group_name=form.cleaned_data['group_name']
            if username == 'Select' or group_name == 'Select':
                message='Select username and groupname'
            else:
                if svg.delete_group_member(group_name,username):
                    message='User deleted successfully..'
                else:
                    message='Please check username or group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
        else:
            message='Form error:Please select both username and group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
    else:
        return HttpResponseRedirect("/svn_manage/user_manage")


def create_group(request):
    svg=SvnGroup('/home/svn/config_file.conf')
    
    if request.method == 'POST':

        form=new_group_form(request.POST)
        
        if form.is_valid():
            group_name=form.cleaned_data['group_name']
            if svg.add_group(group_name):
                message1='group added successfully..'
            else:
                message1='Please check group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message1="+str(message1))
        else:
            message1='Please fill group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message1="+str(message1))
    else:
        return HttpResponseRedirect("/svn_manage/user_manage")
def delete_group(request):
    svg=SvnGroup('/home/svn/config_file.conf')
    
    if request.method == 'POST':

        form=new_group_form(request.POST)
        
        if form.is_valid():
            group_name=form.cleaned_data['group_name']
            if svg.delete_group(group_name):
                message='group deleted successfully..'
            else:
                message='Please check group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
        else:
            message='Please fill group name'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
    else:
        return HttpResponseRedirect("/svn_manage/user_manage")



def get_users_ldap():

    con = ldap.initialize("ldap://10.0.0.201")
    con.simple_bind("ou=people,dc=telibrahma,dc=com")
    res = con.search_s("ou=people,dc=telibrahma,dc=com", ldap.SCOPE_SUBTREE,'uid=*')
    con.unbind()
    result_set = []
    for i in res:
                      i=i[1]['uid'][0]  
                      result_set.append(i)
    return result_set

def repo_set_members(request,*args,**kwargs):
    svg=SvnGroup('/home/svn/config_file.conf')
    
    if request.GET.has_key('repo'):
        repo=request.GET.get('repo')
    else:    
        repo=request.POST['repo_name']

    group=svg.get_all_groups()
    grp_list=[]
    grp_list.append(('Select','Select'))
    for g in group:
          grp_list.append((g,g))
   
    ld=get_users_ldap()
    usr_list=[]
    usr_list.append(('Select','Select'))
    for usr in ld:
            usr_list.append((usr,usr))
    form=set_users_form(usr_list)
    form1=set_groups_form(grp_list)
    if request.GET.has_key('message'):
        message=request.GET.get('message')
    else:
        message=''
    
    return render_to_response('svn_manage/set_members.html',{'form':form,'form1':form1,'repo':repo,'message':message},context_instance=RequestContext(request))

def save_repo__user(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    
    repo=request.POST['repo']
    if request.method == 'POST':
        ld=get_users_ldap()
        usr_list=[]
        usr_list.append(('Select','Select'))
        for usr in ld:
            usr_list.append((usr,usr))
        
        form=set_users_form(usr_list,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            permission=form.cleaned_data['user_permission']
            try:
                repo_obj=Repos.objects.get(repo_name=repo)
                repo_managers=(repo_obj.repo_manager).split(',')
                if username in repo_managers:
                   message="This user already added as manager..."
            except:
                message=''
            
            
            if 'r' in permission:
                    permission='r'
            else:
                    permission='rw'
                    
            if sv.add_repo_user(repo,username,permission):
                     message='Saved successfully...'
            else:
                    message='Some Error...'
            return HttpResponseRedirect('/svn_manage/repo_set_members?message=%s&repo=%s' %(message,repo))
        else:
            pass
def save_repo_group(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    svg=SvnGroup('/home/svn/config_file.conf')
    
    repo=request.POST['repo']
    if request.method == 'POST':
        group=svg.get_all_groups()
        grp_list=[]
        grp_list.append(('Select','Select'))
        for g in group:
          grp_list.append((g,g))
        
        form=set_groups_form(grp_list,request.POST)
        if form.is_valid():
            grp_name=form.cleaned_data['group_name']
            permission=form.cleaned_data['group_permission']
            if 'r' in permission:
                permission='r'
            else:
                permission='rw'
                
            if sv.add_repo_group(repo,grp_name,permission):
                 message='Saved successfully...'
            else:
                message='Some Error...'
            return HttpResponseRedirect('/svn_manage/repo_set_members?message=%s&repo=%s' %(message,repo))
        else:
            pass
def save_manager(request):
    sv=SvnRepo('/home/svn/config_file.conf')
    
    repo=request.POST['repo']
    if request.method == 'POST':
        ld=get_users_ldap()
        usr_list=[]
        for usr in ld:
            usr_list.append((usr,usr))
        
        form=set_manager_form(usr_list,request.POST)
        if form.is_valid():
            manager=form.cleaned_data['manager_name']
            repo_m=Repos.objects.get(repo_name=repo)
            if repo_m.repo_manager == '' or repo_m.repo_manager == None:
                repo_m.repo_manager=manager
            else:
                repo_m.repo_manager=repo_m.repo_manager+','+manager
            repo_m.save()
            sv.add_repo_user(repo,manager,'rw')
            return HttpResponseRedirect('/login/home?privillege=%s'%(1))
        else:
            return HttpResponseRedirect('/login/home')
        
def add_manager(request):
     if request.method == 'POST':
        ld=get_users_ldap()
        usr_list=[]
        for usr in ld:
            usr_list.append((usr,usr))
        
        form=set_manager_form(usr_list,request.POST)
        if form.is_valid():
            manager=form.cleaned_data['manager_name']
            save_manager=Managers(name=manager)
            save_manager.save()
            message='Manager added successfully'
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
        else:
          return HttpResponseRedirect("/svn_manage/user_manage")

def delete_manager(request):
    if request.method == 'POST':
        usr_list=[]
        m=Managers.objects.all()
        for usr in m:
            usr_list.append((usr.name,usr.name))
        
        form=set_manager_form(usr_list,request.POST)
        if form.is_valid():
            manager=form.cleaned_data['manager_name']
            try:
                save_manager=Managers.objects.filter(name=manager).delete()
                message='Manager deleted successfully'
            except:
                message='Some problem..'    
            
            return HttpResponseRedirect("/svn_manage/user_manage?message="+str(message))
        else:
          return HttpResponseRedirect("/svn_manage/user_manage")
    

def set_manager(request):
    repo=request.POST['repo_name']
    usr_list=[]
    m=Managers.objects.all()
    for usr in m:
            usr_list.append((usr.name,usr.name))
    form=set_manager_form(usr_list)
    form=set_manager_form(usr_list)
    return render_to_response('svn_manage/set_manager.html',{'form':form,'repo':repo},context_instance=RequestContext(request))
    
    
    