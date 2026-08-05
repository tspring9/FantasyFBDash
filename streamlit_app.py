"""
League Stat Sheet — The Liquorball Syndicate
A fantasy football BI dashboard built from ESPN exports (2018-2025).
"""

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="League Stat Sheet",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------
# THEME
# ---------------------------------------------------------------
BG = "#0F2818"
PANEL = "#1C3D28"
PANEL_LINE = "#2A4E36"
CHALK = "#F2EFE6"
CHALK_DIM = "#B9C2B4"
STEEL = "#8A9186"
AMBER = "#F5A623"
AMBER_DIM = "#8C6A2E"
RED = "#C1443C"
GREEN = "#5FA777"

FONT_DISPLAY = "'Oswald', 'Arial Narrow', Impact, sans-serif"
FONT_MONO = "'IBM Plex Mono', 'SF Mono', 'Courier New', monospace"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    .stApp {{
        background-color: {BG};
        color: {CHALK};
    }}

    /* headline / title */
    .league-eyebrow {{
        font-family: {FONT_MONO};
        font-size: 11px;
        letter-spacing: 0.16em;
        color: {STEEL};
        text-transform: uppercase;
    }}
    .league-title {{
        font-family: {FONT_DISPLAY};
        font-weight: 800;
        font-size: 42px;
        letter-spacing: 0.01em;
        color: {CHALK};
        margin: 4px 0 6px 0;
    }}

    /* KPI tiles */
    div[data-testid="stMetric"] {{
        background-color: {PANEL};
        border: 1px solid {PANEL_LINE};
        border-radius: 4px;
        padding: 14px 16px 10px 16px;
    }}
    div[data-testid="stMetricLabel"] {{
        font-family: {FONT_MONO} !important;
        font-size: 10.5px !important;
        letter-spacing: 0.1em;
        color: {STEEL} !important;
        text-transform: uppercase;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: {FONT_DISPLAY} !important;
        font-weight: 800 !important;
        color: {CHALK} !important;
    }}

    /* section panel */
    .panel {{
        background-color: {PANEL};
        border: 1px solid {PANEL_LINE};
        border-radius: 4px;
        padding: 18px 20px;
        margin-bottom: 18px;
    }}
    .eyebrow {{
        font-family: {FONT_MONO};
        font-size: 11px;
        letter-spacing: 0.14em;
        color: {AMBER};
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .big-stat {{
        font-family: {FONT_DISPLAY};
        font-weight: 800;
        font-size: 40px;
        line-height: 1;
    }}
    .mono-line {{
        font-family: {FONT_MONO};
        font-size: 12.5px;
        color: {CHALK};
        margin-top: 4px;
    }}
    .mono-line-main {{
        font-family: {FONT_MONO};
        font-size: 13px;
        color: {CHALK};
        margin-top: 8px;
    }}
    .name-tag {{
        font-family: {FONT_DISPLAY};
        font-weight: 800;
        font-size: 24px;
        color: {CHALK};
    }}
    .name-tag .unique {{
        color: {AMBER};
    }}
    .name-tag .team {{
        color: {CHALK};
        font-weight: 500;
        font-size: 18px;
    }}
    .footnote {{
        font-family: {FONT_MONO};
        font-size: 11px;
        color: {STEEL};
        text-align: center;
        margin-top: 24px;
    }}

    /* tabs */
    button[data-baseweb="tab"] {{
        font-family: {FONT_DISPLAY};
        font-weight: 700;
        font-size: 15px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: {CHALK};
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {AMBER} !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: {AMBER} !important;
    }}

    /* dataframes */
    div[data-testid="stDataFrame"] {{
        font-family: {FONT_MONO};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

PLOTLY_LAYOUT = dict(
    paper_bgcolor=PANEL,
    plot_bgcolor=PANEL,
    font=dict(family=FONT_MONO, color=CHALK, size=12),
    margin=dict(l=10, r=10, t=10, b=10),
)


def style_fig(fig, height=320):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(gridcolor=PANEL_LINE, zerolinecolor=PANEL_LINE)
    fig.update_yaxes(gridcolor=PANEL_LINE, zerolinecolor=PANEL_LINE)
    return fig


# ---------------------------------------------------------------
# DATA
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    path = Path(__file__).parent / "data" / "dashboard_data.json"
    with open(path) as f:
        return json.load(f)


DATA = load_data()
SEASONS = [c["season"] for c in DATA["champions"]]
PERF_SEASONS = DATA["draftPerformance"]["seasonsAvailable"]

standings_df = pd.DataFrame(DATA["standings"])
leaderboard_df = pd.DataFrame(DATA["leaderboard"])
trend_df = pd.DataFrame(DATA["trend"])
top_players_df = pd.DataFrame(DATA["topPlayers"])
first_picks_df = pd.DataFrame(DATA["firstPicks"])
draft_slot_agg_df = pd.DataFrame(DATA["draftVsStanding"]["aggregate"])


def name_tag_html(unique, team, stacked=True):
    if not unique:
        return team
    if stacked:
        return f'<span class="unique">{unique}</span> <span class="team">&mdash; {team}</span>'
    return unique


# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.markdown('<div class="league-eyebrow">The Liquorball Syndicate &middot; Est. 2018</div>', unsafe_allow_html=True)
st.markdown('<div class="league-title">LEAGUE STAT SHEET</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# KPI ROW
# ---------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Seasons Logged", DATA["kpis"]["seasons"], "2018\u20132025")
k2.metric("Managers", DATA["kpis"]["managers"])
k3.metric("Games Played", DATA["kpis"]["totalGames"])
k4.metric("All-Time High Score", DATA["kpis"]["highScore"], "single team, single week")
k5.metric("Avg Score / Team-Game", DATA["kpis"]["avgScore"])

st.write("")

# ---------------------------------------------------------------
# TABS
# ---------------------------------------------------------------
tab_season, tab_alltime, tab_draft, tab_records = st.tabs(
    ["Season Explorer", "All-Time", "Draft Room", "Record Book"]
)

# =================================================================
# TAB: SEASON EXPLORER
# =================================================================
with tab_season:
    season = st.radio("Season", SEASONS, index=len(SEASONS) - 1, horizontal=True, label_visibility="collapsed")

    champ = next(c for c in DATA["champions"] if c["season"] == season)
    rows = standings_df[standings_df.Season == season].sort_values("Rank")

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">{season} Champion</div>
            <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:8px;">
                <div class="name-tag">{name_tag_html(champ['uniqueName'], champ['team'].strip())}</div>
                <div class="mono-line">Record {champ['record']} &nbsp;|&nbsp; {champ['pf']} PF</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Final Standings &mdash; Wins / Losses</div>', unsafe_allow_html=True)

    rows_sorted = rows.sort_values("Rank", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=rows_sorted["UniqueName"], x=rows_sorted["Wins"], name="Wins",
        orientation="h", marker_color=AMBER,
        customdata=rows_sorted["Team"], hovertemplate="%{customdata}<br>Wins: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=rows_sorted["UniqueName"], x=rows_sorted["Losses"], name="Losses",
        orientation="h", marker_color=RED,
        customdata=rows_sorted["Team"], hovertemplate="%{customdata}<br>Losses: %{x}<extra></extra>",
    ))
    fig.update_layout(barmode="stack", legend=dict(orientation="h", y=1.08))
    style_fig(fig, height=max(280, len(rows_sorted) * 34))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<div class="mono-line">Bars labeled by manager &mdash; hover for team name.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================================
# TAB: ALL-TIME
# =================================================================
with tab_alltime:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">League-Wide Scoring Trend (avg pts / team / game)</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df["season"], y=trend_df["avgScore"], mode="lines+markers",
        line=dict(color=AMBER, width=2.5), marker=dict(size=8, color=AMBER), name="Avg Score",
    ))
    style_fig(fig, height=260)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Best Win % All-Time, By Manager (min. one full season)</div>', unsafe_allow_html=True)
    lb = leaderboard_df[leaderboard_df.GP >= 13].sort_values("WinPct", ascending=False).head(10).copy()
    lb.insert(0, "#", range(1, len(lb) + 1))
    lb["Record"] = lb.apply(
        lambda r: f"{int(r.Wins)}-{int(r.Losses)}" + (f"-{int(r.Ties)}" if r.Ties else ""), axis=1
    )
    lb["Win %"] = (lb["WinPct"] * 100).round(1).astype(str) + "%"
    display_lb = lb[["#", "UniqueName", "Record", "Win %", "PPG", "Seasons"]].rename(
        columns={"UniqueName": "Manager"}
    )
    st.dataframe(display_lb, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================================
# TAB: DRAFT ROOM
# =================================================================
with tab_draft:
    sub = st.radio(
        "View", ["Best & Busts", "Draft Order Impact", "Draft Trends"],
        horizontal=True, label_visibility="collapsed",
    )

    # ---------------- Best & Busts ----------------
    if sub == "Best & Busts":
        perf_season = st.radio(
            "Perf season", PERF_SEASONS, index=len(PERF_SEASONS) - 1,
            horizontal=True, label_visibility="collapsed", key="perf_season",
        )
        block = DATA["draftPerformance"]["bySeason"][str(perf_season)]

        c1, c2 = st.columns(2)
        if block["busts"]:
            b = block["busts"][0]
            c1.markdown(
                f"""
                <div class="panel">
                    <div class="eyebrow">Biggest Bust &mdash; {perf_season}</div>
                    <div class="big-stat" style="color:{RED};">{b['player']}</div>
                    <div class="mono-line">Round {b['round']}, Pick {b['pick']} &mdash; {b['uniqueName']}</div>
                    <div class="mono-line">Scored {b['pts']} vs {b['proj']} projected ({b['diff']})</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if block["sleepers"]:
            sl = block["sleepers"][0]
            c2.markdown(
                f"""
                <div class="panel">
                    <div class="eyebrow">Biggest Sleeper &mdash; {perf_season}</div>
                    <div class="big-stat" style="color:{GREEN};">{sl['player']}</div>
                    <div class="mono-line">Round {sl['round']}, Pick {sl['pick']} &mdash; {sl['uniqueName']}</div>
                    <div class="mono-line">Scored {sl['pts']} vs {sl['proj']} projected (+{sl['diff']})</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="eyebrow">Draft Pick vs. Points Above Projection &mdash; {perf_season}</div>',
            unsafe_allow_html=True,
        )
        scatter_df = pd.DataFrame(block["scatter"])
        colors = scatter_df["diff"].apply(lambda d: RED if d <= -25 else GREEN if d >= 25 else STEEL)
        opacity = scatter_df["diff"].apply(lambda d: 0.95 if abs(d) >= 25 else 0.35)
        fig = go.Figure()
        fig.add_hline(y=0, line_dash="dash", line_color=STEEL)
        fig.add_trace(go.Scatter(
            x=scatter_df["pick"], y=scatter_df["diff"], mode="markers",
            marker=dict(color=colors, opacity=opacity, size=9),
            customdata=scatter_df[["player", "round", "uniqueName", "pts", "proj"]],
            hovertemplate=(
                "%{customdata[0]}<br>Pick %{x} (Rd %{customdata[1]}) &mdash; %{customdata[2]}"
                "<br>%{customdata[3]} pts vs %{customdata[4]} proj<extra></extra>"
            ),
        ))
        fig.update_xaxes(autorange="reversed", title="Overall Pick (earlier picks on the right)")
        fig.update_yaxes(title="Pts vs Projection")
        style_fig(fig, height=340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="mono-line">Each dot is a drafted player. Red = underperformed projection by 25+ pts. '
            'Green = beat projection by 25+ pts.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="eyebrow">Top Busts (Rounds 1&ndash;4)</div>', unsafe_allow_html=True)
            for b in block["busts"]:
                st.markdown(
                    f'<div class="mono-line-main">{b["player"]} '
                    f'<span style="color:{STEEL};">(R{b["round"]}, {b["uniqueName"]})</span> '
                    f'&nbsp;&mdash;&nbsp; <span style="color:{RED};">{b["diff"]}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="eyebrow">Top Sleepers (Rounds 12&ndash;16)</div>', unsafe_allow_html=True)
            for sl in block["sleepers"]:
                st.markdown(
                    f'<div class="mono-line-main">{sl["player"]} '
                    f'<span style="color:{STEEL};">(R{sl["round"]}, {sl["uniqueName"]})</span> '
                    f'&nbsp;&mdash;&nbsp; <span style="color:{GREEN};">+{sl["diff"]}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Draft Order Impact ----------------
    elif sub == "Draft Order Impact":
        view = st.radio(
            "Order view", ["All Seasons (Aggregate)", "Single Season"],
            horizontal=True, label_visibility="collapsed", key="order_view",
        )

        if view == "All Seasons (Aggregate)":
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(
                '<div class="eyebrow">Average Final Rank By Draft Slot (2018&ndash;2025)</div>',
                unsafe_allow_html=True,
            )
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=draft_slot_agg_df["draftSlot"], y=draft_slot_agg_df["avgFinalRank"],
                marker_color=AMBER, text=draft_slot_agg_df["avgFinalRank"], textposition="outside",
            ))
            fig.update_yaxes(autorange="reversed", range=[12, 1], title="Avg Final Rank")
            fig.update_xaxes(title="Round 1 Draft Slot", dtick=1)
            style_fig(fig, height=340)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<div class="mono-line">Lower bar = better average finish. A flat chart would mean draft '
                "slot doesn't predict outcome.</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            order_seasons = sorted(int(y) for y in DATA["draftVsStanding"]["bySeason"].keys())
            order_season = st.radio(
                "Order season", order_seasons, index=len(order_seasons) - 1,
                horizontal=True, label_visibility="collapsed", key="order_season",
            )
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="eyebrow">Draft Slot vs. Final Rank &mdash; {order_season}</div>',
                unsafe_allow_html=True,
            )
            season_rows = pd.DataFrame(DATA["draftVsStanding"]["bySeason"][str(order_season)])
            season_rows = season_rows.sort_values("draftSlot")
            season_rows["Movement"] = season_rows["draftSlot"] - season_rows["finalRank"]

            def move_label(m):
                if m > 0:
                    return f"\u2191 {m}"
                if m < 0:
                    return f"\u2193 {abs(m)}"
                return "\u2014"

            display = pd.DataFrame({
                "Draft Slot": season_rows["draftSlot"].apply(lambda x: f"#{x}"),
                "Manager": season_rows["uniqueName"] + " (" + season_rows["team"].str.strip() + ")",
                "Final Rank": season_rows["finalRank"].apply(lambda x: f"#{x}"),
                "Movement": season_rows["Movement"].apply(move_label),
            })
            st.dataframe(display, hide_index=True, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Draft Trends ----------------
    else:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Most Drafted Players (2018-2025)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_players_df["player"], y=top_players_df["count"],
            marker_color=AMBER, text=top_players_df["count"], textposition="outside",
        ))
        fig.update_xaxes(tickangle=-35)
        fig.update_yaxes(title="Seasons Drafted")
        style_fig(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Round 1, Pick 1 &mdash; By Season</div>', unsafe_allow_html=True)
        fp = first_picks_df.copy()
        fp["Manager"] = fp["UniqueName"] + " (" + fp["Team"].str.strip() + ")"
        st.dataframe(
            fp[["Season", "Manager", "Player"]], hide_index=True, use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

# =================================================================
# TAB: RECORD BOOK
# =================================================================
with tab_records:
    rb_options = ["All-Time"] + SEASONS
    rb_choice = st.radio("Record scope", rb_options, horizontal=True, label_visibility="collapsed")

    r = DATA["records"]["overall"] if rb_choice == "All-Time" else DATA["records"]["bySeason"][str(rb_choice)]

    cards = [
        {
            "title": "Biggest Blowout",
            "big": f"+{r['blowout']['margin']}",
            "color": AMBER,
            "lines": [
                f"{r['blowout'].get('winnerUnique') or r['blowout']['winner']} over "
                f"{r['blowout'].get('loserUnique') or r['blowout']['loser']}",
                f"{r['blowout']['season']}, Week {r['blowout']['week']}",
            ],
        },
        {
            "title": "Closest Finish",
            "big": f"{r['closest']['margin']}",
            "color": AMBER,
            "lines": [
                f"{r['closest'].get('homeUnique') or r['closest']['home']} {r['closest']['homeScore']} "
                f"\u2013 {r['closest']['awayScore']} {r['closest'].get('awayUnique') or r['closest']['away']}",
                f"{r['closest']['season']}, Week {r['closest']['week']}",
            ],
        },
        {
            "title": "Highest Single Score",
            "big": f"{r['highScore']['score']}",
            "color": AMBER,
            "lines": [
                r["highScore"].get("uniqueName") or r["highScore"]["team"],
                f"{r['highScore']['season']}, Week {r['highScore']['week']}",
            ],
        },
        {
            "title": "Highest-Scoring Shootout",
            "big": f"{r['shootout']['total']}",
            "color": AMBER,
            "lines": [
                f"{r['shootout'].get('homeUnique') or r['shootout']['home']} vs "
                f"{r['shootout'].get('awayUnique') or r['shootout']['away']}",
                f"{r['shootout']['season']}, Week {r['shootout']['week']}",
            ],
        },
    ]

    cols = st.columns(4)
    for col, c in zip(cols, cards):
        col.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">{c['title']}</div>
                <div class="big-stat" style="color:{c['color']};">{c['big']}</div>
                <div class="mono-line-main">{c['lines'][0]}</div>
                <div class="mono-line">{c['lines'][1]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.markdown(
    f"""
    <div class="footnote">
        Source: ESPN Fantasy Football exports, 2018&ndash;2025 &middot;
        Manager names shown as First Name + Last Initial &middot;
        Draft value analysis covers seasons with weekly projection data: {", ".join(str(s) for s in PERF_SEASONS)}
    </div>
    """,
    unsafe_allow_html=True,
)
