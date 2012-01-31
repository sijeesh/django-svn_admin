try:
	import ConfigParser
except:
	import configparser as ConfigParser



class SvnRepo:
   
	def __init__(self,filename):
	       self.cfgfile=filename
               self.config=ConfigParser.ConfigParser()
               self.config.read(self.cfgfile)  
	def create_repo(self,repo_name,admin_name):
		
		if not self.config.sections():
		        self.config.add_section('groups')
			if not self.config.has_section('/'):
				self.config.add_section('/')
				self.config.set('/','*','r')
				self.config.set('/','@admin','rw')
			with open(self.cfgfile,'w') as configfile:
			    self.config.write(configfile)
			
                if self.config.has_section(repo_name):
                	#raise Exception, "Duplicate repository name"
			return 0 

                else: 
                    try: 
			self.config.add_section(repo_name+':/')
                        self.config.set(repo_name+':/','@'+admin_name,'rw')
			
                        with open(self.cfgfile,'w') as configfile:
			    self.config.write(configfile)
                        return 1
                    except :
                        return 0 

        def remove_repo(self,repo_name):
                try:
			self.config.remove_section(repo_name+':/')
			with open(self.cfgfile,'w') as configfile:
				self.config.write(configfile)
			return 1
		except:
			return 0

        def get_all_repo(self):
                repo_list=[]
                for repo in self.config.sections():
			if repo != 'groups' and repo !='/':
				repo_list.append(repo[:-2])
		return repo_list

        def add_repo_group(self,repo_name,group_name,per):
                 
                if self.config.has_option(repo_name,'@'+group_name):
                            raise Exception ," Duplicate group"
                else:
                    try:
	                self.config.set(repo_name+':/','@'+group_name,per)
                        with open(self.cfgfile,'w') as configfile:
                            self.config.write(configfile)
                        return 1
                    except:
        	        return 0

        def delete_repo_group(self,repo_name,group_name):
                
                for option in self.config.options(repo_name+':/'):
                          if option == '@'+group_name:
                              try:
	                              self.config.remove_option(repo_name+':/',option)
                                      with open(self.cfgfile,'w') as configfile:
                            			self.config.write(configfile)
                             	      return 1
                              except:
                                      return 0
        def get_repo_groups(self,repo_name):
                
                repo_groups=[]
                for group in self.config.options(repo_name+':/'):
                    if '@'  in group:
			permission=self.config.get(repo_name+':/',group)
                        repo_groups.append((group[1:],permission))
                return repo_groups


        def add_repo_user(self,repo_name,username,per):

                if self.config.has_option(repo_name,username):
                            raise Exception ," Duplicate user name"
                else:
                    try:
                        self.config.set(repo_name+':/',username,per)
                        with open(self.cfgfile,'w') as configfile:
                            self.config.write(configfile)
                        return 1
                    except:
                        return 0

        
	def delete_repo_user(self,repo_name,username):
                
                for option in self.config.options(repo_name+':/'):
                          if option == username:
                              try:
                                      self.config.remove_option(repo_name+':/',option)
                                      with open(self.cfgfile,'w') as configfile:
                                                self.config.write(configfile)
                                      return 1
                              except:
                                      return 0


        def get_repo_users(self,repo_name):
                
		repo_users=[]
                for user in self.config.options(repo_name+':/'):
                    if '@' not in user:
			permission=self.config.get(repo_name+':/',user)
                        repo_users.append((user,permission))
                return repo_users
	
        def get_group_permission(self,repo_name,group_name):
		try:
			if repo_name != 'groups':
				return self.config.get(repo_name+':/','@'+group_name)

		except:
			return 0
			
	
        def get_user_permission(self,repo_name,username):
		try:
			if repo_name != 'groups':
				return self.config.get(repo_name+':/',username)
			
		except:
			return 0
	def get_admins(self,repo_name):
		mmbr_list=self.config.options(repo_name+':/')
		admin_list=[]
		for m in mmbr_list:
			if self.config.get(repo_name+':/',m) == 'rw':
				if '@' in m :
					m=m[1:]+'(group)'
				admin_list.append(m)
				
		return admin_list
	def get_total_users(self,repo_name):
		user_count=0
		group_count=0
		total=0
		for user in self.config.options(repo_name+':/'):
			if '@' in user :
				group_count=group_count+1
				try:
					gr_list=(self.config.get('groups',user[1:])).split(',')
					total=total+len(gr_list)
				except:
					total=total+1
				
				
			else:
			        user_count=user_count+1
				total=total+1
				
		repo_users={'users':user_count,'groups':group_count,'total':total}
		return repo_users
				
		
		        
class SvnGroup:
        
	def __init__(self,filename):
               self.cfgfile=filename
               self.config=ConfigParser.ConfigParser()
               self.config.read(self.cfgfile)
	       
        def add_group(self,group_name):
              try:
              		if not self.config.has_section('groups'):
                      		self.config.add_section('groups')
                        if group_name in self.config.options('groups'):
				raise Exception ," Duplicate group name"
              		self.config.set('groups',group_name,None)
              		with open(self.cfgfile,'w') as configfile:
	                            self.config.write(configfile)
                           
                	return 1
              except:
                	return 0
   
                    
        def delete_group(self,group_name):
                                             
             try:
                    self.config.remove_option('groups',group_name)
                    with open(self.cfgfile,'w') as configfile:
                        self.config.write(configfile)
                        return 1
             except:
                    return 0
		
	def get_all_groups(self):
		  
		group_list=[]  
		for option in self.config.options('groups'):
			group_list.append(option)
		return group_list
	def get_group_members(self,group_name):
		
		return (self.config.get('groups',group_name)).split(',')
	
        def set_group_member(self,member_name,group_name):
		
		if self.config.has_option('groups',group_name):
			members=self.config.get('groups',group_name)
			if not self.config.get('groups',group_name):
				members=member_name
			else:
				if members == 'None':
					members=member_name
				else:
				        members=members+','+member_name
				
			self.config.set('groups',group_name,members)
			with open(self.cfgfile,'w') as configfile:
				self.config.write(configfile)
                        return 1
		else:
			return 0
		
	def delete_group_member(self,group_name,member_name):
		
		members=self.config.get('groups',group_name)
		member_list=members.split(',')
		group_members=''
		for mmbr in member_list:
			if mmbr != member_name:
				group_members=group_members+','+mmbr
		self.config.set('groups',group_name,group_members[1:])
		with open(self.cfgfile,'w') as configfile:
				self.config.write(configfile)
                return 1
	
		
		
		
		

              
          
               
                            

                 

        

		
                      

              
              
              
		
            
                


 
