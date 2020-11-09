from mycroft import MycroftSkill, intent_file_handler


class HslTracking(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tracking.hsl.intent')
    def handle_tracking_hsl(self, message):
        self.speak_dialog('tracking.hsl')


def create_skill():
    return HslTracking()

