from otree.api import Page
from .models import C

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class ProfileReview(Page):
    def vars_for_template(self):
        # ゴシップの発信者をテンプレートに渡す
        return {
            'sender_is_cooperative': self.player.treatment == 'cooperative_sender'
        }
    def is_displayed(self):
        return self.round_number == 1

class GossipStimuli(Page):
    form_model = 'player'
    form_fields = [
        'invest_A_limit',
        'invest_B_limit',
        'invest_C_limit',
        'invest_X_limit',
        #'invest_A_amount',
        #'invest_B_amount',
        #'invest_C_amount',
        #'invest_X_amount'
    ]
    
    def vars_for_template(self):
        return {
            'sender_is_cooperative': self.player.treatment == 'cooperative_sender'
        }
    
    def error_message(self, values):
        # 予算枠重複チェックと投資上限チェックのロジックはそのまま残します。
        limits = [
            values['invest_A_limit'],
            values['invest_B_limit'],
            values['invest_C_limit'],
            values['invest_X_limit']
        ]
        if len(set(limits)) != 4:
            return "4つの予算枠（4000万、3000万、500万、100万）を、重複しないように4人の起業家に割り当ててください。"
        """
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
        """    

class Questionnaire(Page):
    form_model = 'player'
    
    def vars_for_template(self):
        return {
            'sender_is_cooperative': self.player.treatment == 'cooperative_sender'
        }
    # 1ページ目はゴシップと意図の評価のみ
    form_fields = [
        'gossip_is_true', 'orange_is_risky', 'orange_is_unethical',
        'intent_selfish', 'intent_altruistic', 'intent_fact_telling',
    ]

# 新規追加: 関係流動性とアテンションチェック、デモグラフィック
class RelationalMobility(Page):
    form_model = 'player'
    form_fields = [
        'rm_1_meet_many', 'rm_2_talk_strangers', 'rm_3_choose_partners',
        'rm_4_few_friends_rev', 'rm_5_uncommon_talk_rev', 'rm_6_leave_for_better',
        'attention_check', 
        'rm_7_cannot_choose_rev', 'rm_8_easy_to_meet', 'rm_9_stay_in_group_rev',
        'rm_10_choose_groups', 'rm_11_must_stay_rel_rev', 'rm_12_must_stay_group_rev',
        'age', 'gender', 'feedback'
    ]

class Debrief(Page):
    form_model = 'player'
    form_fields = ['data_usage_consent']

page_sequence = [
    Introduction,
    ProfileReview,
    GossipStimuli,
    Questionnaire,
    RelationalMobility, 
    Debrief
]