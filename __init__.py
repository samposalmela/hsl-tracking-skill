# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import requests
import datetime

__author__ = 'samposalmela'

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
{
  stop(id: "HSL:4610237") {
    name
      stoptimesWithoutPatterns {
      scheduledArrival
      realtimeArrival
      arrivalDelay
      scheduledDeparture
      realtimeDeparture
      departureDelay
      realtime
      realtimeState
      serviceDay
      headsign
    }
  }  
}
"""

class HslSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super(HslSkill, self).__init__(name='HslSkill')
        #self.learning = True

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        #my_setting = self.settings.get('my_setting')
        self.load_data_files(dirname(__file__))

    @intent_handler(IntentBuilder('NextBusIntent').require('NextBusKeyword'))
    def next_bus_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        result = run_query(query) # Execute the query
        json_output = result # Drill down the dictionary
        output = json_output['data']

        stop = output['stop']
        times = stop['stoptimesWithoutPatterns']

        #3 seuraavaa bussia
        next = times[0]
        # after = times[1]
        # last = times [2]


        #muuttaa sekunnit kellon ajaksi
        conversion = datetime.timedelta(seconds=next['realtimeArrival'])
        arrival_time = str(conversion)
        headsign = next['headsign']

        # conversion = datetime.timedelta(seconds=after['realtimeArrival'])
        # arrival_time2 = str(conversion)

        # conversion = datetime.timedelta(seconds=last['realtimeArrival'])
        # arrival_time3 = str(conversion)

        #printtaa 3 seuraavaa bussia
        # print(arrival_time,next['headsign'])
        # print(arrival_time2,after['headsign'])
        # print(arrival_time3,last['headsign'])

       
        self.speak_dialog("Next bus leaves at {} {}".format(arrival_time, headsign))

    # @intent_handler('HowAreYou.intent')
    # def handle_how_are_you_intent(self, message):
    #     """ This is a Padatious intent handler.
    #     It is triggered using a list of sample phrases."""
    #     self.speak_dialog("how.are.you")

    # @intent_handler(IntentBuilder('HelloWorldIntent')
    #                 .require('HelloWorldKeyword'))
    # def handle_hello_world_intent(self, message):
    #     """ Skills can log useful information. These will appear in the CLI and
    #     the skills.log file."""
    #     self.log.info("There are five types of log messages: "
    #                   "info, debug, warning, error, and exception.")
    #     self.speak_dialog("hello.world")



    def stop(self):
        pass


def create_skill():
    return HslSkill()
