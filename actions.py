# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Dict, List, Text, Union, Optional

from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)


class UserForm(FormAction):
    """Collects user information and adds it to the spreadsheet"""

    def name(self) -> Text:
        return "user_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "person_name",
            "college",
            "purpose",
            "email",
            "question",
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "person_name": [
                self.from_entity(entity="name"),
                self.from_text(intent="enter_data"),
            ],
            "college": [
                self.from_entity(entity="college"),
                self.from_text(intent="enter_data"),
            ],
            "purpose": [
                self.from_entity(entity="purpose"),
                self.from_text(intent="enter_data"),
            ],
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
            ],
            "question": [
                self.from_entity(entity="question"),
                self.from_text(intent="enter_data"),
            ],
        }

    def validate_business_email(
        self, value, dispatcher, tracker, domain
    ) -> Dict[Text, Any]:
        """Check to see if an email entity was actually picked up by duckling."""

        if any(tracker.get_latest_entity_values("email")):
            # entity was picked up, validate slot
            return {"email": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_message(template="utter_no_email")
            return {"business_email": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        college = tracker.get_slot("college")
        email = tracker.get_slot("email")
        person_name = tracker.get_slot("person_name")
        purpose = tracker.get_slot("purpose")
        question = tracker.get_slot("question")

        fout = open('user_data/user_data.csv', 'a')
        fout.write('\n'+person_name+','+college+','+email+','+purpose+','+question)    
        fout.close()
        dispatcher.utter_message(text="Great! Our team will get in touch with you as soon as possible over email.")
        return []

class NavigationForm(FormAction):
    """Collects information from user about where he wants to navigate to and returns a google maps link to the place"""

    def name(self) -> Text:
        return "navigation_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "destination_place",
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "destination_place": [
                self.from_entity(entity="destination_place"),
                self.from_text(intent="enter_data"),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        destination_place = tracker.get_slot("destination_place")
        destination_place = str(destination_place)
        destination_place = destination_place.replace(" ","+")
        string = "Okay! Here is a google maps search to your destination: https://www.google.com/maps/search/" + destination_place + "+nit+trichy"
        dispatcher.utter_message(text=string)
        return []

# class ActionRestarted(Action):  
#     def name(self):         
#         return 'action_restarted'   
#     def run(self, dispatcher, tracker, domain): 
#         return[Restarted()] 

# class ActionSlotReset(Action):  
#     def name(self):         
#         return 'action_slot_reset'  
#     def run(self, dispatcher, tracker, domain):         
#         return[AllSlotsReset()]