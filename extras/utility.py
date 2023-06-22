class UtilityManager:

    def __init__(self, request):
        self.request = request

    def get_or_create_session(self):
        the_session = None
        the_session = self.request.session.session_key
        if not the_session:
            the_session = self.request.session.create()
        return the_session
