# Animal Clash Atlas（仮）

## コンセプト

子供向けの教育型カードバトルゲーム。

テーマ:

「本物の動物を知り、自分だけの技構成で最強を目指す」

特徴:

- 実在する動物のみ登場
- 動物ごとに固有の能力
- グー / チョキ / パー の3種類の技をカスタマイズ可能
- 技にはコスト制限あり
- あいこが3回続くと「アイコ技」が発動
- 弱点属性を突くと1.5倍ダメージ
- 図鑑要素あり（知育）

---

# ゲームルール

## 1ターンの流れ

1. プレイヤーが手を選択
   - グー
   - チョキ
   - パー

2. CPUも手を選択

3. じゃんけん判定

- 勝ち → 技発動
- 負け → 相手の技発動
- あいこ → draw_count +1

4. あいこ3回でアイコ技発動

5. HPが0になったら負け

---

# 技カテゴリ

グー:
パワー技

例:
- 噛みつく
- 突進
- 叩きつける

チョキ:
スピード技

例:
- 爪
- ひっかく
- 連続攻撃

パー:
特殊技

例:
- 威嚇
- 防御
- 毒
- 回復

アイコ:
必殺技

例:
- 群れの連携
- 奇襲
- 大咆哮

---

# 技コスト

各カードには上限コストがある。

例:

ライオン:
MAX COST = 12

構成:

グー:
強力な噛みつき cost 4

チョキ:
鋭い爪 cost 3

パー:
咆哮 cost 2

アイコ:
群れの連携 cost 3

合計:
12 / 12

OK

---

# 属性

例:

- bite
- claw
- water
- poison
- speed
- sound
- tail
- team
- ambush

弱点属性を受けると:

damage * 1.5

---

# MVP仕様

最初に作るもの:

- CLIで遊べる
- 動物3体
- 技10個程度
- CPU対戦
- カスタマイズなし（初期構成固定）
- 後でデッキ編集画面追加

---

# Python MVPコード
```python
from dataclasses import dataclass
import random

RPS = ["rock", "scissors", "paper"]

WIN_MAP = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}


@dataclass
class Skill:
    name: str
    hand: str
    power: int
    cost: int
    skill_type: str


@dataclass
class AnimalCard:
    name: str
    hp: int
    weakness: list[str]
    skills: dict[str, Skill]
    aiko_skill: Skill


def judge(player_hand, cpu_hand):
    if player_hand == cpu_hand:
        return "draw"
    if WIN_MAP[player_hand] == cpu_hand:
        return "player"
    return "cpu"


def calc_damage(skill, defender):
    damage = skill.power
    if skill.skill_type in defender.weakness:
        damage = int(damage * 1.5)
    return damage


lion = AnimalCard(
    name="ライオン",
    hp=120,
    weakness=["water", "poison"],
    skills={
        "rock": Skill("強力な噛みつき", "rock", 35, 4, "bite"),
        "scissors": Skill("鋭い爪", "scissors", 25, 3, "claw"),
        "paper": Skill("咆哮", "paper", 20, 2, "sound"),
    },
    aiko_skill=Skill("群れの連携", "draw", 30, 3, "team"),
)

crocodile = AnimalCard(
    name="ワニ",
    hp=130,
    weakness=["speed", "sound"],
    skills={
        "rock": Skill("デスロール", "rock", 40, 5, "bite"),
        "scissors": Skill("しっぽ攻撃", "scissors", 25, 3, "tail"),
        "paper": Skill("水中待ち伏せ", "paper", 30, 4, "water"),
    },
    aiko_skill=Skill("一瞬の奇襲", "draw", 35, 4, "ambush"),
)


player = lion
cpu = crocodile

draw_count = 0

while player.hp > 0 and cpu.hp > 0:
    print(f"\n{player.name} HP:{player.hp} / {cpu.name} HP:{cpu.hp}")

    player_hand = input("rock / scissors / paper > ").strip()
    cpu_hand = random.choice(RPS)

    print("あなた:", player_hand)
    print("CPU:", cpu_hand)

    result = judge(player_hand, cpu_hand)

    if result == "draw":
        draw_count += 1
        print("あいこ！", draw_count)

        if draw_count >= 3:
            damage = calc_damage(player.aiko_skill, cpu)
            cpu.hp -= damage
            print(f"アイコ技 {player.aiko_skill.name} 発動！ {damage}ダメージ")
            draw_count = 0

        continue

    draw_count = 0

    if result == "player":
        skill = player.skills[player_hand]
        damage = calc_damage(skill, cpu)
        cpu.hp -= damage
        print(f"{skill.name}! {damage}ダメージ")

    else:
        skill = cpu.skills[cpu_hand]
        damage = calc_damage(skill, player)
        player.hp -= damage
        print(f"敵の {skill.name}! {damage}ダメージ")


if player.hp <= 0:
    print("LOSE")
else:
    print("WIN")
```