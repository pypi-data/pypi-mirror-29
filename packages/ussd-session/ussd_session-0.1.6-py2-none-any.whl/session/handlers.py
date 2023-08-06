from session.models import Session

class SessionHandler:
    def __init__(self, session_id):
        self.session_id = session_id

    def get_or_create(self, **kwargs):
        return Session.objects.get_or_create(
            session_id=self.session_id,
            defaults=kwargs
        )

    def set_init_message(self, message):
        session = self.get_or_create()[0]
        session.initiation_message = message
        session.save()

    def get_init_message(self):
        return self.get_or_create()[0].initiation_message

    def set_method_and_action(self, method, action=None):
        session = self.get_or_create()[0]
        session.method = method
        if action:
            session.action = action
        session.save()

    def set_success(self):
        session = self.get_or_create()[0]
        session.succeeded = True
        session.save()

    def set_menu_option(self, option):
        session = self.get_or_create()[0]
        session.menu_option = option
        session.save()

    def get_menu_option(self):
        return self.get_or_create()[0].menu_option

    def set_sequence_at_menu(self, seq):
        session = self.get_or_create()[0]
        session.sequence_at_menu = seq
        session.save()

    def get_sequence_at_menu(self):
        return self.get_or_create()[0].sequence_at_menu

    def set_step_at_paged(self, step):
        session = self.get_or_create()[0]
        session.step_at_paged = step
        session.save()

    def get_step_at_paged(self):
        return self.get_or_create()[0].step_at_paged

    def set_page_stop(self, stop):
        session = self.get_or_create()[0]
        session.page_stop = stop
        session.save()

    def get_page_stop(self):
        return self.get_or_create()[0].page_stop

    def set_selector(self, selector):
        session = self.get_or_create()[0]
        session.selector = selector
        session.save()

    def get_selector(self):
        return self.get_or_create()[0].selector