from otree.api import Page
from .models import Constants

class Introduction(Page):
    pass

class GossipStimuli(Page):
    form_model = 'player'
    # 投資額を入力させる
    form_fields = ['invest_A', 'invest_B', 'invest_C', 'invest_X']

    def vars_for_template(self):
        # テンプレート側で「誰が発信者か」を表示し分けるための変数を渡す
        return {
            'sender_is_cooperative': self.player.treatment == 'cooperative_sender'
        }

class Ranking(Page):
    form_model = 'player'
    form_fields = ['rank_A', 'rank_B', 'rank_C', 'rank_X']

    def error_message(self, values):
        # 入力チェック：1位〜4位が重複していないか確認
        ranks = [values['rank_A'], values['rank_B'], values['rank_C'], values['rank_X']]
        if sorted(ranks) != [1, 2, 3, 4]:
            return '順位は1位から4位まで、重複なく入力してください。'

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['intent_guess']

class Debrief(Page):
    pass

page_sequence = [
    #Introduction,
    GossipStimuli,
    #Ranking,
    #Questionnaire,
    #Debrief
    ]