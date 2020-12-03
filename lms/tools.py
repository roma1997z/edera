from lms.models import InterestKey, Interest, InterestUser


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