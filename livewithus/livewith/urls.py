from django.conf.urls.defaults import *
from django.conf import settings

LIVE_SITE_PREFIX = settings.LIVE_SITE_PREFIX

urlpatterns = patterns(#'django.views.generic.simple',                     
                       'djsite',                       
    # utility URLs
    (r'utilities/', include('livewith.utilities.urls')),

    # alpha site URLs
    (r'faq/$', 'alpha.views.faq'),
    (r'do_signup/$', 'alpha.views.signup'),
    (r'signup/$', 'alpha.views.signup_page'),
    (r'signuphandler/$', 'alpha.views.signuphandler'),
    (r'signuphandler/forgotpassword$', 'alpha.views.forgotpassword'),
    (r'signuphandler/resetpassword$', 'alpha.views.resetpassword'),
    (r'chathandler$', 'alpha.views.chathandler'),
    (r'pollhandler$', 'alpha.views.pollhandler'),
    (r'savewikihandler$', 'alpha.views.savewikihandler'),
    (r'house_redirect$', 'alpha.views.house_redirect'),
     
    #(r'^%smy-settings/$', 'alpha.views.settings'),
    
    (r'alerts/(?P<alert_id>\d+)/pay_complete', 'alpha.views.complete_payrequest_alert'),
    (r'alerts/(?P<alert_id>\d+)/pay', 'alpha.views.accept_payrequest_alert'),
    (r'alerts/(?P<alert_id>\d+)/refuse', 'alpha.views.refuse_payrequest_alert'),
    (r'alerts/(?P<alert_id>\d+)/', 'alpha.views.ack_alert'),
    (r'join/(?P<approval_code>\w+)', 'alpha.views.joinhouse_with_code'),
    (r'(?P<house_id>\d+)/settings/$', 'alpha.views.house_settings'),
    (r'(?P<house_id>\d+)/invite_housemates/$', 'alpha.views.invite_housemates'),
    (r'(?P<house_id>\d+)/apply_house_settings/$', 'alpha.views.apply_house_settings'),
    (r'(?P<house_id>\d+)/$', 'alpha.views.dashboard'),
    (r'(?P<house_id>\d+)/chatter/(?P<chatter_id>\d+)/delete/$', 'alpha.views.delete_chatter'),
    (r'(?P<house_id>\d+)/chatter/(?P<chatter_id>\d+)/stick/$', 'alpha.views.stick_chatter'),
    (r'(?P<house_id>\d+)/chatter/(?P<chatter_id>\d+)/unstick/$', 'alpha.views.unstick_chatter'),
    (r'(?P<house_id>\d+)/chatter/more/$', 'alpha.views.more_chatter'),
    (r'(?P<house_id>\d+)/dashboard/$', 'alpha.views.dashboard'),
    (r'(?P<house_id>\d+)/finances/(?P<transaction_id>\d+)/details/$', 'alpha.views.finance_detail_view'),
    (r'(?P<house_id>\d+)/finances/new_purchase_handler$', 'alpha.views.new_purchase_handler'),
    (r'(?P<house_id>\d+)/finances/request_payment$', 'alpha.views.request_payment'),
    (r'(?P<house_id>\d+)/finances/request_payment_handler$', 'alpha.views.request_payment_handler'),
    (r'(?P<house_id>\d+)/finances/report_payment$', 'alpha.views.report_payment'),
    (r'(?P<house_id>\d+)/finances/report_payment_handler$', 'alpha.views.report_payment_handler'),
    (r'(?P<house_id>\d+)/finances/edit_payment_handler$', 'alpha.views.edit_payment_handler'),
    (r'(?P<house_id>\d+)/finances/edit_purchase_handler/(?P<purchase_id>\d+)$', 'alpha.views.edit_purchase_handler'),
    (r'(?P<house_id>\d+)/finances/new$', 'alpha.views.add_transaction'),
    (r'(?P<house_id>\d+)/finances/(?P<sort_view>\w+)$', 'alpha.views.finances'),
    (r'(?P<house_id>\d+)/finances/edit/(?P<transaction_id>\d+)$', 'alpha.views.edit_transaction'),
    (r'(?P<house_id>\d+)/finances/delete/(?P<transaction_id>\d+)$', 'alpha.views.delete_transaction_handler'),
    (r'dologin/$', 'alpha.views.do_login'),
    (r'login/$', 'alpha.views.loginrequired'),
    (r'logout/$', 'alpha.views.do_logout'),
#    (r'privacy/$', 'django.views.generic.simple.direct_to_template', {'template': 'alpha/privacy.html'}),
#    (r'faq/$', 'django.views.generic.simple.direct_to_template', {'template': 'alpha/faq.html'}),
    (r'apply_settings/$', 'alpha.views.apply_person_settings'),
    (r'settings/$', 'alpha.views.person_settings'),
    (r'signup/newhouse/$', 'alpha.views.createhouse'),
    (r'signup/do_createhouse/$', 'alpha.views.do_createhouse'),
    (r'signup/joinhouse/$', 'alpha.views.joinhouse'),
    (r'signup/(?P<approval_code>\w+)', 'alpha.views.signup_with_code'),
    (r'errors/houserequired/$', 'alpha.views.houserequired'),
    (r'test/(?P<template_id>\w+.html)$', 'alpha.views.test_view'),
    
    #top level directories have to be last
    (r'$', 'alpha.views.index'),
    )
