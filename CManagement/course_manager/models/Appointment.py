from django.db import models
from course_manager.models.Course import Course
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Users.Participant import Participant


class Appointment(models.Model):
    """
        stores information's about a specific appointment \n

        about parameters:
        -----------------

        - **current_count_of_participants:**
            + shows the number of participants actually joined the course
            + integer value
            + *default:* 0

        - **my_course:**
            + the course the appointment is assigned

        - **my_tutor:**
            + the tutor(s) are assigned to the appointment

        - **my_participants:**
            + participants assigned to this appointment

        - **weekday:**
            + keep the name of a weekday the appointment is
            + its a string with maximum length of ten, not proofed that it is a real name of a weekday
            + *default:* 'Monday'

        - **lesson:**
            + describes the time of appointment in the time plan of the TU Dresden (double periods = DS)
            + its a string with maximum length of ten, not proofed by any rules
            + *default:* '1. DS' -> means first double period 7.30 am - 9.00 am

        - **location:**
            + keeps information's about the room where the appointment is
            + its a string with maximum length ot 30, not proofed by any rules
            + *default:* not set

        - **attandance:**
            + is the count of maximum participants they can join this specific course
            + integer value
            + *default:* 15

        - **is_visible:**
            + after an executive has created a new course with its appointments he can choose to hide this information
             on the screen where a potential participant can look for it
            + *default:* True

        - **additional_information:**
            + keeps information's for more details
            + its a string with a maximum length of 200, not proofed by any rules
            + *default:* not set

    """

    class Meta:
        app_label = 'course_manager'

    __version__ = "$Revision$"
    # $Source$

    current_count_of_participants = models.IntegerField(default=0)
    my_course = models.ForeignKey(Course)
    my_tutors = models.ManyToManyField(Tutor, blank=True)
    my_participants = models.ManyToManyField(Participant, blank=True)
    weekday = models.CharField(max_length=10, default="Monday")
    lesson = models.CharField(max_length=10, default="1.DS")
    location = models.CharField(max_length=30)
    attendance = models.IntegerField(default=15)
    is_visible = models.BooleanField(default=True)
    additional_information = models.CharField(max_length=200, blank=True)

    def __str__(self):
        """
        returns a string that contains the weekday, the time (in DS) and the location of the appointment
        """
        return self.weekday+", "+self.lesson+",  "+self.location

    def add_tutor(self, tutor):
        """
        add a (additional) tutor to the appointment
        - **input:**
            + *tutor*: must be a instance of class Tutor, affiliation is checked

        \todo: implement True or False ?
        """

        if not tutor:
            print("app: no tutor to add")
            return

        self.my_tutors.add(tutor)
        print("app: tutor added successfully")

    def remove_tutor(self, tutor):
        """
        removes a specified tutor from the list of tutors ('self.my_tutor') for this appointment
        - **input:**
            + *tutor*: must be a instance of class Tutor, affiliation is checked
            + 'tutor.username' must be identical for successfully erasing

        \todo: implement True or False ?
        """

        if not tutor:
            return
        mylist = self.my_tutors.all()
        len(mylist)
        self.my_tutors = []
        self.save()
        for t in mylist:
            if t.username != tutor.username:
                self.my_tutors.add(t)
        self.save()


    def add_participant(self, part):
        """
        add a participant to the list of participants ('self.my_participants'),
        if the maximum number of participants ('self.attendance') is reached an addition to the list is not possible
        - **input:**
            + *part*: must be a instance of class Participant, affiliation is checked

        \todo: implement True or False ?
        """
        if not part:
            print("app: no participant to add")
            return

        if self.my_participants.all().count() >= self.attendance:
            print("app: maximum number of participants reached")
            return

        for p in self.my_participants.all():
            if p.username == part.username:
                print("app: participant already signed in")
                return

        self.my_participants.add(part)
        self.current_count_of_participants = self.my_participants.all().count()
        print("app: participant added successfully")

    def remove_participant(self, part):
        """
        removes a specified participant from the list ('self.my_participants')
        - **input:**
            + *part*: must be a instance of class Participant, affiliation is checked
            + 'participant.username' must be identical for successfully erasing

        \todo: implement True or False ?
        """
        if not part:
            return
        mylist = self.my_participants.all()
        len(mylist)
        self.my_participants = []
        self.save()
        for p in mylist:
            if p.username != part.username:
                self.my_participants.add(p)
        self.current_count_of_participants = self.my_participants.all().count()
        self.save()