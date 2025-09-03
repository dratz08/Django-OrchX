from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class RegisterAnonRateThrottle(AnonRateThrottle):
    rate = '4/day'


class BotCreateUserRateThrottle(UserRateThrottle):
    rate = '10/day'