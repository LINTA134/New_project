from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
卒業研究：評判とゴシップへの疑い実験（投資シナリオ版）
"""

class C(BaseConstants):
    NAME_IN_URL = 'reputation_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # 予算枠の選択肢（数値と表示ラベル）
    LIMIT_CHOICES = [
        [4000, '最大 4,000万円 枠'],
        [3000, '最大 3,000万円 枠'],
        [2000, '最大 2,000万円 枠'],
        [1000, '最大 1,000万円 枠'],
    ]
    MAX_POSSIBLE_INVESTMENT = 4000

class Subsession(BaseSubsession):
    def creating_session(self):
        import itertools
        treatments = itertools.cycle(['cooperative_sender', 'selfish_sender'])
        for player in self.get_players():
            player.treatment = next(treatments)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()

    # --- Step 1 & 2: 予算枠の選択 と 投資実行額 ---
    
    # 起業家A
    invest_A_limit = models.IntegerField(choices=C.LIMIT_CHOICES, label="割り当てる予算枠")
    invest_A_amount = models.CurrencyField(min=0, max=C.MAX_POSSIBLE_INVESTMENT, label="実際の投資実行額")

    # 起業家B
    invest_B_limit = models.IntegerField(choices=C.LIMIT_CHOICES, label="割り当てる予算枠")
    invest_B_amount = models.CurrencyField(min=0, max=C.MAX_POSSIBLE_INVESTMENT, label="実際の投資実行額")

    # 起業家C
    invest_C_limit = models.IntegerField(choices=C.LIMIT_CHOICES, label="割り当てる予算枠")
    invest_C_amount = models.CurrencyField(min=0, max=C.MAX_POSSIBLE_INVESTMENT, label="実際の投資実行額")

    # 起業家X
    invest_X_limit = models.IntegerField(choices=C.LIMIT_CHOICES, label="割り当てる予算枠")
    invest_X_amount = models.CurrencyField(min=0, max=C.MAX_POSSIBLE_INVESTMENT, label="実際の投資実行額")


    # --- アンケート項目 ---
    intent_guess = models.IntegerField(
        choices=[
            [1, '親切心（あなたが損をしないように）'],
            [2, '事実伝達（ありのままを伝えるため）'],
            [3, '競争心（ライバルを蹴落とすため）'],
        ],
        label="この情報を伝えた人物の「意図」として最も近いものは？",
        widget=widgets.RadioSelect
    )

    # --- 一般的信頼尺度 ---
    trust_1 = models.IntegerField(
        label="ほとんどの人は基本的に正直だと思う",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    trust_2 = models.IntegerField(
        label="ほとんどの人は信頼できると思う",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    trust_3 = models.IntegerField(
        label="ほとんどの人は基本的に善良で親切だと思う",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    # --- デモグラフィック ---
    age = models.IntegerField(label="あなたの年齢を教えてください", min=18, max=99)
    gender = models.StringField(
        label="あなたの性別を教えてください",
        choices=['男性', '女性', 'その他', '回答しない'],
        widget=widgets.RadioSelect
    )
    feedback = models.LongStringField(
        label="この実験について、気になったことや感想があれば自由にお書きください（任意）",
        blank=True
    )
    data_usage_consent = models.BooleanField(
        label="上記の説明を読み、デセプション（情報の操作）が含まれていたことを理解しました。その上で、私の回答データを研究分析に使用することに同意します。",
        widget=widgets.CheckboxInput,
        initial=False
    )