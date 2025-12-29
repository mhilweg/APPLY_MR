from otree.api import *
import random
from django.utils.safestring import mark_safe
from common import *

doc = '''
This is the first app - the Introduction app. It contains
1. Demgraphics page
2. Instructions that participants can always access
3. Comprehension checks 
4. and the first attention checks
Following are saved to the participant level
- Allowed: if they didnt fail the comprehension checks
- Comprehension_passed: whether they passed the comprehension checks
- Attention_1: whether they passed the first attention check
- Treatment: which treatment they are assigned to
'''


def get_treatment_part(part, player):
    'returns the part of the treatment that is relevant for the player'
    'i.e. if treatment="T1_Math_men" and part=1, it returns "Math"'
    return player.participant.Treatmentstring.split('_')[part]


class C(CommonConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Round_length = 120  # change to 120
    Round_length_min = int(Round_length / 60)
    Timer_text = "Time left to complete this round:"

    # Treatment quotas. This will be copied to the session variable.
    MathMemory_pic = 'https://raw.githubusercontent.com/argunaman2022/stereotypes-replication2/master/_static/pics/MathMemory_pic.png'

    TOTAL_QUOTAS = {  # For 1,2,9,10 (both genders)
        '2_M_N_N_N': 400,
        #'2_M_Y_N_N': 0,
        #'9_E_N_N_N': 0,
        '10_E_Y_N_N': 400,
    }
    QUOTA_4 = {  # T4 men only
        '4_M_Y_YM_M': 0,
    }


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    session = subsession.session

    # Only initialize on round 1
    if subsession.round_number == 1:
        session.Total_quotas = {k: 0 for k in C.TOTAL_QUOTAS}
        session.Quota_4 = {k: 0 for k in C.QUOTA_4}

    for player in subsession.get_players():
        player.Allowed = True
        player.participant.Promised = True
        player.participant.Comprehension_passed = False
        player.participant.Attention_passed = True
        player.participant.Blur_warned = 0
        player.participant.payrule_version = 0

        # create and save Group_members to the participant variable


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.IntegerField()
    # Demographics
    # prolific_id = models.StringField(default=str("None")) #prolific id, will be fetched automatically.
    gender = models.StringField(label='What is your gender identity?',
                                choices=['Male', 'Female', 'Other', 'Rather not say'], widget=widgets.RadioSelect)
    age = models.IntegerField(label='How old are you?', min=18, max=99)
    country = models.StringField(label='In which country do you live?')
    job = models.StringField(label='What is your employment status?',
                             choices=['Unemployed', 'Part-time', 'Full-time', 'Student', 'Retired', 'Other'],
                             widget=widgets.RadioSelect)

    Bot = models.IntegerField(initial=0)

    Comprehension_password = models.StringField(blank=False,
                                                label='Password')

    browser = models.StringField(
        label='Please enter your browser name and version (e.g. Chrome 100.0.4896.127)',
        blank=True,
    )
    Allowed = models.IntegerField(initial=1)

    Piece_rate = models.IntegerField(initial=0)  # correct answers
    Piece_rate_Attempts = models.IntegerField(initial=0,
                                              blank=True)  # logs the number of attempts in the math memory game
    ai_catch_answer = models.StringField(blank=True, max_length=4)
    honeypot = models.StringField(
        label='Please enter your browser name and version (e.g. Chrome 100.0.4896.127)',
        blank=True,
    )
    mouse_data = models.LongStringField(blank=True)

    # Store card orders for Round 1
    R1_easy_card_order = models.LongStringField(blank=True)
    R1_hard_card_order = models.LongStringField(blank=True)

    # Store breakdown scores
    R1_easy_score = models.IntegerField(initial=0)
    R1_hard_score = models.IntegerField(initial=0)
    R1_easy_attempts = models.IntegerField(initial=0)
    R1_hard_attempts = models.IntegerField(initial=0)

    # data quality
    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)


# %% Functions
def treatment_assignment(player):
    session = player.subsession.session

    # Initialize if missing
    if not hasattr(session, 'Total_quotas'):
        session.Total_quotas = {C.TOTAL_QUOTAS}  # Merge all
    if not hasattr(session, 'Quota_4'):
        session.Quota_4 = {k: 0 for k in C.QUOTA_4}

    quotas = session.Total_quotas
    max_quotas = C.TOTAL_QUOTAS
    quota4 = session.Quota_4
    max_quota4 = C.QUOTA_4

    print(f"DEBUG: gender={player.gender}, quota4={quota4}")

    # **MEN: T4 priority until full**
    if player.gender == 'Male' and quota4['4_M_Y_YM_M'] < max_quota4['4_M_Y_YM_M']:
        treatment = '4_M_Y_YM_M'
        session.Quota_4['4_M_Y_YM_M'] += 1  # ✅ WRITE BACK
        print("DEBUG: Male -> T4 (priority)")

    # **EVERYONE ELSE: randomize 1,2,9,10 only**
    else:
        available = [t for t in C.TOTAL_QUOTAS if quotas[t] < max_quotas[t]]
        if not available:
            player.Allowed = 0
            return
        treatment = random.choice(available)
        session.Total_quotas[treatment] += 1  # ✅ WRITE BACK
        print(f"DEBUG: Randomized to {treatment}, available={available}")

    # COMMIT
    player.participant.vars['Treatmentstring'] = treatment
    player.participant.vars['Gender'] = player.gender
    session.Total_quotas = quotas  # Ensure write-back

    print(f"DEBUG: New quotas: T4={session.Quota_4}, others={session.Total_quotas}")


# %% Pages

# Consent, Demographics, Introduction, Comprehension checks and attention check 1
class Welcome(Page):
    pass


class AI_catch(Page):
    form_model = 'player'
    form_fields = ['ai_catch_answer', 'honeypot', 'mouse_data']

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1

    @staticmethod
    def error_message(player, values):
        # Normalize: strip spaces and uppercase
        entered = (values.get('ai_catch_answer') or '').replace(' ', '').upper()
        if entered != 'A8F':
            return 'That entry does not match. Please type the 3 characters you see.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):

        if player.honeypot != "":
            player.Allowed = 0
            player.Bot = 1


class Aboutyou(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'age',
        'country',
        'job',
        'blur_log',
        'blur_count',
        'blur_warned',
        'browser'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1

    @staticmethod
    def vars_for_template(player: Player):

        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned', 'browser'],
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        if player.gender in ['Other', 'Rather not say']:
            player.Allowed = 0
        else:
            treatment_assignment(player)  # Assign treatment and update quotas
            # Ensure Treatmentstring is set before calling get_treatment_part
            if player.Allowed == 1:
                player.participant.Treatment = int(get_treatment_part(0, player))
                player.treatment = int(get_treatment_part(0, player))


class Instructions(MyBasePage):

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1


class Round_1_instructions(MyBasePage):

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1


class Round_1_begin(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1


class Round_1_play_easy(MyBasePage):
    extra_fields = ['Piece_rate', 'Piece_rate_Attempts', 'R1_easy_card_order']
    form_fields = MyBasePage.form_fields + extra_fields

    timeout_seconds = C.Round_length / 2  # set to 60 later
    timer_text = C.Timer_text

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        for _ in ['Piece_rate', 'Piece_rate_Attempts', 'R1_easy_card_order']:
            variables['hidden_fields'].append(_)
        return variables

    @staticmethod
    def js_vars(player: Player):
        # Start from zero on the first (easy) minute
        return {
            'field_name': 'Piece_rate',
            'treatment_num': player.participant.Treatment,
            'round_index': 1,
            'mix': None,
            'phase': 'easy',  # NEW
            'start_value': 0,  # NEW: matches carried-in ImgFound
            'attempts_start': 0,  # NEW
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        MyBasePage.before_next_page(player, timeout_happened)
        # park the easy minute results to participant vars
        player.participant.vars['R1_easy'] = player.Piece_rate
        player.participant.vars['R1_easy_attempts'] = player.Piece_rate_Attempts


class Round_1_Transition(MyBasePage):

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1


class Round_1_play_hard(MyBasePage):
    extra_fields = ['Piece_rate', 'Piece_rate_Attempts', 'R1_hard_card_order']
    form_fields = MyBasePage.form_fields + extra_fields

    timeout_seconds = C.Round_length / 2  # set to 60 later
    timer_text = C.Timer_text

    @staticmethod
    def is_displayed(player: Player):
        return player.Allowed == 1

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        for _ in ['Piece_rate', 'Piece_rate_Attempts', 'R1_hard_card_order']:
            variables['hidden_fields'].append(_)
        return variables

    @staticmethod
    def js_vars(player: Player):
        # Continue from where the easy minute stopped
        r1_easy = player.participant.vars.get('R1_easy', 0)
        r1_easy_att = player.participant.vars.get('R1_easy_attempts', 0)
        return {
            'field_name': 'Piece_rate',
            'treatment_num': player.participant.Treatment,
            'round_index': 1,
            'mix': None,
            'phase': 'hard',  # NEW
            'start_value': r1_easy,  # NEW
            'attempts_start': r1_easy_att,  # NEW
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        MyBasePage.before_next_page(player, timeout_happened)
        r1_easy = player.participant.vars.get('R1_easy', 0)
        r1_easy_att = player.participant.vars.get('R1_easy_attempts', 0)

        # Store breakdown scores in Player model for database
        player.R1_easy_score = r1_easy
        player.R1_hard_score = player.Piece_rate - r1_easy
        player.R1_easy_attempts = r1_easy_att
        player.R1_hard_attempts = player.Piece_rate_Attempts - r1_easy_att

        # Store in participant vars (for display)
        player.participant.vars['R1_hard'] = player.R1_hard_score
        player.participant.vars['R1_hard_attempts'] = player.R1_hard_attempts

        # Store total score
        player.participant.R1_score = player.Piece_rate


class Practice_Score(MyBasePage):
    pass


class ScreenOut(Page):

    @staticmethod
    def is_displayed(player):
        return player.Allowed == 0 and player.Bot == 0


class RejectBot(Page):

    @staticmethod
    def is_displayed(player):
        return player.Allowed == 0 and player.Bot == 1


class RedirectScreenOut(Page):

    @staticmethod
    def is_displayed(player):
        return player.Allowed == 0 and player.Bot == 0

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkscreenout=
            player.subsession.session.config['completionlinkscreenout']
        )


class RedirectBot(Page):

    @staticmethod
    def is_displayed(player):
        return player.Allowed == 0 and player.Bot == 0

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkbot=
            player.subsession.session.config['completionlinkbot']
        )


# TBU !


page_sequence = [Welcome,
                 AI_catch,
                 Aboutyou,
                 Instructions,
                 Round_1_instructions,
                 Round_1_begin,
                 Round_1_play_easy,
                 Round_1_Transition,
                 Round_1_play_hard,
                 Practice_Score,
                 ScreenOut,
                 RejectBot,
                 RedirectScreenOut,
                 RedirectBot
                 ]