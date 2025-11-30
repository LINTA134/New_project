from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
卒業研究：評判とゴシップへの疑い実験（投資シナリオ版）
"""

class Constants(BaseConstants):
    NAME_IN_URL = 'reputation_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # 投資可能額の上限（1,000万円）
    MAX_INVESTMENT = 1000

class Subsession(BaseSubsession):
    def creating_session(self):
        # 参加者がアクセスした瞬間に、条件をランダムに割り当てる処理
        import itertools
        treatments = itertools.cycle(['cooperative_sender', 'selfish_sender'])
        for player in self.get_players():
            player.treatment = next(treatments)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # --- 実験条件（自動割り当て） ---
    treatment = models.StringField()

    # --- Step 1: 個別投資額 (0-1000) ---
    invest_A = models.CurrencyField(min=0, max=Constants.MAX_INVESTMENT, label="起業家Aへの承認額")
    invest_B = models.CurrencyField(min=0, max=Constants.MAX_INVESTMENT, label="起業家Bへの承認額")
    invest_C = models.CurrencyField(min=0, max=Constants.MAX_INVESTMENT, label="起業家Cへの承認額")
    invest_X = models.CurrencyField(min=0, max=Constants.MAX_INVESTMENT, label="起業家Xへの承認額")

    # --- Step 2: 優先順位 (1-4位) ---
    # UI側で重複チェックなどを行うか、単純な入力欄にするか選べますが、
    # ここではシンプルな整数入力として定義します。
    rank_A = models.IntegerField(min=1, max=4, label="起業家Aの順位")
    rank_B = models.IntegerField(min=1, max=4, label="起業家Bの順位")
    rank_C = models.IntegerField(min=1, max=4, label="起業家Cの順位")
    rank_X = models.IntegerField(min=1, max=4, label="起業家Xの順位")

    # --- アンケート項目 ---
    # ゴシップ発信者の意図推測
    intent_guess = models.IntegerField(
        choices=[
            [1, '親切心（あなたが損をしないように）'],
            [2, '事実伝達（ありのままを伝えるため）'],
            [3, '競争心（ライバルを蹴落とすため）'],
        ],
        label="この情報を伝えた人物の「意図」として最も近いものは？",
        widget=widgets.RadioSelect
    )
    
    # 一般的信頼尺度などが必要ならここに追加