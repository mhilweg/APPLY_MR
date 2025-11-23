# common.py

from otree.api import Page
from otree.api import BaseConstants
from otree.api import  models, widgets
import json

# %% Functions
def get_treatment_part(part, player):
    'returns the part of the treatment that is relevant for the player'
    'i.e. if treatment="T1_Math_men" and part=1, it returns "Math"'
    # print(player.participant.Treatment)
    return player.participant.Treatmentstring.split('_')[part]




    



# %% Constants
class CommonConstants(BaseConstants):
    Completion_fee = 3.50
    Max_Bonus = 10  

    Piece_rate = 0.05
    Tournament_rate1 = 4

    Recruiter_Treatments = {3, 4, 5, 8, 11, 12, 13, 16}

    
    # Prolific links:
    Completion_redirect = "https://www.wikipedia.org/" #TODO: adjust completion redirect
    Reject_redirect = "https://www.wikipedia.org/" #TODO: adjust reject redirect
    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust return redirect
    
    Instructions_Manager_MM_path = "_templates/global/Instructions_Manager_MM.html"
    Instructions_Manager_ER_path = "_templates/global/Instructions_Manager_ER.html"
    Selection_Instructions = "_templates/global/Selection_instructions_template.html"

    Task_instructions_path = "_templates/global/Task_instructions.html"
    Task_instructions_MM_path = "_templates/global/Task_instructions_MM.html"
    Task_instructions_ER_path = "_templates/global/Task_instructions_ER.html"

RECRUITER_TREATMENTS = set(CommonConstants.Recruiter_Treatments)

# %% Player
# DOESNT WORK WITH PLAYER

# %% Pages
class MyBasePage(Page):
    form_model = 'player'
    form_fields = ['blur_log', 'blur_count', 'blur_warned']


    @staticmethod
    def vars_for_template(player):
 # --- Instructions path logic (updated) ---
        # Use neutral instructions if treatment hides gender (1 or 9).





       # if player.participant.Gender == '':
        #    Instructions_path = CommonConstants.Instructions_female_path
        #elif player.participant.Gender == 'Male':
         #       Instructions_path = CommonConstants.Instructions_male_path
        #else: Instructions_path = CommonConstants.Instructions_female_path

        if player.participant.Treatment > 8:
            Task_path = CommonConstants.Task_instructions_ER_path
            Instructions_path = CommonConstants.Instructions_Manager_ER_path
        else:
            Task_path = CommonConstants.Task_instructions_MM_path
            Instructions_path = CommonConstants.Instructions_Manager_MM_path
        
        piece_rate = CommonConstants.Piece_rate
        tournament_rate1 = CommonConstants.Tournament_rate1 * piece_rate

        if player.participant.Blur_warned == 1:
            player.blur_warned = 1

        if player.participant.Treatment < 9:
            task = "Maths-Memory"
        else:
            task = "Emotion Recognition"
            

        return {
            'hidden_fields': ['blur_log', 'blur_count','blur_warned'],
            'Completion_fee': CommonConstants.Completion_fee,
            
            'Instructions_path': Instructions_path,
            'Task_path': Task_path,
            'Task_instructions': Task_path,
            'Selection_instructions': CommonConstants.Selection_Instructions,
            'MathMemory': get_treatment_part(1, player),
            'task': task,
            'Skill': get_treatment_part(1, player).lower(),

            'piece_rate': "{:.2f}".format(piece_rate),
            'tournament_rate1': "{:.2f}".format(tournament_rate1),

        }
        
        
                   

    @staticmethod
    def before_next_page(player, timeout_happened=False):
        blob = player.blur_log or '{}'
        page_counts = json.loads(blob)
        Blur_log = player.participant.vars.get('Blur_log', {})
        for page_name, count in page_counts.items():
            Blur_log[page_name] = Blur_log.get(page_name, 0) + count
        player.participant.vars['Blur_log'] = Blur_log
        player.participant.vars['Blur_count'] = (
            player.participant.vars.get('Blur_count', 0)
            + (player.blur_count or 0))
        
        # if player has been warned in this page, we set the flag and keep track of it, if not we keep the previous value
        # TODO: decide if you want the bonus to be determined based on the blur_warned flag, if so, adjust your bonus logic accordingly
        if player.blur_warned:
            player.participant.Blur_warned = 1
        
