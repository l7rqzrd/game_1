from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

from core import (
    ANIMALS,
    DEFAULT_LOADOUTS,
    EDITABLE_HANDS,
    HAND_LABELS,
    SKILL_INDEX,
    SKILL_LIBRARY,
    build_custom_card,
    get_total_cost,
    new_battle,
    resolve_turn,
)


st.set_page_config(
    page_title="Animal Clash Atlas",
    page_icon="🦁",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top, #fff4bf 0%, #ffe08a 24%, transparent 25%),
            linear-gradient(180deg, #8fd6ff 0%, #b9ecff 34%, #eef9d8 34%, #d8f0a6 100%);
    }
    .main .block-container {
        max-width: 980px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #17324d;
    }
    .battle-card {
        background: rgba(255, 255, 255, 0.92);
        border: 4px solid #17324d;
        border-radius: 28px;
        box-shadow: 0 14px 0 rgba(23, 50, 77, 0.16);
        padding: 1.2rem 1.4rem;
    }
    .battle-card.enemy {
        background: linear-gradient(180deg, #fff7f0 0%, #ffe2cf 100%);
    }
    .battle-card.player {
        background: linear-gradient(180deg, #f7fff3 0%, #daf9cf 100%);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }
    .card-title {
        font-size: 2rem;
        font-weight: 800;
        color: #17324d;
        line-height: 1.1;
    }
    .card-chip {
        display: inline-block;
        background: #17324d;
        color: #fff;
        border-radius: 999px;
        padding: 0.35rem 0.8rem;
        font-size: 0.9rem;
        font-weight: 700;
    }
    .card-portrait {
        display: block;
        width: 100%;
        max-height: 240px;
        object-fit: contain;
        border-radius: 22px;
        margin: 0.4rem 0 0.9rem;
        background: rgba(255, 255, 255, 0.7);
        padding: 0.6rem;
    }
    .card-portrait-emoji {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 180px;
        font-size: 5rem;
        border-radius: 22px;
        margin: 0.4rem 0 0.9rem;
        background: rgba(255, 255, 255, 0.7);
    }
    .hp-label {
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        color: #17324d;
        margin-bottom: 0.3rem;
    }
    .hp-track {
        width: 100%;
        height: 22px;
        border-radius: 999px;
        background: #dbe6ef;
        overflow: hidden;
        border: 2px solid #17324d;
    }
    .hp-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #ff8a65 0%, #ffd54f 48%, #7ddc6d 100%);
    }
    .fact-box {
        margin-top: 0.8rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.7);
        padding: 0.8rem 1rem;
        color: #26405b;
        font-size: 0.95rem;
    }
    .center-panel {
        text-align: center;
        padding: 1.4rem 0 1rem;
    }
    .vs-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 92px;
        height: 92px;
        border-radius: 999px;
        background: #17324d;
        color: #fff6b0;
        font-size: 2rem;
        font-weight: 900;
        box-shadow: 0 10px 0 rgba(23, 50, 77, 0.18);
        margin-bottom: 1rem;
    }
    .draw-badge {
        display: inline-block;
        margin-top: 0.8rem;
        background: #fff3b0;
        color: #5f4b00;
        border: 2px solid #d6b23b;
        border-radius: 999px;
        padding: 0.45rem 1rem;
        font-size: 1rem;
        font-weight: 800;
    }
    .battle-log {
        margin: 0 auto;
        max-width: 620px;
        background: rgba(255, 255, 255, 0.92);
        border: 4px solid #17324d;
        border-radius: 28px;
        box-shadow: 0 14px 0 rgba(23, 50, 77, 0.16);
        padding: 1rem 1.3rem;
        text-align: left;
    }
    .battle-log-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #17324d;
        margin-bottom: 0.5rem;
    }
    .battle-log-line {
        font-size: 1.05rem;
        color: #26405b;
        line-height: 1.6;
        font-weight: 700;
    }
    .weak-hit {
        margin-top: 0.7rem;
        display: inline-block;
        background: #ff6b6b;
        color: white;
        border-radius: 999px;
        padding: 0.5rem 0.95rem;
        font-size: 1rem;
        font-weight: 900;
    }
    .action-title {
        margin: 1.1rem 0 0.7rem;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 800;
        color: #17324d;
    }
    .mini-info {
        margin-top: 1rem;
        text-align: center;
        color: #26405b;
        font-weight: 700;
    }
    div.stButton > button {
        min-height: 74px;
        border-radius: 24px;
        border: 3px solid #17324d;
        font-size: 1.15rem;
        font-weight: 900;
        background: linear-gradient(180deg, #fffdf4 0%, #ffe7b8 100%);
        color: #17324d;
        box-shadow: 0 8px 0 rgba(23, 50, 77, 0.15);
    }
    div.stButton > button:hover {
        border-color: #17324d;
        color: #17324d;
        background: linear-gradient(180deg, #fff4d6 0%, #ffd68f 100%);
    }
    .skill-panel {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 24px;
        padding: 1rem 1.2rem;
        border: 3px solid rgba(23, 50, 77, 0.18);
    }
    [data-testid="stExpander"] details div[role="button"] p {
        font-weight: 800;
        color: #17324d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Animal Clash Atlas")
st.caption("実在する動物で戦う、明るいカードバトルMVP")


ANIMAL_EMOJI = {
    "ライオン": "🦁",
    "ワニ": "🐊",
    "ハヤブサ": "🦅",
}

ASSET_DIR = Path(__file__).parent / "assets" / "animals"


def ensure_state() -> None:
    if "custom_loadouts" not in st.session_state:
        st.session_state.custom_loadouts = {
            animal_name: loadout.copy()
            for animal_name, loadout in DEFAULT_LOADOUTS.items()
        }
    if "selected_player_animal" not in st.session_state:
        st.session_state.selected_player_animal = "ライオン"
    if "selected_enemy_animal" not in st.session_state:
        st.session_state.selected_enemy_animal = "ワニ"
    if "battle" not in st.session_state:
        start_battle(
            st.session_state.selected_player_animal,
            st.session_state.selected_enemy_animal,
        )
    if "log_history" not in st.session_state:
        st.session_state.log_history = [st.session_state.battle.last_log]


def get_player_card(animal_name: str):
    return build_custom_card(animal_name, st.session_state.custom_loadouts[animal_name])


def get_enemy_card(animal_name: str):
    return build_custom_card(animal_name, st.session_state.custom_loadouts[animal_name])


def start_battle(player_name: str, enemy_name: str) -> None:
    st.session_state.selected_player_animal = player_name
    st.session_state.selected_enemy_animal = enemy_name
    st.session_state.battle = new_battle(
        player_name,
        cpu_name=enemy_name,
        player_card=get_player_card(player_name),
        cpu_card=get_enemy_card(enemy_name),
    )
    st.session_state.log_history = [st.session_state.battle.last_log]


def skill_option_label(skill_key: str) -> str:
    skill = SKILL_INDEX[skill_key]
    hand_label = "アイコ" if skill.hand == "draw" else HAND_LABELS[skill.hand]
    return f"{skill.name} | {hand_label} | 威力{skill.power} | cost{skill.cost} | {skill.skill_type}"


def get_animal_art_markup(title: str) -> str:
    for suffix in ("png", "jpg", "jpeg", "webp"):
        image_path = ASSET_DIR / f"{title}.{suffix}"
        if image_path.exists():
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            return (
                f'<img class="card-portrait" src="data:image/{suffix};base64,{encoded}" '
                f'alt="{html.escape(title)}">'
            )
    emoji = ANIMAL_EMOJI.get(title, "🐾")
    return f'<div class="card-portrait-emoji">{emoji}</div>'


def render_card(title: str, hp: int, max_hp: int, fact: str, role: str) -> None:
    ratio = max(0, min(100, int(hp / max_hp * 100)))
    art_markup = get_animal_art_markup(title)
    st.markdown(
        f"""
        <div class="battle-card {role}">
            <div class="card-header">
                <div class="card-title">{html.escape(title)}</div>
                <div class="card-chip">{'てき' if role == 'enemy' else 'あなた'}</div>
            </div>
            {art_markup}
            <div class="hp-label">
                <span>HP</span>
                <span>{hp}/{max_hp}</span>
            </div>
            <div class="hp-track">
                <div class="hp-fill" style="width: {ratio}%;"></div>
            </div>
            <div class="fact-box">{html.escape(fact)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_log() -> None:
    lines = [line for line in battle.last_log.splitlines() if line.strip()]
    weak_hit = any("弱点！1.5倍！" in line for line in lines)
    log_html = "".join(
        f"<div class='battle-log-line'>{html.escape(line)}</div>"
        for line in lines[-4:]
    )
    weak_html = "<div class='weak-hit'>弱点！1.5倍！</div>" if weak_hit else ""
    st.markdown(
        f"""
        <div class="center-panel">
            <div class="vs-badge">VS</div>
            <div class="battle-log">
                <div class="battle-log-title">バトルログ</div>
                {log_html}
                {weak_html}
            </div>
            <div class="draw-badge">あいこカウント: {battle.draw_count} / 3</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


ensure_state()
battle = st.session_state.battle

with st.sidebar:
    st.header("対戦設定")
    animal_names = list(ANIMALS.keys())
    selected_player_animal = st.selectbox(
        "あなたの動物",
        animal_names,
        index=animal_names.index(st.session_state.selected_player_animal),
    )
    selected_enemy_animal = st.selectbox(
        "敵の動物",
        animal_names,
        index=animal_names.index(st.session_state.selected_enemy_animal),
    )
    if st.button("この組み合わせで最初から遊ぶ", use_container_width=True):
        start_battle(selected_player_animal, selected_enemy_animal)
        st.rerun()

    st.divider()
    st.header("どうぶつ図鑑")
    for animal in ANIMALS.values():
        with st.expander(animal.name):
            st.write(animal.fact)
            st.write(f"HP: {animal.max_hp}")
            st.write(f"弱点属性: {', '.join(animal.weakness)}")
            st.write(f"最大コスト: {animal.max_cost}")

tabs = st.tabs(["バトル", "カード編集"])

with tabs[0]:
    render_card(
        battle.cpu_card.name,
        battle.cpu_hp,
        battle.cpu_card.max_hp,
        battle.cpu_card.fact,
        "enemy",
    )
    render_log()
    render_card(
        battle.player_card.name,
        battle.player_hp,
        battle.player_card.max_hp,
        battle.player_card.fact,
        "player",
    )

    if battle.finished:
        if battle.winner == "player":
            st.success("勝利しました。もう一度遊ぶなら再戦してください。")
        else:
            st.error("敗北しました。技構成を見直して再挑戦できます。")
    else:
        st.markdown("<div class='action-title'>出す手をえらぼう！</div>", unsafe_allow_html=True)
        action_cols = st.columns(3)
        for column, hand in zip(action_cols, ("rock", "scissors", "paper")):
            skill = battle.player_card.skills[hand]
            label = f"{HAND_LABELS[hand]}\n{skill.name}"
            if column.button(label, use_container_width=True):
                resolve_turn(battle, hand)
                st.session_state.log_history.insert(0, battle.last_log)
                st.rerun()

    if st.button("同じ組み合わせでもう一度", use_container_width=True):
        start_battle(battle.player_card.name, battle.cpu_card.name)
        st.rerun()

    with st.expander("技のくわしい情報"):
        left, right = st.columns(2)
        with left:
            st.subheader("自分の技")
            for hand in ("rock", "scissors", "paper"):
                skill = battle.player_card.skills[hand]
                st.markdown(
                    f"**{HAND_LABELS[hand]} / {skill.name}**  \n"
                    f"威力: {skill.power} / コスト: {skill.cost} / 属性: {skill.skill_type}  \n"
                    f"{skill.description}"
                )
            aiko = battle.player_card.aiko_skill
            st.markdown(
                f"**アイコ / {aiko.name}**  \n"
                f"威力: {aiko.power} / コスト: {aiko.cost} / 属性: {aiko.skill_type}  \n"
                f"{aiko.description}"
            )
            total_cost = get_total_cost(st.session_state.custom_loadouts[battle.player_card.name])
            st.info(f"自分の合計コスト: {total_cost} / {battle.player_card.max_cost}")
        with right:
            st.subheader("敵の技")
            for hand in ("rock", "scissors", "paper"):
                skill = battle.cpu_card.skills[hand]
                st.markdown(
                    f"**{HAND_LABELS[hand]} / {skill.name}**  \n"
                    f"威力: {skill.power} / コスト: {skill.cost} / 属性: {skill.skill_type}  \n"
                    f"{skill.description}"
                )
            enemy_aiko = battle.cpu_card.aiko_skill
            st.markdown(
                f"**アイコ / {enemy_aiko.name}**  \n"
                f"威力: {enemy_aiko.power} / コスト: {enemy_aiko.cost} / 属性: {enemy_aiko.skill_type}  \n"
                f"{enemy_aiko.description}"
            )
            enemy_cost = get_total_cost(st.session_state.custom_loadouts[battle.cpu_card.name])
            st.info(f"敵の合計コスト: {enemy_cost} / {battle.cpu_card.max_cost}")

    if st.session_state.log_history:
        with st.expander("これまでのログ"):
            for entry in st.session_state.log_history[:8]:
                st.code(entry)

with tabs[1]:
    st.subheader("カード編集")
    edit_animal = st.selectbox(
        "編集する動物",
        list(ANIMALS.keys()),
        key="edit_animal",
        index=list(ANIMALS.keys()).index(st.session_state.selected_player_animal),
    )
    base_card = ANIMALS[edit_animal]
    loadout = st.session_state.custom_loadouts[edit_animal].copy()

    st.write(f"{edit_animal} の最大コスト: {base_card.max_cost}")

    edited_loadout = {}
    for hand in EDITABLE_HANDS:
        label = "アイコ技" if hand == "draw" else HAND_LABELS[hand]
        options = [option.key for option in SKILL_LIBRARY[hand]]
        current_key = loadout[hand]
        edited_key = st.selectbox(
            label,
            options,
            index=options.index(current_key),
            format_func=skill_option_label,
            key=f"{edit_animal}_{hand}",
        )
        edited_loadout[hand] = edited_key
        selected_skill = SKILL_INDEX[edited_key]
        st.caption(
            f"{selected_skill.description} 属性: {selected_skill.skill_type} / cost {selected_skill.cost}"
        )

    total_cost = get_total_cost(edited_loadout)
    remaining_cost = base_card.max_cost - total_cost
    preview_card = build_custom_card(edit_animal, edited_loadout)

    if remaining_cost >= 0:
        st.success(f"保存可能です。合計コスト: {total_cost} / {base_card.max_cost}")
    else:
        st.error(f"コスト超過です。合計コスト: {total_cost} / {base_card.max_cost}")

    st.write("編集プレビュー")
    for hand in ("rock", "scissors", "paper"):
        skill = preview_card.skills[hand]
        st.write(f"{HAND_LABELS[hand]}: {skill.name} / 威力 {skill.power} / {skill.skill_type}")
    st.write(
        f"アイコ: {preview_card.aiko_skill.name} / 威力 {preview_card.aiko_skill.power} / {preview_card.aiko_skill.skill_type}"
    )

    save_disabled = remaining_cost < 0
    if st.button("この構成を保存して再戦", disabled=save_disabled, use_container_width=True):
        st.session_state.custom_loadouts[edit_animal] = edited_loadout
        start_battle(
            st.session_state.selected_player_animal,
            st.session_state.selected_enemy_animal,
        )
        st.rerun()

    if st.button("初期構成に戻す", use_container_width=True):
        st.session_state.custom_loadouts[edit_animal] = DEFAULT_LOADOUTS[edit_animal].copy()
        if edit_animal in {
            st.session_state.selected_player_animal,
            st.session_state.selected_enemy_animal,
        }:
            start_battle(
                st.session_state.selected_player_animal,
                st.session_state.selected_enemy_animal,
            )
        st.rerun()
