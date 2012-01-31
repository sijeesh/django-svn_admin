from django.conf.urls.defaults import patterns, include, url
from svn_manage.views import *

urlpatterns=patterns('',

  url(r'^detailed_view',detailed_view),
  url(r'^repo_deactivate',repo_deactivate),
  url(r'^new_repo',new_repo_direct),
  url(r'^create_repo',create_repo),
  (r'^user_manage',user_manage),
  (r'^create_user',create_user),
  (r'^create_group',create_group),
  (r'^repo_set_members',repo_set_members),
  (r'^set_manager',set_manager),
  (r'^save_repo__user',save_repo__user),
  (r'^save_repo_group',save_repo_group),
  (r'^save_manager',save_manager),
  (r'^delete_user',delete_user),
  (r'^delete_group',delete_group),
  (r'^add_manager',add_manager),
  (r'^delete_manager',delete_manager),
  
  

)
