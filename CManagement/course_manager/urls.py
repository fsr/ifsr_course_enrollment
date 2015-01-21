from django.conf.urls import patterns, url
from course_manager.views import View_Organizer, View_Participants,\
    View_Login, View_Tutor, View_Organizer_Email, View_password, View_Tutor_Email

urlpatterns = patterns('',
    # Participants' View
    url(r'^home/$', View_Participants.index, name='index'),
    url(r'^(?P<appointment_id>\d+)/signinapp/$', View_Participants.show_enroll, name='show_enroll'),
    url(r'^(?P<appointment_id>\d+)/signinappdone/$', View_Participants.process_enrollment, name='proc_enroll'),
    url(r'^confirm/(?P<confirmation_code>\w*?)/(?P<username>\w*?)/(?P<app_id>\d+)/$',
        View_Participants.confirm, name='confirm_enroll'),
    url(r'^(?P<appointment_id>\d+)/enrollmailout/$', View_Participants.show_enroll_mail_out, name='show_en_mail_out'),
    url(r'^(?P<appointment_id>\d+)/signinsucc/$', View_Participants.show_enroll_success, name='show_enroll_succ'),
    url(r'^notemailsuccpart/$', View_Participants.show_notification_email_success, name='noteMailSuccPart'),
    url(r'^notetimeoutpart/$', View_Participants.show_notification_timeout, name='noteTimeoutPart'),
    url(r'^whoReadsThis/$', View_Participants.show_awesome_guys, name='teamcredits'),

    # Organizers' View:
    url(r'^exec/$', View_Organizer.executives_index, name='exec'),
    url(r'^orgashowallc/$', View_Organizer.show_all_courses, name='orgaShowAllCourses'),
    url(r'^orgashowallt/$', View_Organizer.show_all_tutors, name='orgaShowAllTutors'),

    # Organizer: add/edit appointments
    url(r'^(?P<course_id>\d+)/showcourseapp/$', View_Organizer.show_course_appointments, name='showCourseAppointments'),
    url(r'^(?P<course_id>\d+)/addapp/$', View_Organizer.show_add_appointments, name='newAppointmentForm'),
    url(r'^(?P<course_id>\d+)/addappdone/$', View_Organizer.add_appointment, name='AppointmentFormDone'),
    url(r'^(?P<app_id>\d+)/editapp/$', View_Organizer.show_edit_appointments, name='editAppointmentForm'),
    url(r'^(?P<app_id>\d+)/editappdone/$', View_Organizer.edit_appointment, name='editAppointmentFormDone'),
    url(r'^(?P<app_id>\d+)/deleteapp/$', View_Organizer.delete_appointment, name='delAppointment'),
    url(r'^(?P<app_id>\d+)/orgshowpart/$', View_Organizer.show_appointment_participants, name='showAppointmentPart'),
    url(r'^(?P<app_id>\d+)/orgaddpart/$', View_Organizer.show_add_participant, name='showAddPart'),

    # Organizer: add/remove Participants
    url(r'^(?P<app_id>\d+)/orgaddpartdone/$', View_Organizer.add_participant_done, name='addPartDone'),
    url(r'^(?P<part_id>\d+)/(?P<app_id>\d+)/delpart/$', View_Organizer.delete_participant, name='deletePart'),

    # Organizer: add Course
    url(r'^addcourse/$', View_Organizer.show_add_course, name='addCourseForm'),
    url(r'^addcoursedone/$', View_Organizer.add_course, name='addCourseFormDone'),

    # Organizer: delete Course
    url(r'^(?P<course_id>\d+)/delcourse/$', View_Organizer.show_add_course, name='delCourseForm'),
    url(r'^(?P<course_id>\d+)/delcoursedone/$', View_Organizer.delete_course, name='delCourseFormDone'),

    # Organizer: toggle visibility
    url(r'^(?P<course_id>\d+)/tviscourse/$', View_Organizer.toggle_course_visibility, name='toggleCourseVis'),

    # Organizer: show credit date for course participants
    url(r'^(?P<course_id>\d+)/showcredcourse/$', View_Organizer.show_course_credits, name='showCourseCredits'),

    # Organizer: add Tutor
    url(r'^addtut/$', View_Organizer.show_create_tutor_form, name='addTutorForm'),
    url(r'^addtutdone/$', View_Organizer.create_tutor, name='addTutorFormDone'),

    # Organizer: edit/delete Tutor
    url(r'^(?P<tutor_id>\d+)/edittut/$', View_Organizer.show_edit_tutor, name='editTutorForm'),
    url(r'^(?P<tutor_id>\d+)/edittutdone/$', View_Organizer.edit_tutor, name='editTutorFormDone'),
    url(r'^(?P<tutor_id>\d+)/deltutdone/$', View_Organizer.delete_tutor, name='delTutorFormDone'),
    url(r'^(?P<app_id>\d+)/assigntut/$', View_Organizer.show_assign_tutor_to_app, name='assignTutorForm'),
    url(r'^(?P<app_id>\d+)/assigntutdone/$', View_Organizer.assign_tutor_to_app, name='assignTutorFormDone'),

    # Organizer: notifications
    url(r'^notemailsucc/$', View_Organizer.show_notification_email_success, name='noteMailSuccOrga'),
    url(r'^notetutsucc/$', View_Organizer.show_notification_addtutor_success, name='noteTutSuccOrga'),

    # Tutors' View:
    url(r'^tutor/$', View_Tutor.tutor_index, name='tut'),
    url(r'^(?P<course_id>\d+)/tutshowcapp/$', View_Tutor.show_course_appointments, name='showCourseAppointmentsTut'),
    url(r'^(?P<app_id>\d+)/tutshowpart/$', View_Tutor.show_appointment_participants, name='showAppointmentPartTut'),
    url(r'^(?P<part_id>\d+)/delparttut/$', View_Tutor.delete_participant, name='deletePartTut'),
    url(r'^(?P<app_id>\d+)/tutsetloc/$', View_Tutor.edit_appointment_location, name='editAppointmentLocTut'),
    url(r'^(?P<app_id>\d+)/tutsetlocdone/$', View_Tutor.edit_appointment_location_done, name='editAppointmentLocTutD'),

    # Tutor: notifications
    url(r'^notemailsucctut/$', View_Tutor.show_notification_email_success, name='noteMailSuccTut'),

    # login and logout:
    url(r'^loginDone/$', View_Login.login_executive, name='loginDone'),
    url(r'^Login/$', View_Login.show_form_login, name='newLoginForm'),
    url(r'^Logout/$', View_Login.logout_view, name='Logout'),

    # send EMails:
    url(r'^(?P<recipient_id>\d+)/newemailformpart/$', View_Participants.show_form_email, name='newEmailFormPart'),
    url(r'^(?P<recipient_id>\d+)/sendmailpart/$', View_Participants.send_email, name='sendmailparticipant'),
    url(r'^(?P<recipient_id>\d+)/newemailform/$', View_Organizer_Email.show_form_email, name='newEmailFormOrga'),
    url(r'^(?P<recipient_id>\d+)/sendmail/$', View_Organizer_Email.send_email, name='sendmail'),
    url(r'^(?P<course_id>\d+)/newemmailfo/$', View_Organizer_Email.show_form_email_to_course, name='newMEmailFormOrga'),
    url(r'^(?P<course_id>\d+)/sendmmailorga/$', View_Organizer_Email.send_email_to_course, name='sendmmailOrga'),
    url(r'^(?P<recipient_id>\d+)/newemailformtut/$', View_Tutor_Email.show_form_email, name='newEmailFormTut'),
    url(r'^(?P<recipient_id>\d+)/sendmailtut/$', View_Tutor_Email.send_email, name='sendmailtut'),
    url(r'^(?P<course_id>\d+)/newemmailftut/$', View_Tutor_Email.show_form_email_to_course, name='newMEmailFormTut'),
    url(r'^(?P<course_id>\d+)/sendmmailtut/$', View_Tutor_Email.send_email_to_course, name='sendmmailtut'),

    # show appointments
    url(r'^(?P<course_id>\d+)/indexsapp/$', View_Participants.index_show_appointments, name='showAppointments'),
    url(r'^(?P<appointment_id>\d+)/appinfo/$', View_Participants.show_app_information, name='showAppInfo'),

    # reset password
    url(r'^resetpassword/passwordsent/$', View_password.password_reset_done, name='resetDone'),
    url(r'^resetpassword/$', View_password.password_reset, name='resetPW'), #resetPW
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', View_password.password_reset_confirm,
    name='confirmReset'),
    url(r'^reset/done/$', View_password.password_reset_complete, name='resetComplete'),
)