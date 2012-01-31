from django import forms
from svn_admin.svn_admin_conf import *
svg=SvnGroup('/home/svn/config_file.conf')

class newrepo_form(forms.Form):
    reponame=forms.CharField(label='Repository Name',error_messages={'required':'Enter repository  name'} ,widget=forms.TextInput(attrs={'size':'20'}))
    admin=forms.ComboField(label='Repository Admin',error_messages={'required':'Enter repository admin'})

class new_user_form(forms.Form):
    def __init__(self,grp_list,usr_list,*args,**kwrds):
        super(new_user_form,self).__init__(*args,**kwrds)
        self.fields['username'].choices=usr_list
        self.fields['group_name'].choices=grp_list
        
    
    username=forms.ChoiceField(label='Select user')
    group_name=forms.ChoiceField(label='Select group')
    
class new_group_form(forms.Form):
    
    group_name=forms.CharField(label='Group Name',error_messages={'required':'Enter group name'} ,widget=forms.TextInput(attrs={'size':'20'}))

class set_users_form(forms.Form):
    
    def __init__(self,usr_list,*args,**kwrds):
        super(set_users_form,self).__init__(*args,**kwrds)
        self.fields['username'].choices=usr_list
    username=forms.ChoiceField(label='Select user')
    PER_CHOICES = (
    ('rw', 'rw'),
    ('r', 'r'),)

    user_permission =forms.MultipleChoiceField(choices=PER_CHOICES, widget=forms.CheckboxSelectMultiple())
    
class set_groups_form(forms.Form):
    
    def __init__(self,grp_list,*args,**kwrds):
        super(set_groups_form,self).__init__(*args,**kwrds)
        self.fields['group_name'].choices=grp_list
        
    group_name=forms.ChoiceField(label='Select group')    
    PER_CHOICES = (
    ('rw', 'rw'),
    ('r', 'r'),)

    group_permission =forms.MultipleChoiceField(choices=PER_CHOICES, widget=forms.CheckboxSelectMultiple())

class set_manager_form(forms.Form):
    def __init__(self,usr_list,*args,**kwrds):
        super(set_manager_form,self).__init__(*args,**kwrds)
        self.fields['manager_name'].choices=usr_list
    manager_name=forms.ChoiceField(label='Select Manager')
    

    
    
    
    
    
