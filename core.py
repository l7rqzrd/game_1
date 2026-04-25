from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Literal

RPS = ("rock", "scissors", "paper")
EDITABLE_HANDS = ("rock", "scissors", "paper", "draw")
Hand = Literal["rock", "scissors", "paper", "draw"]

HAND_LABELS = {
    "rock": "グー",
    "scissors": "チョキ",
    "paper": "パー",
}

WIN_MAP = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}


@dataclass(frozen=True)
class Skill:
    name: str
    hand: str
    power: int
    cost: int
    skill_type: str
    description: str


@dataclass(frozen=True)
class AnimalCard:
    name: str
    max_hp: int
    weakness: tuple[str, ...]
    skills: dict[str, Skill]
    aiko_skill: Skill
    max_cost: int
    fact: str


@dataclass
class BattleState:
    player_card: AnimalCard
    cpu_card: AnimalCard
    player_hp: int
    cpu_hp: int
    draw_count: int = 0
    turn: int = 1
    last_log: str = "対戦開始"
    finished: bool = False
    winner: str | None = None


@dataclass(frozen=True)
class SkillOption:
    key: str
    skill: Skill


def judge(player_hand: str, cpu_hand: str) -> str:
    if player_hand == cpu_hand:
        return "draw"
    if WIN_MAP[player_hand] == cpu_hand:
        return "player"
    return "cpu"


def calc_damage(skill: Skill, defender: AnimalCard) -> tuple[int, bool]:
    damage = skill.power
    weak_hit = skill.skill_type in defender.weakness
    if weak_hit:
        damage = int(damage * 1.5)
    return damage, weak_hit


SKILL_LIBRARY: dict[Hand, tuple[SkillOption, ...]] = {
    "rock": (
        SkillOption("power_bite", Skill("強力な噛みつき", "rock", 35, 4, "bite", "大きなあごでかみつく。")),
        SkillOption("death_roll", Skill("デスロール", "rock", 40, 5, "bite", "かみついたまま回転して大ダメージ。")),
        SkillOption("dive_kick", Skill("急降下キック", "rock", 32, 4, "speed", "高い空から一気に急降下する。")),
        SkillOption("rush_attack", Skill("突進クラッシュ", "rock", 30, 3, "tail", "全身を使って勢いよくぶつかる。")),
    ),
    "scissors": (
        SkillOption("sharp_claw", Skill("鋭い爪", "scissors", 25, 3, "claw", "前足の爪で素早く切り裂く。")),
        SkillOption("tail_attack", Skill("しっぽ攻撃", "scissors", 25, 3, "tail", "太いしっぽを振り回す。")),
        SkillOption("talon_strike", Skill("かぎ爪ストライク", "scissors", 28, 3, "claw", "かぎ爪でねらいを定めてつかむ。")),
        SkillOption("combo_slash", Skill("連続ひっかき", "scissors", 22, 2, "speed", "素早い連続攻撃で相手を追い詰める。")),
    ),
    "paper": (
        SkillOption("roar", Skill("咆哮", "paper", 20, 2, "sound", "大きな声で相手をひるませる。")),
        SkillOption("water_ambush", Skill("水中待ち伏せ", "paper", 30, 4, "water", "水辺にかくれてタイミングをうかがう。")),
        SkillOption("sky_circle", Skill("上空旋回", "paper", 18, 2, "wind", "上空を回って相手のすきを探す。")),
        SkillOption("venom_mist", Skill("毒のしぶき", "paper", 24, 3, "poison", "毒をふくんだしぶきでじわじわ弱らせる。")),
    ),
    "draw": (
        SkillOption("team_combo", Skill("群れの連携", "draw", 30, 3, "team", "仲間と連携して一気に攻める。")),
        SkillOption("instant_ambush", Skill("一瞬の奇襲", "draw", 35, 4, "ambush", "水中から一気に飛び出しておそいかかる。")),
        SkillOption("air_ambush", Skill("空からの連続奇襲", "draw", 38, 3, "ambush", "空中戦の強みを生かして連続攻撃。")),
        SkillOption("great_roar", Skill("大咆哮", "draw", 28, 2, "sound", "大地にひびく大きな声で流れを変える。")),
    ),
}

SKILL_INDEX = {
    option.key: option.skill
    for options in SKILL_LIBRARY.values()
    for option in options
}


def create_animals() -> dict[str, AnimalCard]:
    return {
        "ライオン": AnimalCard(
            name="ライオン",
            max_hp=120,
            weakness=("water", "poison"),
            skills={
                "rock": Skill("強力な噛みつき", "rock", 35, 4, "bite", "大きなあごでかみつく。"),
                "scissors": Skill("鋭い爪", "scissors", 25, 3, "claw", "前足の爪で素早く切り裂く。"),
                "paper": Skill("咆哮", "paper", 20, 2, "sound", "大きな声で相手をひるませる。"),
            },
            aiko_skill=Skill("群れの連携", "draw", 30, 3, "team", "仲間と連携して一気に攻める。"),
            max_cost=12,
            fact="ライオンは群れでくらし、協力して狩りをすることがあります。",
        ),
        "ワニ": AnimalCard(
            name="ワニ",
            max_hp=130,
            weakness=("speed", "sound"),
            skills={
                "rock": Skill("デスロール", "rock", 40, 5, "bite", "かみついたまま回転して大ダメージ。"),
                "scissors": Skill("しっぽ攻撃", "scissors", 25, 3, "tail", "太いしっぽを振り回す。"),
                "paper": Skill("水中待ち伏せ", "paper", 30, 4, "water", "水辺にかくれてタイミングをうかがう。"),
            },
            aiko_skill=Skill("一瞬の奇襲", "draw", 35, 4, "ambush", "水中から一気に飛び出しておそいかかる。"),
            max_cost=16,
            fact="ワニは水辺でじっと待ち、近づいたえものを一気におそいます。",
        ),
        "ハヤブサ": AnimalCard(
            name="ハヤブサ",
            max_hp=100,
            weakness=("tail", "team"),
            skills={
                "rock": Skill("急降下キック", "rock", 32, 4, "speed", "高い空から一気に急降下する。"),
                "scissors": Skill("かぎ爪ストライク", "scissors", 28, 3, "claw", "かぎ爪でねらいを定めてつかむ。"),
                "paper": Skill("上空旋回", "paper", 18, 2, "wind", "上空を回って相手のすきを探す。"),
            },
            aiko_skill=Skill("空からの連続奇襲", "draw", 38, 3, "ambush", "空中戦の強みを生かして連続攻撃。"),
            max_cost=12,
            fact="ハヤブサはとても速く飛ぶ鳥として知られています。",
        ),
    }


ANIMALS = create_animals()

DEFAULT_LOADOUTS: dict[str, dict[Hand, str]] = {
    "ライオン": {
        "rock": "power_bite",
        "scissors": "sharp_claw",
        "paper": "roar",
        "draw": "team_combo",
    },
    "ワニ": {
        "rock": "death_roll",
        "scissors": "tail_attack",
        "paper": "water_ambush",
        "draw": "instant_ambush",
    },
    "ハヤブサ": {
        "rock": "dive_kick",
        "scissors": "talon_strike",
        "paper": "sky_circle",
        "draw": "air_ambush",
    },
}


def get_total_cost(loadout: dict[Hand, str]) -> int:
    return sum(SKILL_INDEX[key].cost for key in loadout.values())


def build_custom_card(animal_name: str, loadout: dict[Hand, str]) -> AnimalCard:
    base_card = ANIMALS[animal_name]
    return AnimalCard(
        name=base_card.name,
        max_hp=base_card.max_hp,
        weakness=base_card.weakness,
        skills={
            "rock": SKILL_INDEX[loadout["rock"]],
            "scissors": SKILL_INDEX[loadout["scissors"]],
            "paper": SKILL_INDEX[loadout["paper"]],
        },
        aiko_skill=SKILL_INDEX[loadout["draw"]],
        max_cost=base_card.max_cost,
        fact=base_card.fact,
    )


def new_battle(
    player_name: str,
    cpu_name: str | None = None,
    player_card: AnimalCard | None = None,
    cpu_card: AnimalCard | None = None,
) -> BattleState:
    player_card = player_card or ANIMALS[player_name]
    if cpu_card is None:
        candidates = [name for name in ANIMALS if name != player_name]
        cpu_card = ANIMALS[cpu_name] if cpu_name else ANIMALS[random.choice(candidates)]
    return BattleState(
        player_card=player_card,
        cpu_card=cpu_card,
        player_hp=player_card.max_hp,
        cpu_hp=cpu_card.max_hp,
    )


def resolve_turn(state: BattleState, player_hand: str) -> BattleState:
    if state.finished:
        return state

    cpu_hand = random.choice(RPS)
    result = judge(player_hand, cpu_hand)
    log_lines = [
        f"{state.turn}ターン目",
        f"あなた: {HAND_LABELS[player_hand]}",
        f"CPU: {HAND_LABELS[cpu_hand]}",
    ]

    if result == "draw":
        state.draw_count += 1
        log_lines.append(f"あいこ。現在 {state.draw_count} 回連続です。")
        if state.draw_count >= 3:
            damage, weak_hit = calc_damage(state.player_card.aiko_skill, state.cpu_card)
            state.cpu_hp = max(0, state.cpu_hp - damage)
            weak_text = " 弱点！1.5倍！" if weak_hit else ""
            log_lines.append(
                f"アイコ技「{state.player_card.aiko_skill.name}」が発動！ {damage}ダメージ！{weak_text}"
            )
            state.draw_count = 0
    else:
        state.draw_count = 0
        if result == "player":
            skill = state.player_card.skills[player_hand]
            damage, weak_hit = calc_damage(skill, state.cpu_card)
            state.cpu_hp = max(0, state.cpu_hp - damage)
            weak_text = " 弱点！1.5倍！" if weak_hit else ""
            log_lines.append(f"あなたの「{skill.name}」！ {damage}ダメージ！{weak_text}")
        else:
            skill = state.cpu_card.skills[cpu_hand]
            damage, weak_hit = calc_damage(skill, state.player_card)
            state.player_hp = max(0, state.player_hp - damage)
            weak_text = " 弱点！1.5倍！" if weak_hit else ""
            log_lines.append(f"敵の「{skill.name}」！ {damage}ダメージ！{weak_text}")

    if state.player_hp <= 0 or state.cpu_hp <= 0:
        state.finished = True
        state.winner = "player" if state.cpu_hp <= 0 else "cpu"
        log_lines.append("あなたの勝ち!" if state.winner == "player" else "CPUの勝ち...")

    state.last_log = "\n".join(log_lines)
    state.turn += 1
    return state
