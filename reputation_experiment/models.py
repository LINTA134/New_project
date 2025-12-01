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
        [500, '最大 500万円 枠'],
        [100, '最大 100万円 枠'],
    ]
    MAX_POSSIBLE_INVESTMENT = 4000

class Subsession(BaseSubsession):
    def creating_session(self):
        # itertools.cycle の代わりにランダム選択を使用
        for player in self.get_players():
            player.treatment = random.choice(['cooperative_sender', 'selfish_sender'])

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

    # --- アンケート項目（ゴシップ・意図推測） (変更なし) ---
    gossip_is_true = models.IntegerField(
        label="1-1. 内部情報の内容（オレンジ氏が配当を支払わなかったこと）は、事実である可能性が高いと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    orange_is_risky = models.IntegerField(
        label="1-2. 起業家オレンジは、投資するにはリスクが高すぎる人物だと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    orange_is_unethical = models.IntegerField(
        label="1-3. 起業家オレンジは、倫理観に欠けた人物だと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    intent_selfish = models.IntegerField(
        label="2-1 この情報を伝えた人物は、自分の予算枠を有利にするため、意図的にオレンジさんの評判を貶めようとしたと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    intent_altruistic = models.IntegerField(
        label="2-2. この情報を伝えた人物は、私（あなた）が損をしないようにという親切心から、真実を伝えてくれたと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    intent_fact_telling = models.IntegerField(
        label="2-3. この情報を伝えた人物は、特別な意図はなく、単に事実をありのままに報告しただけだと思う。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    
    # --- 関係流動性尺度 (新規追加) ---
    # スケールは7段階で統一（元の研究は6段階だがユーザーの要望に合わせる）
    # 彼ら = あなたの周囲の人たち
    rm_1_meet_many = models.IntegerField(
        label="3-1. 彼らには、人々と知り合いになる機会がたくさんある。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_2_talk_strangers = models.IntegerField(
        label="3-2. 彼らは、初対面の人と会話を交わすことがよくある。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_3_choose_partners = models.IntegerField(
        label="3-3. 彼らは、ふだんどんな人たちと付き合うかを、自分で選ぶことができる。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_4_few_friends_rev = models.IntegerField( # 逆転項目
        label="3-4. 彼らには、新しい友人を見つける機会があまりない。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_5_uncommon_talk_rev = models.IntegerField( # 逆転項目
        label="3-5. 彼らにとって見知らぬ人と会話することはそうあることではない。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_6_leave_for_better = models.IntegerField(
        label="3-6. もし現在所属している集団が気に入らなければ、彼らは新しい集団に移っていくだろう。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_7_cannot_choose_rev = models.IntegerField( # 逆転項目
        label="3-7. 彼らにとって、付き合う相手を自由に選べないことはよくある。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_8_easy_to_meet = models.IntegerField(
        label="3-8. 彼らが新しい人たちと出会うのは簡単なことだ。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_9_stay_in_group_rev = models.IntegerField( # 逆転項目
        label="3-9. たとえ所属する集団に満足していなかったとしても、彼らはたいていそこに居続けることになる。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_10_choose_groups = models.IntegerField(
        label="3-10. 彼らはどの集団や組織に所属するかを自分で選ぶことができる。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_11_must_stay_rel_rev = models.IntegerField( # 逆転項目
        label="3-11. たとえ現在の対人関係に満足していなくても、彼らはそこに留まり続けるしかないことがよくある。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )
    rm_12_must_stay_group_rev = models.IntegerField( # 逆転項目
        label="3-12. たとえ現在所属する集団から離れたいと思っても、彼らはそこに留まらざるを得ないことがよくある。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    # --- アテンション・チェック (新規追加) ---
    attention_check = models.IntegerField(
        label="データの品質を確認するため、この項目には「2」と答えてください。",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    # --- デモグラフィック (変更なし) ---
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