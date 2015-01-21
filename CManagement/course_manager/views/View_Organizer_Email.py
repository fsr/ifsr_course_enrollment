from django.contrib.auth.decorators import login_required
from course_manager.models.Course import Course
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Users.User import UserAccount
from course_manager.models.Appointment import Appointment
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError, send_mass_mail
from smtplib import SMTPException
from django.contrib.auth import logout


@login_required
def show_form_email(request, recipient_id):
    """
    This view shows an E-Mail form for a single recipient.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param recipient_id: the database id of the recipient user
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        recipient = get_object_or_404(UserAccount, pk=recipient_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    tutors_list = Tutor.objects.order_by('-date_joined')
    latest_courses_list = Course.objects.order_by('-name')

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'recipient': recipient,
               'mass_email': False}
    return render(request, 'cmanagement/message.html', context)


@login_required
def send_email(request, recipient_id):
    """
    This view processes POST data provided by an E-Mail form.\n
    The message will be send to a single recipient.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param recipient_id: the database id of the recipient user
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        recipient = get_object_or_404(UserAccount, pk=recipient_id)
    except Http404:
        return HttpResponseRedirect('cmanagement:newEmailFormOrga', args=[recipient_id])
    else:
        pass

    message = request.POST.get('InputMessage', '')
    subject = "Mail from "+request.user.username+" to "+recipient.username
    from_email = request.user.email
    recipient = recipient.email

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [recipient])
        except BadHeaderError:
            return HttpResponseRedirect('cmanagement:newEmailFormOrga', args=[recipient_id])
        else:
            return HttpResponseRedirect(reverse('cmanagement:noteMailSuccOrga'))
    else:
        return HttpResponseRedirect('cmanagement:newEmailFormOrga', args=[recipient_id])


@login_required
def show_form_email_to_course(request, course_id):
    """
    This view shows an E-Mail form.\n
    The written message will be send to all participants enrolled to\n
    appointments which are associated with the selected course.\n

    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: the database id of the selected course
    :return: rendered page or HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        the_course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:exec'))
    else:
        pass

    tutors_list = Tutor.objects.order_by('-date_joined')
    latest_courses_list = Course.objects.order_by('-name')

    context = {'tutors_list': tutors_list,
               'latest_courses_list': latest_courses_list,
               'recipient': the_course,
               'mass_email': True}
    return render(request, 'cmanagement/message.html', context)


@login_required
def send_email_to_course(request, course_id):
    """
    This view processes POST data provided by an E-Mail form.\n
    The message will be send to all participants enrolled to\n
    appointments which are associated with the selected course.\n
    \n*login required*\n
    For security reasons we check the user's group association once more\n
    and redirect if necessary.\n

    :param request: the incoming request
    :param course_id: the database id of the selected course
    :return: HttpResponseRedirect()
    """

    # <SECURITY_BLOCK>
    # check user groups for Tutor or Organizer membership (in hierarchical order)
    if not request.user or not request.user.is_active:
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    elif request.user.groups.filter(name="Organizers").count() is not 0:
        # everything is fine, proceed to organizer's view
        pass
    elif request.user.groups.filter(name="Tutors").count() is not 0:
        # redirect to tutor view
        return HttpResponseRedirect(reverse('cmanagement:tut'))
    else:
        # strange membership, redirect to login page
        logout(request)
        return HttpResponseRedirect(reverse('cmanagement:newLoginForm'))
    # </SECURITY_BLOCK>

    try:
        the_course = get_object_or_404(Course, pk=course_id)
    except Http404:
        return HttpResponseRedirect(reverse('cmanagement:newMEmailFormOrga', args=[course_id]))
    else:
        pass

    message = request.POST.get('message', '')
    subject = "Mail from "+request.user.username+" to course: "+the_course.name
    from_email = "ifsrcourses@gmail.com"

    recipient_list = []
    for app in Appointment.objects.all():
        if app.my_course == the_course:
            for part in app.my_participants.all():
                recipient_list.append(part.email)

    print(subject, message)
    print(recipient_list)

    if subject and message and from_email:
        try:
            data_tuple = (subject, message, from_email, recipient_list)
            send_mass_mail((data_tuple,))
        except BadHeaderError:
            return HttpResponseRedirect(reverse('cmanagement:newMEmailFormOrga', args=[course_id]))
        except SMTPException:
            return HttpResponseRedirect(reverse('cmanagement:newMEmailFormOrga', args=[course_id]))
        else:
            return HttpResponseRedirect(reverse('cmanagement:noteMailSuccOrga'))
    else:
        return HttpResponseRedirect(reverse('cmanagement:newMEmailFormOrga', args=[course_id]))