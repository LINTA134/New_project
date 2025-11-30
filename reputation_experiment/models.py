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
    invest_A = models.CurrencyField(min=0, max=C.MAX_INVESTMENT, label="起業家Aへの承認額")
    invest_B = models.CurrencyField(min=0, max=C.MAX_INVESTMENT, label="起業家Bへの承認額")
    invest_C = models.CurrencyField(min=0, max=C.MAX_INVESTMENT, label="起業家Cへの承認額")
    invest_X = models.CurrencyField(min=0, max=C.MAX_INVESTMENT, label="起業家Xへの承認額")

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

    # --- 一般的信頼尺度（短縮版: 1=全くそう思わない ～ 7=非常にそう思う） ---
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

    # --- デモグラフィック変数 ---
    age = models.IntegerField(
        label="あなたの年齢を教えてください",
        min=18, max=99
    )
    gender = models.StringField(
        label="あなたの性別を教えてください",
        choices=['男性', '女性', 'その他', '回答しない'],
        widget=widgets.RadioSelect
    )
    
    # 自由記述（任意）
    feedback = models.LongStringField(
        label="この実験について、気になったことや感想があれば自由にお書きください（任意）",
        blank=True
    )

    data_usage_consent = models.BooleanField(
        label="上記の説明を読み、デセプション（情報の操作）が含まれていたことを理解しました。その上で、私の回答データを研究分析に使用することに同意します。",
        widget=widgets.CheckboxInput,
        initial=False
    )

    # 一般的信頼尺度などが必要ならここに追加