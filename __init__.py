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

        next = times[0]
      
        conversion = datetime.timedelta(seconds=next['realtimeArrival'])
        arrival_time = str(conversion)
        headsign = next['headsign']

        self.speak_dialog("Next bus leaves at {} destination {}".format(arrival_time, headsign))
    
    @intent_handler(IntentBuilder().require('NextBusKeyword').require('AfterBusKeyword'))
    def after_bus_intent(self, message):
        result = run_query(query) # Execute the query
        json_output = result # Drill down the dictionary
        output = json_output['data']

        stop = output['stop']
        times = stop['stoptimesWithoutPatterns']

        second = times[1]

        conversion = datetime.timedelta(seconds=second['realtimeArrival'])
        arrival_time2 = str(conversion)

        headsign = second['headsign']

        after = message.data.get('AfterBusIntent')
        self.speak("Bus after that leaves at {} destination {}".format(arrival_time2, headsign))
        self.set_context('AfterBusIntent', after)
        


    @intent_handler(IntentBuilder('SecondBusIntent').require('SecondBusKeyword'))
    def second_bus_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        result = run_query(query) # Execute the query
        json_output = result # Drill down the dictionary
        output = json_output['data']

        stop = output['stop']
        times = stop['stoptimesWithoutPatterns']

        second = times[1]

        conversion = datetime.timedelta(seconds=second['realtimeArrival'])
        arrival_time2 = str(conversion)

        headsign = second['headsign']

        self.speak_dialog("Second bus leaves at {} destination {}".format(arrival_time2, headsign))

    @intent_handler(IntentBuilder('ThirdBusIntent').require('ThirdBusKeyword'))
    def third_bus_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        result = run_query(query) # Execute the query
        json_output = result # Drill down the dictionary
        output = json_output['data']

        stop = output['stop']
        times = stop['stoptimesWithoutPatterns']

        third = times[2]

        conversion = datetime.timedelta(seconds=third['realtimeArrival'])
        arrival_time3 = str(conversion)

        headsign = third['headsign']

        self.speak_dialog("Third bus leaves at {} destination {}".format(arrival_time3, headsign))

    @intent_handler(IntentBuilder('NextThreeIntent').require('NextThreeKeyword'))
    def next_three_busses_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        result = run_query(query) # Execute the query
        json_output = result # Drill down the dictionary
        output = json_output['data']

        stop = output['stop']
        times = stop['stoptimesWithoutPatterns']

        next = times[0]
        second = times[1]
        third = times[2]

        conversion = datetime.timedelta(seconds=next['realtimeArrival'])
        conversion = datetime.timedelta(seconds=second['realtimeArrival'])
        conversion = datetime.timedelta(seconds=third['realtimeArrival'])
        arrival_time1 = str(conversion)
        arrival_time2 = str(conversion)
        arrival_time3 = str(conversion)

        headsign1 = next['headsign']
        headsign2 = second['headsign']
        headsign3 = third['headsign']

        self.speak_dialog("Next three busses are {} destination {}, {} destination {}, and {} destination {}".format(arrival_time1, headsign1,arrival_time2, headsign2,arrival_time3, headsign3))

    def stop(self):
        pass


def create_skill():
    return HslSkill()
