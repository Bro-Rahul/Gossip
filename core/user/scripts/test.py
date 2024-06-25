from user.models import *

def run():
    user = User.objects.get(username = 'rahul')
    print(user)
    data = user.followers.all()
    print(data)
    info = [{'username' : User.objects.get(pk=user.follower_id).username }for user in data]
    print(info)
