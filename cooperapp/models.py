from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class UserProfile(models.Model):

	USER_ROLE =(
		('co-operative', 'CO-OPERATIVE'),
		('ajo', 'AJO'),
		('none', 'NONE'),
		)

	USER_STATUS =(
		('not verified', 'NOT VERIFIED'),
		('pending verification', 'PENDING VERIFICIATION'),
		('verified', 'VERIFIED'),
		)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=2000,default='')
	description = models.CharField(max_length=2000,default='')
	city = models.CharField(max_length=100,default='')
	address = models.CharField(max_length=500,default='',blank=True)
	phone_number =  models.CharField(max_length=16,default='')
	image = models.ImageField(upload_to='profile_image',blank=True)
	membership_fee = models.PositiveIntegerField(blank=True,null=True)
	user_role = models.CharField(max_length=30,choices=USER_ROLE,default='none')
	user_status = models.CharField(max_length=30,choices=USER_STATUS, default='not verified')
 
	def __str__(self):
		return self.user.username


	class Meta:
		verbose_name = 'Profile'



class ProjectProfile(models.Model):

		PROJECT_CONTRIBUTION =(
									('weekly', 'WEEKLY'),
									('monthly', 'MONTHLY'),
								
								)

		PROJECT_DISTRIBUTION =(
									('ascending', 'ASCENDING'),
									('descending', 'DESCENDING'),
									('random', 'RANDOM'),
								
								)
		user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
		project_name = models.CharField(max_length=5000)
		project_description = models.CharField(max_length=200)
		project_contribution = models.CharField(max_length=30,choices=PROJECT_CONTRIBUTION, default='weekly')
		project_distribution = models.CharField(max_length=30,choices=PROJECT_DISTRIBUTION, default='ascending')
		project_duration = models.CharField(max_length=500)
		contribution_amount = models.PositiveIntegerField(blank=True,null=True)
		start_date = models.DateField(auto_now=False, auto_now_add=False, )
		end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
		project_returns = models.PositiveIntegerField(blank=True,null=True)


		def __str__(self):
			return "%s " %(self. user)	


class ProjectContributors(models.Model):

		user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
		project_name = models.ForeignKey(ProjectProfile,on_delete=models.CASCADE,default=1)
		

		def __str__(self):
			return "%s " %(self.project_name)	


class Contributions(models.Model):

		user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
		project_name = models.ForeignKey(ProjectProfile,on_delete=models.CASCADE,default=1)
		amount = models.PositiveIntegerField(blank=True,null=True)
		week_num = models.PositiveIntegerField(blank=True,null=True)
		date = models.DateField(auto_now=False, auto_now_add=False, null=True)


		def __str__(self):
			return "%s " %(self.project_name)	


class CooperativeProjectProfile(models.Model):

		user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
		project_name = models.CharField(max_length=5000)
		project_description = models.CharField(max_length=5000)
		project_type = models.CharField(max_length=200, blank=True,null=True,default="")
		project_duration = models.CharField(max_length=500,default="")
		start_date = models.DateField(auto_now=False, auto_now_add=False, )
		end_date = models.DateField(auto_now=False, auto_now_add=False, null=True,)
		project_returns = models.PositiveIntegerField(blank=True,null=True,default=0)
		project_unitblock_available = models.PositiveIntegerField(blank=True,null=True)
		project_cost_perunitblock = models.PositiveIntegerField(blank=True,null=True, default=0)
		
		def __str__(self):
			return "%s " %(self. user)	


class CooperativeProjectContributors(models.Model):
	STATUS =(
		('active', 'ACTIVE'),
		('requesting out', 'REQUESTING OUT'),
		('disabled', 'DISABLED'),
		)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	cooperative_name = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default=1)
	status = models.CharField(max_length=30,choices=STATUS, default='disabled')
	
		

	def __str__(self):
		return "%s " %(self.project_name)	



class CooperativeContributions(models.Model):

		user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
		cooperative_name = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default=1)
		amount = models.PositiveIntegerField(blank=True,null=True)
		total_amount = models.PositiveIntegerField(blank=True,null=True)
		date = models.DateField(auto_now=True)


		def __str__(self):
			return "%s " %(self.project_name)	


class CooperativeInvestment(models.Model):
	STATUS =(
		('active', 'ACTIVE'),
		('not active', 'NOT ACTIVE')
		
		)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	cooperative_name = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default=1)
	investment_name = models.ForeignKey(CooperativeProjectProfile,on_delete=models.CASCADE,default=1)
	unitblock_purchased = models.PositiveIntegerField(blank=True,null=True)
	status = models.CharField(max_length=30,choices=STATUS, default='not active')
		

	def __str__(self):
		return "%s " %(self.project_name)	

class RequestAjoAdminverification(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	date = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True )

	def __str__(self):
		return "%s " %(self. user)


class RequestCopAdminverification(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	date = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True )

	def __str__(self):
		return "%s " %(self. user)	

class CopInvite(models.Model):
	STATUS =(
		('on cooper', 'On Cooper'),
		('not on cooper', 'NOT On Cooper')
		
		)
	cop_sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default=1)
	receiever_mail = models.CharField(max_length=5000)
	status = models.CharField(max_length=30,choices=STATUS, default='not on cooper')

	def __str__(self):
		return "%s " %(self.cop_sender)							



class Fees(models.Model):
	
	admin = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	fee_name = models.CharField(max_length=5000)
	fee_charges = models.PositiveIntegerField(blank=True,null=True)

	def __str__(self):
		return "%s " %(self.admin)							



