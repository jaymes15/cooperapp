from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile,ProjectProfile, CooperativeProjectProfile,CopInvite,Fees
from django.contrib.auth.models import User
from functools import partial


DateInput = partial(forms.DateInput, {'class': 'datepicker'})





class UserroleForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = [
                    'user_role',
                    
                    ]     



class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True,widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',
	        	}))
	username = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	password1 = forms.CharField(widget=forms.PasswordInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	password2 = forms.CharField(widget=forms.PasswordInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	  

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2'
			)                    


class UserUpdateForm(forms.ModelForm):
	 email = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	   
	 first_name = forms.SlugField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        
	 last_name =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	 
	 
	 class Meta:
	 	model = User
	 	fields = [
					'email',
					'first_name',
					'last_name',
					
					]

class EditCompanyprofileForm(forms.ModelForm):
	
	company_name=  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	description =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	city =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	address  =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	phone_number =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	membership_fee = forms.CharField(widget=forms.NumberInput(
	         	attrs={
	        			'class':'form-control',


	        	}))

	class Meta:
		model = UserProfile
		fields = [
		    'company_name',
			'description',
			'city',
			'address',
			'phone_number',
			'phone_number',
			'image',
			'membership_fee'
			
	]




class EditAjoCompanyprofileForm(forms.ModelForm):
	
	company_name=  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	description =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	city =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	address  =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	phone_number =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	

	class Meta:
		model = UserProfile
		fields = [
		    'company_name',
			'description',
			'city',
			'address',
			'phone_number',
			'phone_number',
			'image',
			
			
	]



class ProjectForm(forms.ModelForm):
	

	     project_name = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     project_description = forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     project_duration = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     contribution_amount = forms.CharField(widget=forms.NumberInput(
	         	attrs={
	        			'class':'form-control',


	        	}))

	     start_date = forms.DateField(widget=DateInput())
	     
	     end_date= forms.DateField(widget=DateInput())
	     class Meta:
	     	model = ProjectProfile
	     	fields = [
	        		'project_name',
	        		'project_description',
	        		'project_contribution',
	        		'project_distribution',
	        		'contribution_amount',
	        		'project_duration',
	        		'start_date',
	        		'end_date',
	        		'project_returns',

	        		]



class CooperativeProjectForm(forms.ModelForm):
	

	     project_name = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     project_description = forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     project_duration = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	    
	     start_date = forms.DateField(widget=DateInput())

	     end_date= forms.DateField(widget=DateInput())
	     

	    
	     class Meta:
	     	model = CooperativeProjectProfile
	     	fields = [
	        		'project_name',
	        		'project_description',
	        		'project_duration',
	        		'start_date',
	        		'end_date',
	        		'project_returns',
	        		'project_cost_perunitblock',
	        		'project_unitblock_available',
	        	

	        		]



class CopAdminInviteForm(forms.ModelForm):
	

	     receiever_mail =forms.EmailField(required=True,widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',
	        	}))
	    
	    
	     class Meta:
	     	model = CopInvite
	     	exclude = [
	        		'cop_sender',
	        		'status'
	        		]


class FeesForm(forms.ModelForm):
	

	     fee_name = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	     fee_charges = forms.CharField(widget=forms.NumberInput(
	         	attrs={
	        			'class':'form-control',


	        	}))
	     
	    
	     class Meta:
	     	model = Fees
	     	fields = [
	        		'fee_name',
	        		'fee_charges'
	        	

	        		]




