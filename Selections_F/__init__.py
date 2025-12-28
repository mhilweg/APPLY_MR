from otree.api import *
import random
import time
from common import *

doc = '''
This is the main survey app. It contains
'''


# ==== In‑memory data for treatments 2 and 10 ====
# NOTE: First block you sent is now T10, second block is T2.

T10_ROWS = [
    # row 0
    dict(
        groupid=3,
        gender=[2, 1, 1, 2],
        round2=[13, 10, 14, 11],
        round3=[8, 11, 18, 16],
        ids=[
            '66ae6229ffbaa5975422455e',
            '6314e875f7c98f1d344b2e3f',
            '60ca846ffad77e5b1fee110a',
            '60f722b3a83e22a28e18860e',
        ],
    ),
    # row 1
    dict(
        groupid=26,
        gender=[2, 1, 1, 2],
        round2=[15, 16, 8, 16],
        round3=[13, 25, 10, 16],
        ids=[
            '5a973b8235237b0001127686',
            '5eff4094fad01549cec780bb',
            '63d40af204ab71781d81b112',
            '66ee1b8ee4da3710c1695515',
        ],
    ),
    # row 2
    dict(
        groupid=28,
        gender=[2, 1, 2, 1],
        round2=[17, 18, 19, 16],
        round3=[19, 19, 27, 17],
        ids=[
            '66919140828b8946afc029c5',
            '62734ce38db73cd5bd81a36f',
            '6755e799307c1a8afbb8c162',
            '6522fa3ac0163b9e739d097d',
        ],
    ),
    # row 3
    dict(
        groupid=35,
        gender=[2, 1, 2, 1],
        round2=[20, 18, 13, 10],
        round3=[27, 28, 9, 13],
        ids=[
            '66be0314cbc4fc351df839a0',
            '63cfee97e59ec37f870b287f',
            '669677d986a5a20026bbf20e',
            '64bbf16db125b5d6a2f3a911',
        ],
    ),
    # row 4
    dict(
        groupid=178,
        gender=[1, 2, 2, 1],
        round2=[20, 10, 18, 13],
        round3=[16, 5, 18, 17],
        ids=[
            '59067e147a22a80001849720',
            '6636fd4bc3513a27d95c3e46',
            '662fbae9b9b9d43471a00ef9',
            '5c1ffe5295f978000173df84',
        ],
    ),
]

T2_ROWS = [
    # row 0
    dict(
        groupid=3,
        gender=[2, 1, 1, 2],
        round2=[13, 10, 14, 11],
        round3=[16, 0, 18, 12],
        ids=[
            '66b1967c80dfbef628f49076',
            '5de831cad4995d000c5fb540',
            '5fa1636a77c875235bd8e1f6',
            '65cb90ace80f886a058024ce',
        ],
    ),
    # row 1
    dict(
        groupid=15,
        gender=[2, 1, 2, 1],
        round2=[18, 18, 17, 12],
        round3=[20, 17, 16, 16],
        ids=[
            '6743e31b8d80b64c6fad696f',
            '63d7b81d79044b73bfb50952',
            '63dbddb434d075a0bff1dbc7',
            '62fce9a6d7fa7bc8559d6ce1',
        ],
    ),
    # row 2
    dict(
        groupid=58,
        gender=[2, 1, 1, 2],
        round2=[18, 17, 10, 17],
        round3=[16, 12, 19, 17],
        ids=[
            '613a32539be30e10dca2c288',
            '57160a57cd6ea20011dae249',
            '5c345ebad4f77a0001a91ec0',
            '6736d9badac6c2599d5b0c5d',
        ],
    ),
    # row 3
    dict(
        groupid=73,
        gender=[2, 1, 2, 1],
        round2=[18, 9, 16, 16],
        round3=[20, 10, 16, 16],
        ids=[
            '66e77c1f53b8d806313b5314',
            '614c3ad2075d2710db4dc03e',
            '5a8c5f67000dab00018cd8f0',
            '665ceb52bf7bc5f5f2016e83',
        ],
    ),
    # row 4
    dict(
        groupid=178,
        gender=[1, 2, 2, 1],
        round2=[20, 10, 18, 13],
        round3=[20, 8, 16, 16],
        ids=[
            '68a741770ddcfded8f735e8e',
            '647845ab90c460ec4a86efba',
            '5eab170759f5390b776df5a1',
            '62a0f99814d73df8032871a9',
        ],
    ),
]


def get_rows_for_treatment(treatment):
    if treatment == 2:
        return T2_ROWS
    if treatment == 10:
        return T10_ROWS
    return None


class C(CommonConstants):
    NAME_IN_URL = 'Main_part'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PIECE_RATE = 0.05

    Round_length = 120
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
    page_pass_time = models.FloatField()

    Gender = models.StringField()

    Round2_Mix = models.IntegerField(
        choices=[[1, 'Easy Mix'], [2, 'Hard Mix']]
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

    Selection1_group = models.IntegerField()
    Selection2_group = models.IntegerField()
    Selection3_group = models.IntegerField()
    Selection4_group = models.IntegerField()
    Selection5_group = models.IntegerField()

    treatment = models.IntegerField()
    bonus = models.IntegerField(initial=0)
    moved_to_selection = models.IntegerField(initial=0)
    assigned_id = models.IntegerField()

    Round2 = models.IntegerField(initial=0)
    Round2_Attempts = models.IntegerField(initial=0, blank=True)
    Round3 = models.IntegerField(initial=0)
    Round3_Attempts = models.IntegerField(initial=0, blank=True)

    Choice = models.IntegerField(
        choices=[[1, 'Payment Rule A'], [2, 'Payment Rule B']],
        label='R3 Payment Rule Choice'
    )

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

    Comprehension_password = models.StringField(blank=False, label='Password')

    clicked_info = models.StringField(initial=False)
    Calculator = models.StringField(min=0, max=100, blank=True, label='Calculator')

    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)


# ==== Helper functions for selections ====

def get_row(player: Player, which_line: int):
    rows = get_rows_for_treatment(player.treatment)
    if rows is None:
        return None
    index = getattr(player, f'SelectionLine{which_line}')
    return rows[index]


def vars_for_selection(player: Player, which_line: int):
    row = get_row(player, which_line)
    if row is None:
        return dict(
            score1=None, score2=None, score3=None, score4=None,
            gender1=None, gender2=None, gender3=None, gender4=None
        )
    return dict(
        score1=row['round2'][0],
        score2=row['round2'][1],
        score3=row['round2'][2],
        score4=row['round2'][3],
        gender1=row['gender'][0],
        gender2=row['gender'][1],
        gender3=row['gender'][2],
        gender4=row['gender'][3],
    )


def process_selection(player: Player, which_line: int, choice_field: str, id_field: str):
    row = get_row(player, which_line)
    if row is None:
        return

    choice = getattr(player, choice_field)

    # record chosen id
    if choice in [1, 2, 3, 4]:
        chosen_id = row['ids'][choice - 1]
        setattr(player, id_field, str(chosen_id))

    # record groupid for this selection
    setattr(player, f'Selection{which_line}_group', row['groupid'])

    # bonus logic (highest round3score)
    round3 = row['round3']
    max_idx = max(range(4), key=lambda i: round3[i]) + 1
    if player.incentivised_selection == which_line and choice == max_idx:
        player.bonus = 1

# ==== Pages ====

class Selection_instructions(MyBasePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.treatment = player.participant.Treatment
        player.page_pass_time = time.time() + C.Min_round_length

        mix_draw = random.randint(1, 2)
        player.Round2_Mix = mix_draw
        player.participant.R2_mix = mix_draw

        player.incentivised_selection = random.randint(1, 5)
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

        incorrect_index = (
            player.CQ1_incorrect +
            player.CQ2_incorrect +
            player.CQ3_incorrect
        )
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
            if 'Treatment' not in p.participant.vars:
                continue
            if getattr(p, 'moved_to_selection', 0) != 1:
                continue
            if p.treatment == player.treatment:
                same_treatment_passed_count += 1

        player_id = (same_treatment_passed_count % 90) + 1
        player.assigned_id = player_id

        # random order of the 5 rows (for both t2 and t10)
        indices = [0, 1, 2, 3, 4]
        random.shuffle(indices)
        player.SelectionLine1 = indices[0]
        player.SelectionLine2 = indices[1]
        player.SelectionLine3 = indices[2]
        player.SelectionLine4 = indices[3]
        player.SelectionLine5 = indices[4]

        player.moved_to_selection = 1


class Selection1(MyBasePage):
    extra_fields = ['Selection1']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        context = MyBasePage.vars_for_template(player)
        context.update(vars_for_selection(player, 1))
        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        process_selection(player, which_line=1,
                          choice_field='Selection1',
                          id_field='Selection1_id')


class Selection2(MyBasePage):
    extra_fields = ['Selection2']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        context = MyBasePage.vars_for_template(player)
        context.update(vars_for_selection(player, 2))
        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        process_selection(player, which_line=2,
                          choice_field='Selection2',
                          id_field='Selection2_id')


class Selection3(MyBasePage):
    extra_fields = ['Selection3']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        context = MyBasePage.vars_for_template(player)
        context.update(vars_for_selection(player, 3))
        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        process_selection(player, which_line=3,
                          choice_field='Selection3',
                          id_field='Selection3_id')


class Selection4(MyBasePage):
    extra_fields = ['Selection4']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        context = MyBasePage.vars_for_template(player)
        context.update(vars_for_selection(player, 4))
        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        process_selection(player, which_line=4,
                          choice_field='Selection4',
                          id_field='Selection4_id')


class Selection5(MyBasePage):
    extra_fields = ['Selection5']
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player):
        context = MyBasePage.vars_for_template(player)
        context.update(vars_for_selection(player, 5))
        return context

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        process_selection(player, which_line=5,
                          choice_field='Selection5',
                          id_field='Selection5_id')


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
            completionlinkcorrect=player.subsession.session.config['completionlinkcorrect']
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
            completionlinkincorrect=player.subsession.session.config['completionlinkincorrect']
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
    RedirectIncorrect,
]
