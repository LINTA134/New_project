from otree.api import Page
from .models import C

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class GossipStimuli(Page):
    form_model = 'player'
    form_fields = [
        'invest_A_limit', 'invest_A_amount',
        'invest_B_limit', 'invest_B_amount',
        'invest_C_limit', 'invest_C_amount',
        'invest_X_limit', 'invest_X_amount'
    ]

    def vars_for_template(self):
        return {
            'sender_is_cooperative': self.player.treatment == 'cooperative_sender'
        }

    def error_message(self, values):
        # 1. 予算枠の重複チェック
        limits = [
            values['invest_A_limit'],
            values['invest_B_limit'],
            values['invest_C_limit'],
            values['invest_X_limit']
        ]
        if len(set(limits)) != 4:
            return "4つの予算枠（4000万、3000万、2000万、1000万）を、重複しないように4人の起業家に割り当ててください。"

        # 2. 投資額が枠を超えていないかチェック
        errors = []
        if values['invest_A_amount'] > values['invest_A_limit']:
            errors.append(f"起業家Aへの投資額が上限（{values['invest_A_limit']}万円）を超えています。")
        if values['invest_B_amount'] > values['invest_B_limit']:
            errors.append(f"起業家Bへの投資額が上限（{values['invest_B_limit']}万円）を超えています。")
        if values['invest_C_amount'] > values['invest_C_limit']:
            errors.append(f"起業家Cへの投資額が上限（{values['invest_C_limit']}万円）を超えています。")
        if values['invest_X_amount'] > values['invest_X_limit']:
            errors.append(f"起業家Xへの投資額が上限（{values['invest_X_limit']}万円）を超えています。")
        
        if errors:
            return errors

class Questionnaire(Page):
    form_model = 'player'
    form_fields = [
        'intent_guess',
        'trust_1', 'trust_2', 'trust_3',
        'age', 'gender', 'feedback'
    ]

class Debrief(Page):
    form_model = 'player'
    form_fields = ['data_usage_consent']

page_sequence = [
    Introduction,
    GossipStimuli,
    Questionnaire,
    Debrief
]