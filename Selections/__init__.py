from otree.api import *
import random
import numpy as np
import pandas as pd
import time
from common import *

doc = '''
This is the main survey app. It contains
'''


# %%Functions

# %%

class C(CommonConstants):
    NAME_IN_URL = 'Main_part'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PIECE_RATE = 0.05

    Round_length = 120  # TODO: reduce to 120 seconds
    Min_round_length = Round_length
    Timer_text = "Time left to complete this round:"

    Calculator_path = "_templates/global/Calculator.html"

    Instructions_choice_path = "_templates/global/Instructions_choice.html"
    Instructions_choice_past_path = "_templates/global/Instructions_choice_past.html"
    Instructions_choice_2_path = "_templates/global/Instructions_choice_2.html"

    MathMemory_pic = 'https://raw.githubusercontent.com/argunaman2022/stereotypes-replication2/master/_static/pics/MathMemory_pic.png'

    Belief_Treatment_male = "_templates/global/Belief_treatment_male.html"
    Belief_Treatment_female = "_templates/global/Belief_treatment_female.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Timer
    page_pass_time = models.FloatField()

    ## Group
    Gender = models.StringField()

    # Player answers
    ## Data quality

    ## Main
    Round2_Mix = models.IntegerField(
        choices=[
            [1, 'Easy Mix'],
            [2, 'Hard Mix']
        ]
    )

    incentivised_selection = models.IntegerField()
    SelectionLine1 = models.IntegerField()
    Selection1 = models.IntegerField()
    Selection1_id = models.LongStringField()

    SelectionLine2 = models.IntegerField()
    Selection2 = models.IntegerField()
    Selection2_id = models.LongStringField()

    SelectionLine3 = models.IntegerField()
    Selection3 = models.IntegerField()
    Selection3_id = models.LongStringField()

    SelectionLine4 = models.IntegerField()
    Selection4 = models.IntegerField()
    Selection4_id = models.LongStringField()

    SelectionLine5 = models.IntegerField()
    Selection5 = models.IntegerField()
    Selection5_id = models.LongStringField()

    treatment = models.IntegerField()
    bonus = models.IntegerField(initial=0)
    moved_to_selection = models.IntegerField(initial=0)
    assigned_id = models.IntegerField()

    Round2 = models.IntegerField(initial=0)  # correct answers
    Round2_Attempts = models.IntegerField(initial=0, blank=True)  # logs the number of attempts in the math memory game
    Round3 = models.IntegerField(initial=0)  # correct answers
    Round3_Attempts = models.IntegerField(initial=0, blank=True)  # logs the number of attempts in the math memory game

    Choice = models.IntegerField(
        choices=[
            [1, 'Payment Rule A'],
            [2, 'Payment Rule B']
        ],
        label='R3 Payment Rule Choice'
    )  #

    # Comprehension check question

    # In class Player:

    CQ1 = models.IntegerField(
        choices=[
            [1, 'Mix 1 only'],
            [2, 'Mix 2 only'],
            [3, 'Either Mix 1 or Mix 2'],
        ],
        label='In round 1, which mix could a participant have received?',
        widget=widgets.RadioSelect
    )
    CQ1_incorrect = models.IntegerField(initial=0)
    CQ1_incorrect2 = models.IntegerField(initial=0)

    CQ2 = models.IntegerField(
        choices=[
            [1, 'Yes, I will see which mix each participant received'],
            [2, 'No, I will only see their round 1 score'],
        ],
        label='Will you know which mix (Mix 1 or Mix 2) each participant received in round 1?',
        widget=widgets.RadioSelect
    )
    CQ2_incorrect = models.IntegerField(initial=0)
    CQ2_incorrect2 = models.IntegerField(initial=0)

    CQ3 = models.IntegerField(
        choices=[
            [1, 'Only easy pairs'],
            [2, 'Only hard pairs'],
            [3, 'Either Mix 1 or Mix 2'],
        ],
        label='In round 2, what type of pairs will all participants face?',
        widget=widgets.RadioSelect
    )
    CQ3_incorrect = models.IntegerField(initial=0)
    CQ3_incorrect2 = models.IntegerField(initial=0)

    cq_page_2 = models.IntegerField(initial=0)

    Comprehension_password = models.StringField(blank=False,
                                                label='Password')




    # clicked info
    clicked_info = models.StringField(initial=False)
    # Choice stage choices
    Calculator = models.StringField(min=0, max=100, blank=True, label='Calculator' )


    # data quality
    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)



# %% Base Pages
# class MyBasePage(MyBasePageCommon):

#     @staticmethod
#     def vars_for_template(player: Player):
#         variables = MyBasePage.vars_for_template(player)

#         if player.participant.Gender == 'Male':
#                 Instructions_path = C.Instructions_male_path
#         else: Instructions_path = C.Instructions_female_path

#         variables['Instructions_path'] = Instructions_path
#         variables['Task_instructions'] = C.Task_instructions_path
#         variables['MathMemory'] = get_treatment_part(1, player)
#         variables['Skill'] = get_treatment_part(1, player)
#         variables['MathMemory'] = get_treatment_part(1, player).lower()
#         variables['SOB'] = get_treatment_part(2, player)

#         variables['Tournament_rate_cents'] = int(C.Tournament_rate*100)
#         variables['Piece_rate_cents'] = int(C.Piece_rate*100)


#         return variables


# %% Pages


'R2: Tournament stage'


class Selection_instructions(MyBasePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.treatment = player.participant.Treatment
        player.page_pass_time = time.time() + C.Min_round_length

        mix_draw = random.randint(1, 2)
        player.Round2_Mix = mix_draw
        player.participant.R2_mix = mix_draw

        player.incentivised_selection = random.randint(1,5)
        player.participant.incentivised_selection = player.incentivised_selection


class Comprehension_Qs(MyBasePage):
    extra_fields = ['CQ1', 'CQ2', 'CQ3']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        MyBasePage.before_next_page(player, timeout_happened)

        if player.CQ1 != 3:
            player.CQ1_incorrect = 1
            player.CQ1 = 0

        if player.CQ2 != 2:
            player.CQ2_incorrect = 1
            player.CQ2 = 0

        if player.CQ3 != 2:
            player.CQ3_incorrect = 1
            player.CQ3 = 0

        incorrect_index = (player.CQ1_incorrect + player.CQ2_incorrect +
                          player.CQ3_incorrect)
        if incorrect_index > 0:
            player.cq_page_2 = 1

class Comprehension_Qs2(MyBasePage):
    extra_fields = ['CQ1', 'CQ2', 'CQ3']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def is_displayed(player: Player):
        return player.cq_page_2 == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        MyBasePage.before_next_page(player, timeout_happened)

        if player.CQ1 != 3:
            player.CQ1_incorrect2 = 1

        if player.CQ2 != 2:
            player.CQ2_incorrect2 = 1

        if player.CQ3 != 2:
            player.CQ3_incorrect2 = 1

class SelectionsBegin(MyBasePage):

    @staticmethod
    def before_next_page(player, timeout_happened):


        session_players = player.subsession.get_players()

        same_treatment_passed_count = 0
        for p in session_players:
            # Skip players with no Treatment
            if 'Treatment' not in p.participant.vars:
                continue
            if getattr(p, 'moved_to_selection', 0) != 1:
                continue
            if p.treatment == player.treatment:
                same_treatment_passed_count += 1

        player_id = (same_treatment_passed_count % 90) + 1
        player.assigned_id = player_id

        base = (player_id - 1) * 5
        player.SelectionLine1 = base + 0
        player.SelectionLine2 = base + 1
        player.SelectionLine3 = base + 2
        player.SelectionLine4 = base + 3
        player.SelectionLine5 = base + 4

        player.moved_to_selection = 1

class Selection1(MyBasePage):
    extra_fields = ['Selection1']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        # Get base vars from MyBasePage
        context = MyBasePage.vars_for_template(player)

        # Your CSV and data processing logic
        treatments_map = {
            1: 't1_data.csv',
            2: 't2_data.csv',
            4: 't4_data.csv',
            9: 't9_data.csv',
            10: 't10_data.csv',
        }
        csv = treatments_map.get(player.treatment)
        wide_df = pd.read_csv(csv)

        # Add your extracted data to context
        row_number = player.SelectionLine1
        # Adjust for zero-based indexing
        selected_row = wide_df.iloc[row_number]

        if selected_row is not None:
            context.update({
                'score1': selected_row['round2score1'],
                'score2': selected_row['round2score2'],
                'score3': selected_row['round2score3'],
                'score4': selected_row['round2score4'],
                'gender1': selected_row['gender1'],
                'gender2': selected_row['gender2'],
                'gender3': selected_row['gender3'],
                'gender4': selected_row['gender4'],
            })
        else:
            # Provide default or empty values to avoid template errors
            context.update({
                'score1': None,
                'score2': None,
                'score3': None,
                'score4': None,
                'gender1': None,
                'gender2': None,
                'gender3': None,
                'gender4': None,
            })

        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):


        if player.treatment == 1:
            csv = 't1_data.csv'
        elif player.treatment == 2:
            csv = 't2_data.csv'
        elif player.treatment == 4:
            csv = 't4_data.csv'
        elif player.treatment == 9:
            csv = 't9_data.csv'
        elif player.treatment == 10:
            csv = 't10_data.csv'

        wide_df = pd.read_csv(csv)
        result_df = pd.DataFrame()
        result_df['groupid'] = wide_df['groupid']
        result_df['gender'] = wide_df[['gender1', 'gender2', 'gender3', 'gender4']].values.tolist()
        result_df['round2score'] = wide_df[
            ['round2score1', 'round2score2', 'round2score3', 'round2score4']].values.tolist()
        result_df['round3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].values.tolist()
        result_df['ids'] = wide_df[['id1', 'id2', 'id3', 'id4']].values.tolist()

        result_df['highestround3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].idxmax(axis=1).apply(lambda x: int(x[-1]))

        row_number = player.SelectionLine1
        selected_row = wide_df.iloc[row_number]
        selected_row2 = result_df.iloc[row_number]

        if player.Selection1 == 1:
            player.Selection1_id = str(selected_row['id1'])
        elif player.Selection1 == 2:
            player.Selection1_id = str(selected_row['id2'])
        elif player.Selection1 == 3:
            player.Selection1_id = str(selected_row['id3'])
        elif player.Selection1 == 4:
            player.Selection1_id = str(selected_row['id4'])

        if player.incentivised_selection == 1:
            if player.Selection1 == selected_row2['highestround3score']:
                player.bonus = 1



class Selection2(MyBasePage):
    extra_fields = ['Selection2']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        # Get base vars from MyBasePage
        context = MyBasePage.vars_for_template(player)

        # Your CSV and data processing logic
        treatments_map = {
            1: 't1_data.csv',
            2: 't2_data.csv',
            4: 't4_data.csv',
            9: 't9_data.csv',
            10: 't10_data.csv',
        }
        csv = treatments_map.get(player.treatment)
        wide_df = pd.read_csv(csv)

        # Add your extracted data to context
        row_number = player.SelectionLine2
        # Adjust for zero-based indexing
        selected_row = wide_df.iloc[row_number]

        if selected_row is not None:
            context.update({
                'score1': selected_row['round2score1'],
                'score2': selected_row['round2score2'],
                'score3': selected_row['round2score3'],
                'score4': selected_row['round2score4'],
                'gender1': selected_row['gender1'],
                'gender2': selected_row['gender2'],
                'gender3': selected_row['gender3'],
                'gender4': selected_row['gender4'],
            })
        else:
            # Provide default or empty values to avoid template errors
            context.update({
                'score1': None,
                'score2': None,
                'score3': None,
                'score4': None,
                'gender1': None,
                'gender2': None,
                'gender3': None,
                'gender4': None,
            })

        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):

        if player.treatment == 1:
            csv = 't1_data.csv'
        elif player.treatment == 2:
            csv = 't2_data.csv'
        elif player.treatment == 4:
            csv = 't4_data.csv'
        elif player.treatment == 9:
            csv = 't9_data.csv'
        elif player.treatment == 10:
            csv = 't10_data.csv'

        wide_df = pd.read_csv(csv)
        result_df = pd.DataFrame()
        result_df['groupid'] = wide_df['groupid']
        result_df['gender'] = wide_df[['gender1', 'gender2', 'gender3', 'gender4']].values.tolist()
        result_df['round2score'] = wide_df[
            ['round2score1', 'round2score2', 'round2score3', 'round2score4']].values.tolist()
        result_df['round3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].values.tolist()
        result_df['ids'] = wide_df[['id1', 'id2', 'id3', 'id4']].values.tolist()

        result_df['highestround3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].idxmax(axis=1).apply(lambda x: int(x[-1]))

        row_number = player.SelectionLine2
        selected_row = wide_df.iloc[row_number]
        selected_row2 = result_df.iloc[row_number]

        if player.Selection2 == 1:
            player.Selection2_id = str(selected_row['id1'])
        elif player.Selection2 == 2:
            player.Selection2_id = str(selected_row['id2'])
        elif player.Selection2 == 3:
            player.Selection2_id = str(selected_row['id3'])
        elif player.Selection2 == 4:
            player.Selection2_id = str(selected_row['id4'])

        if player.incentivised_selection == 2:
            if player.Selection2 == selected_row2['highestround3score']:
                player.bonus = 1

class Selection3(MyBasePage):
    extra_fields = ['Selection3']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        # Get base vars from MyBasePage
        context = MyBasePage.vars_for_template(player)

        # Your CSV and data processing logic
        treatments_map = {
            1: 't1_data.csv',
            2: 't2_data.csv',
            4: 't4_data.csv',
            9: 't9_data.csv',
            10: 't10_data.csv',
        }
        csv = treatments_map.get(player.treatment)
        wide_df = pd.read_csv(csv)

        # Add your extracted data to context
        row_number = player.SelectionLine3
        # Adjust for zero-based indexing
        selected_row = wide_df.iloc[row_number]

        if selected_row is not None:
            context.update({
                'score1': selected_row['round2score1'],
                'score2': selected_row['round2score2'],
                'score3': selected_row['round2score3'],
                'score4': selected_row['round2score4'],
                'gender1': selected_row['gender1'],
                'gender2': selected_row['gender2'],
                'gender3': selected_row['gender3'],
                'gender4': selected_row['gender4'],
            })
        else:
            # Provide default or empty values to avoid template errors
            context.update({
                'score1': None,
                'score2': None,
                'score3': None,
                'score4': None,
                'gender1': None,
                'gender2': None,
                'gender3': None,
                'gender4': None,
            })

        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):

        if player.treatment == 1:
            csv = 't1_data.csv'
        elif player.treatment == 2:
            csv = 't2_data.csv'
        elif player.treatment == 4:
            csv = 't4_data.csv'
        elif player.treatment == 9:
            csv = 't9_data.csv'
        elif player.treatment == 10:
            csv = 't10_data.csv'

        wide_df = pd.read_csv(csv)
        result_df = pd.DataFrame()
        result_df['groupid'] = wide_df['groupid']
        result_df['gender'] = wide_df[['gender1', 'gender2', 'gender3', 'gender4']].values.tolist()
        result_df['round2score'] = wide_df[
            ['round2score1', 'round2score2', 'round2score3', 'round2score4']].values.tolist()
        result_df['round3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].values.tolist()
        result_df['ids'] = wide_df[['id1', 'id2', 'id3', 'id4']].values.tolist()

        result_df['highestround3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].idxmax(axis=1).apply(lambda x: int(x[-1]))

        row_number = player.SelectionLine3
        selected_row = wide_df.iloc[row_number]
        selected_row2 = result_df.iloc[row_number]

        if player.Selection3 == 1:
            player.Selection3_id = str(selected_row['id1'])
        elif player.Selection3 == 2:
            player.Selection3_id = str(selected_row['id2'])
        elif player.Selection3 == 3:
            player.Selection3_id = str(selected_row['id3'])
        elif player.Selection3 == 4:
            player.Selection3_id = str(selected_row['id4'])

        if player.incentivised_selection == 3:
            if player.Selection3 == selected_row2['highestround3score']:
                player.bonus = 1

class Selection4(MyBasePage):
    extra_fields = ['Selection4']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        # Get base vars from MyBasePage
        context = MyBasePage.vars_for_template(player)

        # Your CSV and data processing logic
        treatments_map = {
            1: 't1_data.csv',
            2: 't2_data.csv',
            4: 't4_data.csv',
            9: 't9_data.csv',
            10: 't10_data.csv',
        }
        csv = treatments_map.get(player.treatment)
        wide_df = pd.read_csv(csv)

        # Add your extracted data to context
        row_number = player.SelectionLine4
        # Adjust for zero-based indexing
        selected_row = wide_df.iloc[row_number]

        if selected_row is not None:
            context.update({
                'score1': selected_row['round2score1'],
                'score2': selected_row['round2score2'],
                'score3': selected_row['round2score3'],
                'score4': selected_row['round2score4'],
                'gender1': selected_row['gender1'],
                'gender2': selected_row['gender2'],
                'gender3': selected_row['gender3'],
                'gender4': selected_row['gender4'],
            })
        else:
            # Provide default or empty values to avoid template errors
            context.update({
                'score1': None,
                'score2': None,
                'score3': None,
                'score4': None,
                'gender1': None,
                'gender2': None,
                'gender3': None,
                'gender4': None,
            })

        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):

        if player.treatment == 1:
            csv = 't1_data.csv'
        elif player.treatment == 2:
            csv = 't2_data.csv'
        elif player.treatment == 4:
            csv = 't4_data.csv'
        elif player.treatment == 9:
            csv = 't9_data.csv'
        elif player.treatment == 10:
            csv = 't10_data.csv'

        wide_df = pd.read_csv(csv)
        result_df = pd.DataFrame()
        result_df['groupid'] = wide_df['groupid']
        result_df['gender'] = wide_df[['gender1', 'gender2', 'gender3', 'gender4']].values.tolist()
        result_df['round2score'] = wide_df[
            ['round2score1', 'round2score2', 'round2score3', 'round2score4']].values.tolist()
        result_df['round3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].values.tolist()
        result_df['ids'] = wide_df[['id1', 'id2', 'id3', 'id4']].values.tolist()

        result_df['highestround3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].idxmax(axis=1).apply(lambda x: int(x[-1]))

        row_number = player.SelectionLine4
        selected_row = wide_df.iloc[row_number]
        selected_row2 = result_df.iloc[row_number]

        if player.Selection4 == 1:
            player.Selection4_id = str(selected_row['id1'])
        elif player.Selection4 == 2:
            player.Selection4_id = str(selected_row['id2'])
        elif player.Selection4 == 3:
            player.Selection4_id = str(selected_row['id3'])
        elif player.Selection4 == 4:
            player.Selection4_id = str(selected_row['id4'])

        if player.incentivised_selection == 4:
            if player.Selection4 == selected_row2['highestround3score']:
                player.bonus = 1

class Selection5(MyBasePage):
    extra_fields = ['Selection5']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        # Get base vars from MyBasePage
        context = MyBasePage.vars_for_template(player)

        # Your CSV and data processing logic
        treatments_map = {
            1: 't1_data.csv',
            2: 't2_data.csv',
            4: 't4_data.csv',
            9: 't9_data.csv',
            10: 't10_data.csv',
        }
        csv = treatments_map.get(player.treatment)
        wide_df = pd.read_csv(csv)

        # Add your extracted data to context
        row_number = player.SelectionLine5
        # Adjust for zero-based indexing
        selected_row = wide_df.iloc[row_number]

        if selected_row is not None:
            context.update({
                'score1': selected_row['round2score1'],
                'score2': selected_row['round2score2'],
                'score3': selected_row['round2score3'],
                'score4': selected_row['round2score4'],
                'gender1': selected_row['gender1'],
                'gender2': selected_row['gender2'],
                'gender3': selected_row['gender3'],
                'gender4': selected_row['gender4'],
            })
        else:
            # Provide default or empty values to avoid template errors
            context.update({
                'score1': None,
                'score2': None,
                'score3': None,
                'score4': None,
                'gender1': None,
                'gender2': None,
                'gender3': None,
                'gender4': None,
            })

        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):

        if player.treatment == 1:
            csv = 't1_data.csv'
        elif player.treatment == 2:
            csv = 't2_data.csv'
        elif player.treatment == 4:
            csv = 't4_data.csv'
        elif player.treatment == 9:
            csv = 't9_data.csv'
        elif player.treatment == 10:
            csv = 't10_data.csv'

        wide_df = pd.read_csv(csv)
        result_df = pd.DataFrame()
        result_df['groupid'] = wide_df['groupid']
        result_df['gender'] = wide_df[['gender1', 'gender2', 'gender3', 'gender4']].values.tolist()
        result_df['round2score'] = wide_df[
            ['round2score1', 'round2score2', 'round2score3', 'round2score4']].values.tolist()
        result_df['round3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].values.tolist()
        result_df['ids'] = wide_df[['id1', 'id2', 'id3', 'id4']].values.tolist()

        result_df['highestround3score'] = wide_df[
            ['round3score1', 'round3score2', 'round3score3', 'round3score4']].idxmax(axis=1).apply(lambda x: int(x[-1]))

        row_number = player.SelectionLine5
        selected_row = wide_df.iloc[row_number]
        selected_row2 = result_df.iloc[row_number]

        if player.Selection5 == 1:
            player.Selection5_id = str(selected_row['id1'])
        elif player.Selection5 == 2:
            player.Selection5_id = str(selected_row['id2'])
        elif player.Selection5 == 3:
            player.Selection5_id = str(selected_row['id3'])
        elif player.Selection5 == 4:
            player.Selection5_id = str(selected_row['id4'])

        if player.incentivised_selection == 5:
            if player.Selection5 == selected_row2['highestround3score']:
                player.bonus = 1

class Correct(MyBasePage):

    @staticmethod
    def is_displayed(player):
        return player.bonus == 1

class RedirectCorrect(Page):

    @staticmethod
    def is_displayed(player):
        return player.bonus == 1

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkcorrect=
            player.subsession.session.config['completionlinkcorrect']
        )


class Incorrect(MyBasePage):

    @staticmethod
    def is_displayed(player):
        return player.bonus == 0


class RedirectIncorrect(Page):

    @staticmethod
    def is_displayed(player):
        return player.bonus == 0

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkincorrect=
            player.subsession.session.config['completionlinkincorrect']
        )


page_sequence = [
    Selection_instructions,
   Comprehension_Qs,
   Comprehension_Qs2,
    SelectionsBegin,
    Selection1,
    Selection2,
    Selection3,
    Selection4,
    Selection5,
    Correct,
    RedirectCorrect,
    Incorrect,
    RedirectIncorrect
]
