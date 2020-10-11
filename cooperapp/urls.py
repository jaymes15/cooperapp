from . import views
from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



app_name= 'cooperapp'
urlpatterns = [
	path('', views.index,name='index'),
    path('ajo/', views.homepage,name='homepage'),
	path('signup/', views.signup,name='signup'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('profile/', views.userprofile,name='userprofile'),
    url(r'^profile(?P<pk>\d+)/$',views.otherprofile,name='otherusersprofile'),
    path('editcompanyprofile/', views.editcompanyprofile,name='editcompanyprofile'),
    path('ajoprojectform/',views.projectform,name='projectform'),
    path('projectbyuser/<int:user_id>', views.projectbyuser, name='projectbyuser'),
    path('projectbyotheruser/<int:user_id>', views.projectbyotheruser, name='projectbyotheruser'),
    path('joinproject/<int:project_id>/<int:user_id>', views.joinproject, name='joinproject'),
    path('projectcontributor/<int:project_id>/<int:user_id>', views.projectcontributor, name='projectcontributor'),
    path('alluserinjoinproject/<int:project_id>/<int:projectcontributor_id>', views.alljoinproject, name='alljoinproject'),
    path('optoutproject/<int:project_id>/<int:user_id>', views.Optoutofproject, name='optoutofproject'),
    path('ajocontribution/<int:project_id>', views.getcontributionactiveproject, name='getcontributionactiveproject'),
    path('allcontributionactiveproject/<int:user_id>', views.allcontributionactiveproject, name='allcontributionactiveproject'),
    path('allcontributionactiveprojectbyweek/<int:user_id>', views.allcontributionactiveprojectbyweek, name='allcontributionactiveprojectbyweek'),
    path('allcontributionactiveprojectbymonth/<int:user_id>', views.allcontributionactiveprojectbymonth, name='allcontributionactiveprojectbymonth'),
    path('makeajocontribution/', views.makeajocontribution, name='makeajocontribution'),
    path('success/', views.success, name='success'),
    path('join/', views.cooperatives,name='cooperatives'),
    path('cooperativeprojectform/',views.cooperativeprojectform,name='cooperativeprojectform'),
    path('coperativeprojectbyuser/<int:user_id>', views.cooperativeprojectbyuser, name='cooperativeprojectbyuser'),
    path('cooperativehomepage/', views.cooperativehomepage,name='cooperativehomepage'),
    path('cooperativeprojectbyotheruser/<int:user_id>', views.cooperativeprojectbyotheruser, name='cooperativeprojectbyotheruser'),
    path('cooperativejoinproject/<int:project_id>/<int:user_id>', views.cooperativejoinproject, name='cooperativejoinproject'),
    path('allcopcontributionactiveproject/<int:user_id>', views.allcopcontributionactiveproject, name='allcopcontributionactiveproject'),
    path('copprojectcontributor/<int:project_id>', views.copprojectcontributor, name='copprojectcontributor'),
    path('cooperativedashboard/<int:copproject_id>', views.cooperativedashboard, name='cooperativedashboard'),
    path('optoutcopproject/<int:project_id>/<int:user_id>', views.Optoutofcopproject, name='optoutofcopproject'),
    path('cooperativepaymentinfo/', views.cooperativepaymentinfo, name='cooperativepaymentinfo'),
    path('requestajoadminverification/<int:user_id>', views.requestajoadminverification, name='requestajoadminverification'),
    path('requestcopadminverification/<int:user_id>', views.requestcopadminverification, name='requestcopadminverification'),
    path('optoutcopprojectadmin/<int:project_id>/<int:user_id>', views.Optoutofcopprojectadmin, name='optoutofcopprojectadmin'),
    path('cooperativeinvestment/', views.cooperativeinvestment, name='cooperativeinvestment'),
    path('copprojectinvestors/<int:project_id>/<int:investment_id>', views.copprojectinvestors, name='copprojectinvestors'),
    path('faq/',views.faq,name='faq'),
    path('privacy/', views.privacy,name='privacy'),
    path('about/', views.about,name='about'),
    path('tandc/', views.tandc,name='tandc'),
    path("administrative/<int:user_id>", views.administrative, name="administrative"),
    path("admininvite/", views.admininvite, name="admininvite"),
    path("fees/", views.fees, name="fees"),
    path("deletefee/<int:fee_id>", views.deletefee, name="deletefee"),
    path('checkaccount/',views.checkaccount,name="checkaccount"),
    path('generate_receipt/',views.generate_receipt,name="generate_receipt")
   ]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)