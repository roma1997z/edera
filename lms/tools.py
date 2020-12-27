from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

from lms.models import InterestKey, Interest, InterestUser, TeacherTime, Lesson
import datetime
import portion as P

def get_interest_json():
    # for interest filtering
    interests = []
    interest_key = InterestKey.objects.filter(active=True)
    for key in interest_key:
        key_interests = Interest.objects.filter(active=True, key=key).values("note_id", "name")
        interests.append({"name": key.name, "key_id": key.note_id, "options": key_interests})
    return interests


def set_interest(interests, user_id):
    """

    :param interests: list of interest ids
    :param user_id: user to change interests
    :return:
    """
    iu = InterestUser.objects.filter(user_id=user_id)
    iu.delete()
    for el in interests:
        iu = InterestUser(user_id=user_id, interest=Interest.objects.get(note_id=int(el)))
        iu.save()
    return 0


def get_teacher_time(teacher):
    tt = []
    for day in range(7):
        tt.append(TeacherTime.objects.filter(teacher=teacher, day=day))
    return tt


def can_edit_teacher_profile(user):
    if user.profile.moderator:
        return True
    else:
        return False


def get_moder_user(request, user_id):
    context = {}
    if user_id is not None:
        theuser = User.objects.get(id=user_id)
        context["moderator"] = True
        context["id"] = user_id
        if not can_edit_teacher_profile(request.user):
            return HttpResponseForbidden("Only moderators can access this page")
    else:
        theuser = request.user
    return context, theuser


def get_free_teacher_time(teacher, day, raw=True):

    tt = list(TeacherTime.objects.filter(day=day,
                                         teacher=teacher).order_by("start_time").values_list("start_time", "end_time"))
    t = P.empty()

    for start_time, end_time in tt:
        print(start_time)
        t = t | P.closed(to_min(start_time), to_min(end_time))

    ls = list(Lesson.objects.filter(teacher=teacher, day=day, active__gt=0).values_list("start_time", "end_time"))
    for start_time, end_time in ls:
        t = t - P.closed(to_min(start_time), to_min(end_time))
    return list(t)


def to_min(time):
    return time.hour*60+time.minute


def min_to_time(mins):
    return "{:02d}:{:02d}".format(mins // 60, mins % 60, 0)


def to_time(point, step, duration=0):
    mins = point*step+duration
    return min_to_time(mins)