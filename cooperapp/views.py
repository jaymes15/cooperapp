from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import EditAjoCompanyprofileForm,FeesForm,CopAdminInviteForm,RegistrationForm,UserroleForm,EditCompanyprofileForm,UserUpdateForm,ProjectForm,CooperativeProjectForm
from django.contrib.auth.decorators import login_required
from .models import Fees,RequestAjoAdminverification,CopInvite,CooperativeInvestment,RequestCopAdminverification,CooperativeContributions,UserProfile,ProjectProfile,ProjectContributors,Contributions,CooperativeProjectProfile,CooperativeProjectContributors
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from datetime import datetime,date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import requests
import json
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import time, threading

#pk_test_1ae21e3c162a5687048938e7b4afad6ab72180a4
#paystacksecretkey = "Bearer sk_test_1590017dabc1772e81fd0e246379f6e6ebcfac80"
paystacksecretkey = "Bearer sk_live_8caf73c24429b9d6ca2be4b5f3d1cfa0d101c38f"

def index(request):

	return render(request,'cooperapp/index.html')

def faq(request):

	return render(request,'cooperapp/faqs.html')

def privacy(request):

	return render(request,'cooperapp/privacy.html')

def about(request):

	return render(request,'cooperapp/about.html')

def tandc(request):

	return render(request,'cooperapp/tandc.html')

def ajosendremindermail():


	ajo = ProjectContributors.objects.all()
	todaydate = datetime.today()
	comparedate = datetime.date(todaydate)
	for i in ajo:
		if i.project_name.start_date <= comparedate and i.project_name.end_date >= comparedate:
			subject = 'Cooper Ajo Contribution Reminder'
			contributors = i.user.email
			contributor_name = i.user.username
			ajoname = i.project_name.project_name
			print(ajoname)
			contribution_amount = i.project_name.contribution_amount
			print(contribution_amount)
			projectid = str(i.project_name.id)
			context ={
			'projectid':projectid,
			'contributor_name':contributor_name,
			"ajoname":ajoname,
			"contribution_amount":contribution_amount
			}
			html_message = render_to_string('cooperapp/ajosendremindermaily.html', context)
			plain_message = strip_tags(html_message)
			from_email = settings.EMAIL_HOST_USER
			to = contributors
			mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
			

	threading.Timer(86400, ajosendremindermail).start()


def homepage(request):
	projects = ProjectProfile.objects.all()
	context = {'projects':projects}
	return render(request,'cooperapp/homepage.html', context)

def signup(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		userstatus = UserroleForm(request.POST)

		if form.is_valid() and userstatus.is_valid() :
			user= form.save()
			profile = userstatus.save(commit = False)
			profile.user = user
			profile.save()
			login(request,user)
			return redirect('cooperapp:login')
	else:
		form = RegistrationForm()
		userstatus = UserroleForm()
	return render(request,'cooperapp/signup.html',{'form':form,'userstatus':userstatus,  })



def login_view(request):
	#ajosendremindermail()
	if request.method =='POST':
		p_form = AuthenticationForm(data=request.POST)
		if p_form.is_valid():
			#Log user in
			user = p_form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				if request.user.userprofile.user_role == "none":
					return redirect('cooperapp:allcopcontributionactiveproject',user_id=request.user.id)
				elif request.user.userprofile.user_role == "ajo":
					return redirect('cooperapp:projectform')

				else:
					return redirect('cooperapp:cooperativeprojectform')
						

	else:
		p_form = AuthenticationForm()
	return render(request,'cooperapp/login.html',{'p_form':p_form})

def logout_view(request):

	if request.method =='POST':
		logout(request)
	return redirect('cooperapp:login')



@login_required(login_url="/login/")
def userprofile(request,pk=None):
	if pk:
		user = User.objects.get(pk=pk)
		args = {'user':user}
		return render(request,'cooperapp/profile.html',args)


	else:
		user = request.user
		if request.method == 'POST':
				
				p_form = EditCompanyprofileForm(request.POST,request.FILES, instance=request.user.userprofile)
				u_form = UserUpdateForm(request.POST,instance=request.user)
				

				if p_form.is_valid() and u_form.is_valid()  :
					p_form.save()
					u_form.save()
					return redirect('cooperapp:userprofile')
			
		else:

			p_form =  EditCompanyprofileForm( instance=request.user.userprofile)
			u_form = UserUpdateForm(instance=request.user)
			args = {'user':user,'p_form':p_form,'u_form':u_form}
			return render(request,'cooperapp/profile.html',args)


	

	

@login_required(login_url="/login/")
def editcompanyprofile(request):
		if request.method == 'POST':
				
				p_form = EditCompanyprofileForm(request.POST,request.FILES, instance=request.user.userprofile)
				u_form = UserUpdateForm(request.POST,instance=request.user)
				

				if p_form.is_valid() and u_form.is_valid()  :
					p_form.save()
					u_form.save()
					return redirect('cooperapp:userprofile')
			
		else:

			p_form =  EditCompanyprofileForm( instance=request.user.userprofile)
			u_form = UserUpdateForm(instance=request.user)
			context = {'p_form':p_form,'u_form':u_form}
		return render(request,'cooperapp/editprofile.html',context)



@login_required(login_url="/login/")
def projectform(request):
	user_projects =	ProjectProfile.objects.filter(user_id=request.user.id)
	if request.method =='POST':
		a_form = ProjectForm(request.POST,request.FILES)
		if a_form.is_valid():
			#save to db
			project= a_form.save(commit=False)
			project.user = request.user
			#project.companyprofile = request.user.id
			project.save()
			return redirect('cooperapp:projectform')
	else:
		a_form =  ProjectForm()
	return render(request,'cooperapp/ajoprojectform.html',{'a_form':a_form,'user_projects': user_projects})	

def projectbyuser(request,user_id):
	user_projects =	ProjectProfile.objects.filter(user_id=user_id)
	
	context = {'user_projects': user_projects}
	return render(request, 'cooperapp/projectbyuser.html', context)		


def projectbyotheruser(request,user_id):
	project = ProjectProfile.objects.get(id=user_id)
	dat = datetime.today()
	context = {'project': project, "dat":dat}
	return render(request, 'cooperapp/projectbyotherusers.html', context)

def otherprofile(request,pk):
	
		user = User.objects.get(pk=pk)
		args = {'user':user}
		return render(request,'cooperapp/otherprofile.html',args)	



@login_required(login_url="/login/")
def joinproject(request, project_id, user_id):
	if request.method =='POST':
		user = ProjectContributors.objects.filter(user=user_id)
		
		if user.filter(project_name=project_id).exists():
			return redirect('cooperapp:homepage')
		else:	
			projectcontributor = ProjectContributors(user = User(user_id), project_name = ProjectProfile(project_id))
			projectcontributor.save()
			dat = datetime.today()
			message = "You Have Been Added to this Project Successfully"
			return redirect('cooperapp:alljoinproject', project_id=project_id,projectcontributor_id=projectcontributor.id)
		





@login_required(login_url="/login/")
def alljoinproject(request, project_id,projectcontributor_id):
	project_contributors = ProjectContributors.objects.filter(project_name = project_id)
	project = ProjectContributors.objects.get(id = projectcontributor_id)
	context = {'project':project, 'project_contributors':project_contributors}
	return render(request,'cooperapp/joinproject.html',context)	
		
@login_required(login_url="/login/")				
def projectcontributor(request,project_id,user_id):
	user =	ProjectProfile.objects.get(id= project_id)
	project_contributors = ProjectContributors.objects.filter(project_name = project_id)
	contributions = Contributions.objects.filter(project_name = project_id)
	
	context = {'user': user,'project_contributors':project_contributors,"contributions" : contributions}
	return render(request, 'cooperapp/projectbyuserContributor.html', context)		
	
@login_required(login_url="/login/")
def Optoutofproject(request, project_id, user_id):
	if request.method =='POST':
		
		project = ProjectContributors.objects.filter(project_name = project_id)
		user = project.get(user_id=user_id)
		user.delete()
		return redirect('cooperapp:homepage')


@login_required(login_url="/login/")
def allcontributionactiveproject(request,  user_id):
	user_projects = ProjectContributors.objects.filter(user_id = user_id)
	dat = datetime.now()
	context = {'user_projects': user_projects,"dat":dat}
	return render(request, 'cooperapp/allcontributionactiveproject.html', context)

@login_required(login_url="/login/")
def getcontributionactiveproject(request,  project_id):
	user_project = ProjectContributors.objects.filter(user_id = request.user.id)
	user_projects = user_project.get(project_name = project_id)
	savings = Contributions.objects.filter(user_id = request.user.id)
	saving = savings.filter(project_name = project_id)
	amount = 0
	for save in saving:
		amount += int(save.amount)

	dat = datetime.now()
	context = {'user_projects': user_projects,"dat":dat,"amount":amount}
	return render(request, 'cooperapp/makeajocontribution.html', context)	

@login_required(login_url="/login/")
def allcontributionactiveprojectbyweek(request,  user_id):
	user_weekly = ProjectContributors.objects.filter(user_id = user_id)
	user_projects = user_weekly.filter(project_name__project_contribution = "weekly")
	dat = datetime.now()
	context = {'user_projects': user_projects,"dat":dat}
	return render(request, 'cooperapp/allcontributionactiveproject.html', context)


@login_required(login_url="/login/")
def allcontributionactiveprojectbymonth(request,  user_id):
	user_monthly = ProjectContributors.objects.filter(user_id = user_id)
	user_projects = user_monthly.filter(project_name__project_contribution = "monthly")
	dat = datetime.today()

	context = {'user_projects': user_projects,"dat":dat}
	return render(request, 'cooperapp/allcontributionactiveproject.html', context)	

@login_required(login_url="/login/")
def makeajocontribution(request):
	userid = request.POST.get('userid',None)
	transactionid = request.POST.get('transactionid',None)
	project_id = request.POST.get('project_id',None)
	amount = request.POST.get('amount',None)

	if request.method =='POST':
		

		response = requests.get('https://api.paystack.co/transaction/verify/'+transactionid, headers={
    				'Authorization': paystacksecretkey,
                  })
		if response.status_code == 200:
			result = response.json()
			if (result["data"]['reference'] == transactionid ) :
				project = ProjectProfile.objects.get(id= project_id)
				start = project.start_date
				ends = datetime.now()
				end = date(ends.year,ends.month,ends.day)
				days = abs(start - end).days
				week = days//7
				contribution = Contributions(user = User(userid), project_name = ProjectProfile(project_id), week_num = week, amount =amount, date = datetime.now())
				contribution.save()
				return HttpResponse(status = 200)

def success(request):
	return render(request, 'cooperapp/success.html')	





@login_required(login_url="/login/")
def cooperativeprojectform(request):
	user_projects =	CooperativeProjectProfile.objects.filter(user_id=request.user.id)
	if request.method =='POST':
		a_form = CooperativeProjectForm(request.POST,request.FILES)
		if a_form.is_valid():
			#save to db
			project= a_form.save(commit=False)
			project.user = request.user

			#project.companyprofile = request.user.id
			project.save()
			return redirect('cooperapp:cooperativeprojectform')
	else:
		a_form =  CooperativeProjectForm()
	return render(request,'cooperapp/projectform.html',{'a_form':a_form,'user_projects':user_projects})




@login_required(login_url="/login/")
def cooperativeprojectbyuser(request,user_id):
	user_projects =	CooperativeProjectProfile.objects.filter(user_id=user_id)
	
	context = {'user_projects': user_projects}
	return render(request, 'cooperapp/cooperativeprojectbyuser.html', context)		

		
def cooperatives(request):
	projects = UserProfile.objects.filter(user_role = "co-operative")
	context = {'projects':projects}
	return render(request,'cooperapp/cooperatives.html', context)		

def cooperativehomepage(request):
	projects = CooperativeProjectProfile.objects.all()
	context = {'projects':projects}
	return render(request,'cooperapp/cooperativehomepage.html', context)



def cooperativeprojectbyotheruser(request,user_id):
	project = UserProfile.objects.get(id=user_id)
	confirm = CooperativeProjectContributors.objects.filter(cooperative_name=user_id)
	if CooperativeProjectContributors.objects.filter(cooperative_name=user_id).exists():
		confirm = CooperativeProjectContributors.objects.filter(cooperative_name=user_id)
		if confirm.filter(user=request.user.id).exists():
			confirm_status = confirm.get(user=request.user.id)
			# dat = datetime.today()
			context = {'project': project,'confirm_status':confirm_status}
			return render(request, 'cooperapp/cooperativeprojectbyotherusers.html', context)
	
	context = {'project': project}
	return render(request, 'cooperapp/cooperativeprojectbyotherusers.html', context)	
	

@login_required(login_url="/login/")
def cooperativejoinproject(request, project_id, user_id):
	userid = request.POST.get('userid',None)
	transactionid = request.POST.get('transactionid',None)
	project_id = request.POST.get('project_id',None)
	amount = request.POST.get('amount',None)
	if request.method == 'POST':
		

		response = requests.get('https://api.paystack.co/transaction/verify/'+transactionid, headers={
    				'Authorization': paystacksecretkey,
                  })
		if response.status_code == 200:

			result = response.json()
			if (result["data"]['reference'] == transactionid ) :
				cop = CooperativeProjectContributors.objects.filter(cooperative_name=project_id)
				if cop.filter(user=user_id).exists():
					return redirect('cooperapp:homepage')
				else:
					projectcontributor = CooperativeProjectContributors(
								user = User(user_id), 
								cooperative_name = UserProfile(project_id),
								status = "active"
								)
					projectcontributor.save()
					message = "You Have Been Added to this Project Successfully"
					return redirect('cooperapp:success')


@login_required(login_url="/login/")
def allcopcontributionactiveproject(request,user_id):
	user_projects = CooperativeProjectContributors.objects.filter(user_id = user_id)
	user_investments = CooperativeInvestment.objects.filter(user = request.user.id)
	user_investment =user_investments.filter(status="active")
	user_savings = CooperativeContributions.objects.filter(user=request.user.id)
	user_ajoprojects = ProjectContributors.objects.filter(user_id = user_id)
	dat = datetime.now()
	context = {'dat':dat,'user_projects': user_projects,'user_investment':user_investment,'user_savings':user_savings,'user_ajoprojects':user_ajoprojects}
	return render(request, 'cooperapp/allcopcontributionactiveproject.html', context)



@login_required(login_url="/login/")				
def copprojectcontributor(request,project_id):
	#user =	CooperativeProjectProfile.objects.get(id= project_id)
	project_contributors = CooperativeProjectContributors.objects.filter(cooperative_name = project_id)
	contributions = CooperativeContributions.objects.filter(cooperative_name = project_id)
	investments = CooperativeInvestment.objects.filter(cooperative_name = project_id)
	
	context = {'project_contributors':project_contributors, 'contributions':contributions,'investments':investments}
	return render(request, 'cooperapp/copprojectbyuserContributor.html', context)		
	

@login_required(login_url="/login/")				
def copprojectinvestors(request,project_id,investment_id):
	user_projects =	CooperativeProjectProfile.objects.get(id= investment_id)
	investments = CooperativeInvestment.objects.filter(cooperative_name = project_id)
	investment = investments.filter(investment_name= investment_id)
	context = {'investments':investment,'user':user_projects}
	return render(request, 'cooperapp/copprojectinvestors.html', context)		
	

@login_required(login_url="/login/")
def cooperativedashboard(request,copproject_id):
	#print(copproject_id)

	user_project = CooperativeProjectContributors.objects.filter(user = request.user.id)
	user_projects = user_project.get(cooperative_name = copproject_id)
	investments = CooperativeProjectProfile.objects.filter(user=copproject_id)
	userinvestments = CooperativeInvestment.objects.filter(cooperative_name=copproject_id)
	userinvestment = userinvestments.filter(user=request.user.id)
	response = requests.get('https://api.paystack.co/bank', headers={
    				'Authorization': paystacksecretkey,
                  })
	if response.status_code == 200:
		results = response.json()
		result = results['data']
			
	
	if CooperativeContributions.objects.filter(cooperative_name=copproject_id).exists():

		cop = CooperativeContributions.objects.filter(cooperative_name=copproject_id)
		print("hello")
		if cop.filter(user=request.user.id).exists():

			cooperative = cop.get(user=request.user.id)
			
			response = requests.get('https://api.paystack.co/bank', headers={
    				'Authorization': paystacksecretkey,
                  })

			try:
				if response.status_code == 200:
					results = response.json()
					result = results['data']
					print("result")
					print(result);
					context = {
								'stat': user_projects,
								'user': user_projects,
								"cooperative":cooperative,
								'investments':investments,
								"userinvestment":userinvestment,
								'result':result
								}
					return render(request, 'cooperapp/cooperativedashboard.html', context)
					
			except Exception as ex:
				context = {"error":ex}
				return render(request,'paystacktransapp/homepage.html',context)

	
	context = {'user': user_projects,"investments":investments,"userinvestment":userinvestment,'result':result}
	return render(request, 'cooperapp/cooperativedashboard.html', context)		



@login_required(login_url="/login/")
def cooperativeinvestment(request):
	userid = request.user.id 
	unitBought = request.POST.get('UnitBought',None)
	transactionid = request.POST.get('transactionid',None)
	investmentid = request.POST.get('investmentid',None)
	cooperativeid = request.POST.get('cooperativeid',None)
	if request.method == 'POST':
		

		response = requests.get('https://api.paystack.co/transaction/verify/'+transactionid, headers={
    				'Authorization': paystacksecretkey,
                  })
		if response.status_code == 200:

			result = response.json()
			if (result["data"]['reference'] == transactionid ) :
				userinvestment = CooperativeInvestment(
								user = User(userid), 
								cooperative_name = UserProfile(cooperativeid),
								investment_name	= CooperativeProjectProfile(investmentid),
								unitblock_purchased = unitBought,
								status = "active"
								)
				userinvestment.save()
				message = "You Have Been Added to this Project Successfully"
				return redirect('cooperapp:success')









# @login_required(login_url="/login/")
# def Optoutofcopproject(request, project_id, user_id):
# 	if request.method =='POST':
		
# 		project = CooperativeProjectContributors.objects.filter(project_name = project_id)
# 		user = project.get(user_id=user_id)
# 		user.delete()
# 		if CooperativeContributions.objects.filter(project_name = project_id).exists():
# 			contributions = CooperativeContributions.objects.filter(project_name = project_id)
# 			if contributions.filter(user=user_id).exists():
# 				contribution = contributions.get(user=user_id)
# 				contribution.delete()
# 		return redirect('cooperapp:homepage')


@login_required(login_url="/login/")
def Optoutofcopprojectadmin(request, project_id, user_id):
	if request.method =='POST':
		
		project = CooperativeProjectContributors.objects.filter(cooperative_name = project_id)
		user = project.get(user_id=user_id)
		user.status = "disabled"
		user.save()
		return redirect('cooperapp:userprofile')



def Optoutofcopproject(request, project_id, user_id):
	if request.method =='POST':
		project = CooperativeProjectContributors.objects.filter(cooperative_name = project_id)
		user = project.get(user_id=user_id)
		user.status = "requesting out"
		user.save()
		return redirect('cooperapp:userprofile')


def cooperativepaymentinfo(request):
	
	userid = request.POST.get('userid',None)
	transactionid = request.POST.get('transactionid',None)
	project_id = request.POST.get('project_id',None)
	amount = request.POST.get('amount',None)
	if request.method == 'POST':
		

		response = requests.get('https://api.paystack.co/transaction/verify/'+transactionid, headers={
    				'Authorization': paystacksecretkey,
                  })
		if response.status_code == 200:

			result = response.json()
			if (result["data"]['reference'] == transactionid ) :
				
				cop = CooperativeContributions.objects.filter(cooperative_name=project_id)
				
				if cop.filter(user=userid).exists():
					print("hello3")
					coper = cop.get(user=userid)
					coper.total_amount += int(amount)
					coper.save()
					results = {'message': 'Succesfully Payment'}
					return JsonResponse(results)
				else:	
					projectcontributor = CooperativeContributions(
											user = User(userid), 
											cooperative_name = UserProfile(project_id),
											amount=amount,
											total_amount=amount
											)
					projectcontributor.save()
					message = "You Have Been Added to this Project Successfully"
					return render(request, 'cooperapp/homepage.html')
					

@login_required(login_url="/login/")
def requestajoadminverification(request, user_id):
	user = RequestAjoAdminverification(user = request.user,date = datetime.now() )
	user.save()	
	message = "Request Verifcation Succesfully Sent";
	context = {'message':message}
	return render(request,'cooperapp/success.html',context)



@login_required(login_url="/login/")
def requestcopadminverification(request, user_id):
	user = RequestCopAdminverification(user = request.user,date = datetime.now() )
	user.save()	
	message = "Request Verifcation Succesfully Sent";
	context = {'message':message}
	return render(request,'cooperapp/success.html',context)

def administrative(request,user_id):
	copadmin = UserProfile.objects.get(user=user_id)
	context = {'copadmin':copadmin}
	return render(request,'cooperapp/administrative.html',context)

@login_required(login_url="/login/")
def admininvite(request):
	copadmin = CopInvite.objects.filter(cop_sender=request.user.userprofile.id)
	for i in copadmin:
		print(i.receiever_mail)
		if User.objects.filter(email=i.receiever_mail).exists():
			i.status = "on cooper"
			i.save()			
	
	if request.method =='POST':
		a_form = CopAdminInviteForm(request.POST,request.FILES)
		if a_form.is_valid():
			#save to db
			invite= a_form.save(commit=False)
			invite.cop_sender = UserProfile(request.user.userprofile.id)
			#project.companyprofile = request.user.id
			if User.objects.filter(email=invite.receiever_mail).exists():
				invite.status = "on cooper"
			else:
				invite.status = "not on cooper"

			invite.save()
			
			subject = 'Cooper Invite'
			copinvite = request.user.userprofile.company_name
			
			context ={'copinvite':copinvite}
			html_message = render_to_string('cooperapp/emailbody.html', context)
			plain_message = strip_tags(html_message)
			from_email = settings.EMAIL_HOST_USER
			to = invite.receiever_mail
			mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
			return redirect('cooperapp:admininvite')
	else:
		a_form = CopAdminInviteForm()
		
	context = {'a_form':a_form,"copadmin":copadmin}
	return render(request,"cooperapp/administrative.html",context)	
			
	

def fees(request):
	all_fees = Fees.objects.filter(admin=request.user)
	
	if request.method == 'POST':
				p_form = FeesForm(request.POST,request.FILES)

				if p_form.is_valid():
					fees = p_form.save(commit =False)
					fees.admin = request.user
					p_form.save()
					return redirect('cooperapp:fees')
			
	else:
		p_form =  FeesForm()
		context = {'all_fees':all_fees,'p_form':p_form}
		return render(request,'cooperapp/fees.html',context)
def deletefee(request,fee_id):
	if request.method == 'POST':
		fee = Fees.objects.get(id=fee_id)
		fee.delete()
		return redirect('cooperapp:fees')
	else:
		return redirect('cooperapp:fees')


#withdrawal



def checkaccount(request):
	try:
		
		global bankcode
		bankcode = request.POST.get('bankcode',None)
		accountnumber = request.POST.get('accountnumber',None)
		
		response = requests.get('https://api.paystack.co/bank/resolve?account_number='+accountnumber+'&bank_code='+bankcode, headers={
        			      'Authorization': paystacksecretkey,
        	           })
		if response.status_code == 200:
			results = response.json()
			global acccount_details 
			acccount_details = results
			return JsonResponse(results)
		else:
			return HttpResponseBadRequest()
				
	except Exception as ex:
		context = {"error":ex}
		return render(request,'cooperapp/homepage.html',context)	




def generate_receipt(request):
	try:
		amount = request.POST.get('amount',None)

		he = {"Authorization": paystacksecretkey,"Content-Type" : "application/json"}
		info ={"type": "nuban",
		        "name": str(acccount_details['data']['account_name']),
				"account_number": str(acccount_details['data']['account_number']),
				"bank_code": str(bankcode),
				"currency": "NGN"
				}
		try:
			response = requests.post("https://api.paystack.co/transferrecipient",json=info,headers=he)
			if response.status_code == 201:
					results = response.json()
					global receipt
					receipt = results
					he = {"Authorization": paystacksecretkey,"Content-Type" : "application/json"}
					info ={ "source": "balance",
							 "amount": int(amount),
							 "recipient": str(receipt['data']['recipient_code']),
							 "reason": "Cooper withdrawal" 
							 }
							 
					response = requests.post("https://api.paystack.co/transfer",json=info,headers=he)
					if response.status_code == 201:
								message={"message":"You have been credited"}
								return JsonResponse(message)
					else:
							
							message={"message":"You cannot initiate third party payouts as a starter business"}
							return JsonResponse(message)		
		except Exception as ex:
			message={"message":ex}
			return JsonResponse(message)		
					
	except Exception as ex:
		message={"message":ex}
		return JsonResponse(message)

				











    				


		
