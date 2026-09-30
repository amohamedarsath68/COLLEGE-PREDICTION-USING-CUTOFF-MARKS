import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="TNEA College Allotment Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 40%, #0f172a 100%);
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stMarkdown { color: #cbd5e1; }

    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.25);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.35rem 0 !important;
    }
    .main-header p {
        color: #e0f2fe !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }
    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        color: #fff;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.75rem;
        border: 1px solid rgba(255,255,255,0.25);
    }

    .kpi-card {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        height: 100%;
    }
    .kpi-icon { font-size: 1.75rem; margin-bottom: 0.4rem; }
    .kpi-value { font-size: 1.85rem; font-weight: 800; color: #38bdf8; line-height: 1.2; }
    .kpi-label {
        font-size: 0.8rem; color: #94a3b8; font-weight: 500;
        margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.04em;
    }

    .rec-card {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .rec-college { font-size: 1.05rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem; }
    .rec-meta { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.35rem; }
    .rec-stats {
        display: flex; gap: 1.25rem; flex-wrap: wrap;
        margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #334155;
    }
    .rec-stat-item { font-size: 0.85rem; color: #cbd5e1; }
    .rec-stat-item strong { color: #38bdf8; }

    .badge-safe {
        background: rgba(34, 197, 94, 0.15); color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
        padding: 0.2rem 0.65rem; border-radius: 999px;
        font-size: 0.75rem; font-weight: 700; display: inline-block;
    }
    .badge-moderate {
        background: rgba(234, 179, 8, 0.15); color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.4);
        padding: 0.2rem 0.65rem; border-radius: 999px;
        font-size: 0.75rem; font-weight: 700; display: inline-block;
    }
    .badge-reach {
        background: rgba(239, 68, 68, 0.15); color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 0.2rem 0.65rem; border-radius: 999px;
        font-size: 0.75rem; font-weight: 700; display: inline-block;
    }

    .section-title {
        font-size: 1.35rem; font-weight: 700; color: #f1f5f9;
        margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #334155;
    }
    .summary-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px; padding: 1rem 1.25rem;
        margin-bottom: 1.25rem; color: #cbd5e1; font-size: 0.95rem;
    }
    .summary-box strong { color: #38bdf8; }
    .disclaimer {
        background: rgba(148, 163, 184, 0.08);
        border-left: 3px solid #64748b;
        padding: 0.85rem 1.15rem; border-radius: 0 10px 10px 0;
        font-size: 0.8rem; color: #94a3b8; margin: 1.5rem 0;
    }
    .empty-state {
        text-align: center; padding: 2.5rem 2rem;
        background: rgba(30, 41, 59, 0.6);
        border-radius: 14px; border: 1px dashed #475569;
    }
    .empty-state h3 { color: #f1f5f9; margin-bottom: 0.5rem; }
    .empty-state p { color: #94a3b8; }
    .hint-box {
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.35);
        border-radius: 12px; padding: 1rem 1.25rem;
        margin: 1rem 0; color: #fde68a; font-size: 0.9rem;
    }
    .app-footer {
        text-align: center; padding: 2rem 1rem 1rem;
        margin-top: 2.5rem; border-top: 1px solid #334155;
        color: #64748b; font-size: 0.85rem;
    }
    .app-footer strong { color: #94a3b8; }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    label { color: #cbd5e1 !important; font-weight: 500 !important; }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        border-radius: 8px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# CONSTANTS — same as your notebook
# =============================================================================
CASTE_MAPPING = {
    "OC": "oc",
    "BC": "bc",
    "BCM": "bcm",
    "MBC": "mbc",
    "SC": "sc",
    "SCA": "sca",
    "ST": "st",
}

CATEGORY_COLORS = {"Safe": "#22c55e", "Moderate": "#eab308", "Reach": "#ef4444"}
CATEGORY_EMOJI = {"Safe": "🟢", "Moderate": "🟡", "Reach": "🔴"}


# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data(show_spinner="Loading TNEA cutoff data...")
def load_data() -> pd.DataFrame:
    """Load tnea_cutoffs.csv from the same folder as app.py."""
    candidates = [
        Path(__file__).parent / "tnea_cutoffs.csv",
        Path("tnea_cutoffs.csv"),
        Path(__file__).parent / "data" / "tnea_cutoffs.csv",
    ]
    csv_path = None
    for p in candidates:
        if p.exists():
            csv_path = p
            break
    if csv_path is None:
        raise FileNotFoundError(
            "tnea_cutoffs.csv not found. Place it in the same folder as app.py."
        )

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    for col in ["college_name", "district", "college_type", "branch_code", "branch_name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["oc", "bc", "bcm", "mbc", "sc", "sca", "st"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# =============================================================================
# CORE RECOMMENDATION LOGIC (from your notebook — unchanged rules)
# =============================================================================
def student_college_recommendation(
    df: pd.DataFrame,
    mark: float,
    caste: str,
    district: str | None = None,
    branch: str | None = None,
) -> pd.DataFrame:
    """
    Original logic:
    - Keep rows where category cutoff is not NaN and cutoff <= student mark
    - difference = mark - cutoff
    - Safe (>=5), Moderate (>=2), Reach (<2)
    - Optional district / branch filters (case-insensitive contains)
    - Sort by cutoff descending
    """
    caste = str(caste).upper().strip()
    if caste not in CASTE_MAPPING:
        raise ValueError(f"Invalid caste. Choose from {list(CASTE_MAPPING.keys())}")

    cutoff_column = CASTE_MAPPING[caste]

    result = df[
        df[cutoff_column].notna() & (df[cutoff_column] <= float(mark))
    ].copy()

    result["cutoff"] = result[cutoff_column]
    result["difference"] = float(mark) - result["cutoff"]

    # District filter
    if district and str(district).strip() and str(district).upper() not in (
        "ALL DISTRICTS",
        "ALL",
        "",
    ):
        result = result[
            result["district"].str.contains(str(district).strip(), case=False, na=False)
        ]

    # Branch / department filter
    if branch and str(branch).strip() and str(branch).upper() not in (
        "ALL DEPARTMENTS",
        "ALL",
        "",
    ):
        result = result[
            result["branch_name"].str.contains(str(branch).strip(), case=False, na=False)
        ]

    result["category"] = np.where(
        result["difference"] >= 5,
        "Safe",
        np.where(result["difference"] >= 2, "Moderate", "Reach"),
    )

    result = result.sort_values(by="cutoff", ascending=False)

    cols = [
        "college_code",
        "college_name",
        "district",
        "college_type",
        "branch_code",
        "branch_name",
        "cutoff",
        "difference",
        "category",
    ]
    return result[[c for c in cols if c in result.columns]]


# =============================================================================
# UI HELPERS
# =============================================================================
def category_badge_html(category: str) -> str:
    emoji = CATEGORY_EMOJI.get(category, "")
    cls = f"badge-{category.lower()}"
    return f'<span class="{cls}">{emoji} {category}</span>'


def render_header():
    st.markdown(
        """
        <div class="main-header">
            <h1>🎓 TNEA College Allotment Intelligence</h1>
            <p>Find colleges and branches based on your cutoff, category, location and preferred department.</p>
            <span class="badge">Data-Driven College Recommendation System</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="app-footer">
            <strong>🎓 TNEA College Allotment Intelligence</strong><br>
            Data-driven college exploration system<br>
            Built with Python • Pandas • Streamlit • Plotly<br><br>
            © 2026 College Recommendation Project
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(df: pd.DataFrame, n_recs=None):
    total_colleges = df["college_name"].nunique()
    total_branches = len(df)
    total_districts = df["district"].nunique()
    recs = "—" if n_recs is None else f"{n_recs:,}"

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, value, label in [
        (c1, "🏫", f"{total_colleges:,}", "Total Colleges"),
        (c2, "🎓", f"{total_branches:,}", "Total Branches"),
        (c3, "📍", f"{total_districts}", "Districts"),
        (c4, "📊", recs, "Available Matches"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def plot_gap_chart(student_mark: float, college_cutoff: float, college_name: str):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=["College Cutoff", "Your Mark"],
            x=[college_cutoff, student_mark],
            orientation="h",
            marker_color=["#64748b", "#38bdf8"],
            text=[f"{college_cutoff:.2f}", f"{student_mark:.2f}"],
            textposition="auto",
            hovertemplate="%{y}: %{x:.2f}<extra></extra>",
        )
    )
    title = college_name[:50] + ("…" if len(college_name) > 50 else "")
    fig.update_layout(
        title=dict(text=f"Cutoff Gap — {title}", font=dict(size=14, color="#e2e8f0")),
        xaxis=dict(
            title="Marks",
            range=[0, max(student_mark, college_cutoff) * 1.08],
            gridcolor="#334155",
            color="#94a3b8",
        ),
        yaxis=dict(color="#94a3b8"),
        plot_bgcolor="rgba(15,23,42,0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        height=220,
        margin=dict(l=20, r=20, t=50, b=30),
        showlegend=False,
    )
    return fig


def plot_category_distribution(result: pd.DataFrame):
    counts = result["category"].value_counts().reindex(
        ["Safe", "Moderate", "Reach"], fill_value=0
    )
    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts.index.tolist(),
                values=counts.values.tolist(),
                hole=0.55,
                marker=dict(
                    colors=[CATEGORY_COLORS[c] for c in counts.index],
                    line=dict(color="#0f172a", width=2),
                ),
                textinfo="label+value",
                hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text="Recommendation Category Distribution",
            font=dict(size=14, color="#e2e8f0"),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(orientation="h", y=-0.05),
    )
    return fig


# =============================================================================
# PAGES
# =============================================================================
def page_home(df: pd.DataFrame):
    render_header()
    render_kpi_cards(df)

    st.markdown('<div class="section-title">👋 Welcome</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="summary-box">
            Use the <strong>sidebar</strong> to enter your cutoff mark and category,
            then click <strong>🔍 Find My Colleges</strong>.
            Start with <strong>All Districts</strong> and <strong>All Departments</strong>
            to see every eligible option, then narrow by city or branch.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📍 District-wise College Count (Top 12)")
        dist_counts = (
            df.groupby("district")["college_name"]
            .nunique()
            .sort_values(ascending=False)
            .head(12)
            .reset_index()
        )
        dist_counts.columns = ["District", "Colleges"]
        fig = px.bar(
            dist_counts, x="Colleges", y="District", orientation="h",
            color="Colleges", color_continuous_scale="Blues",
        )
        fig.update_layout(
            plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1"), height=380,
            margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### 🎓 Popular Branches (Top 12)")
        branch_counts = df["branch_name"].value_counts().head(12).reset_index()
        branch_counts.columns = ["Branch", "Count"]
        fig2 = px.bar(
            branch_counts, x="Count", y="Branch", orientation="h",
            color="Count", color_continuous_scale="Teal",
        )
        fig2.update_layout(
            plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1"), height=380,
            margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        <div class="disclaimer">
            <strong>Note:</strong> Recommendations use historical cutoff values in the dataset.
            Actual admission depends on counselling rounds, seats, rank and official TNEA rules.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


def page_college_finder(df: pd.DataFrame):
    render_header()

    mark = float(st.session_state.get("pref_mark", 150.0))
    caste = st.session_state.get("pref_caste", "BC")
    district = st.session_state.get("pref_district", "All Districts")
    branch = st.session_state.get("pref_branch", "All Departments")
    n_results = int(st.session_state.get("pref_n_results", 20))
    run_search = st.session_state.get("run_search", False)

    if not run_search:
        render_kpi_cards(df, None)
        st.markdown(
            """
            <div class="empty-state">
                <h3>🎯 Ready to find your colleges</h3>
                <p>
                    1. Enter your <strong>Cutoff Mark</strong> in the sidebar<br>
                    2. Select your <strong>Community / Category</strong><br>
                    3. Keep District &amp; Department as <strong>All</strong> for first search<br>
                    4. Click <strong>🔍 Find My Colleges</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_footer()
        return

    # ----- Run recommendation -----
    try:
        result = student_college_recommendation(
            df=df,
            mark=mark,
            caste=caste,
            district=None if district == "All Districts" else district,
            branch=None if branch == "All Departments" else branch,
        )
    except ValueError as e:
        st.error(str(e))
        render_footer()
        return
    except Exception as e:
        st.error(f"Error computing recommendations: {e}")
        render_footer()
        return

    st.session_state["last_n_recs"] = len(result)
    render_kpi_cards(df, len(result))

    st.markdown(
        f"""
        <div class="summary-box">
            <strong>Cutoff:</strong> {mark} &nbsp;|&nbsp;
            <strong>Category:</strong> {caste} &nbsp;|&nbsp;
            <strong>District:</strong> {district} &nbsp;|&nbsp;
            <strong>Department:</strong> {branch}<br>
            <strong>Matches found:</strong> {len(result):,}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----- Empty results: explain + show broader alternatives -----
    if result.empty:
        st.markdown(
            """
            <div class="empty-state">
                <h3>No matching colleges found</h3>
                <p>
                    No college–branch in the dataset matches <strong>all</strong> of your filters
                    with cutoff ≤ your mark for this category.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Diagnostics: how many matches if we loosen filters
        without_branch = student_college_recommendation(
            df, mark, caste,
            district=None if district == "All Districts" else district,
            branch=None,
        )
        without_district = student_college_recommendation(
            df, mark, caste,
            district=None,
            branch=None if branch == "All Departments" else branch,
        )
        without_both = student_college_recommendation(
            df, mark, caste, district=None, branch=None
        )

        st.markdown(
            f"""
            <div class="hint-box">
                <strong>💡 Why 0 results?</strong><br>
                • With your mark + category only: <strong>{len(without_both):,}</strong> matches<br>
                • Same district, any department: <strong>{len(without_branch):,}</strong> matches<br>
                • Same department, any district: <strong>{len(without_district):,}</strong> matches<br><br>
                Tip: Set <strong>Preferred District</strong> or <strong>Preferred Department</strong>
                back to <strong>All</strong>, then click Find again.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show best available alternative list (without both filters)
        if not without_both.empty:
            st.markdown(
                '<div class="section-title">⭐ Available options (all districts & departments)</div>',
                unsafe_allow_html=True,
            )
            show_alt = without_both.head(n_results)
            _show_results_table(show_alt, mark)
            csv_bytes = show_alt.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download These Results as CSV",
                data=csv_bytes,
                file_name="tnea_recommendations_all.csv",
                mime="text/csv",
            )
        render_footer()
        return

    # ----- Post filters -----
    st.markdown('<div class="section-title">🎛️ Refine Results</div>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        search_q = st.text_input("🔎 Search", placeholder="College / branch / district…")
    with f2:
        filter_district = st.selectbox(
            "District",
            ["All"] + sorted(result["district"].unique().tolist()),
            key="rf_district",
        )
    with f3:
        filter_type = st.selectbox(
            "College Type",
            ["All"] + sorted(result["college_type"].unique().tolist()),
            key="rf_type",
        )
    with f4:
        filter_cat = st.selectbox(
            "Category", ["All", "Safe", "Moderate", "Reach"], key="rf_cat"
        )

    filtered = result.copy()
    if search_q.strip():
        q = search_q.strip().lower()
        filtered = filtered[
            filtered["college_name"].str.lower().str.contains(q, na=False)
            | filtered["branch_name"].str.lower().str.contains(q, na=False)
            | filtered["district"].str.lower().str.contains(q, na=False)
        ]
    if filter_district != "All":
        filtered = filtered[filtered["district"] == filter_district]
    if filter_type != "All":
        filtered = filtered[filtered["college_type"] == filter_type]
    if filter_cat != "All":
        filtered = filtered[filtered["category"] == filter_cat]

    display_df = filtered.head(n_results)

    if display_df.empty:
        st.warning("No rows match the refine filters. Clear search or set filters to All.")
        render_footer()
        return

    # Charts
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(plot_category_distribution(filtered), use_container_width=True)
    with ch2:
        top_row = display_df.iloc[0]
        st.plotly_chart(
            plot_gap_chart(mark, float(top_row["cutoff"]), str(top_row["college_name"])),
            use_container_width=True,
        )
        st.caption(
            f"Top match difference: **+{top_row['difference']:.2f}** ({top_row['category']})"
        )

    # Top cards
    st.markdown('<div class="section-title">⭐ Top College Matches</div>', unsafe_allow_html=True)
    top_n = min(6, len(display_df))
    cols = st.columns(min(3, top_n))
    for i in range(top_n):
        row = display_df.iloc[i]
        badge = category_badge_html(row["category"])
        name = str(row["college_name"])
        short = name[:55] + ("…" if len(name) > 55 else "")
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="rec-card">
                    <div class="rec-college">🏫 {short}</div>
                    <div class="rec-meta">📍 {row['district']} · {row['college_type']}</div>
                    <div class="rec-meta">🎓 {row['branch_name']}</div>
                    <div class="rec-stats">
                        <span class="rec-stat-item">📈 Cutoff: <strong>{row['cutoff']:.2f}</strong></span>
                        <span class="rec-stat-item">➕ Diff: <strong>+{row['difference']:.2f}</strong></span>
                        <span>{badge}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">🎯 Your College Matches</div>', unsafe_allow_html=True)
    _show_results_table(display_df, mark)

    top = display_df.iloc[0]
    st.info(
        f"**Cutoff:** {top['cutoff']:.2f}  |  **Your Mark:** {mark:.2f}  |  "
        f"**Difference:** +{top['difference']:.2f}  |  **Category:** {top['category']}\n\n"
        f"Your mark is **{top['difference']:.2f}** marks above this historical cutoff. "
        f"This does **not** guarantee admission."
    )

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Results as CSV",
        data=csv_bytes,
        file_name="tnea_college_recommendations.csv",
        mime="text/csv",
    )

    st.markdown(
        """
        <div class="disclaimer">
            <strong>Note:</strong> Based on dataset cutoffs only. Official TNEA counselling
            decides final allotment.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


def _show_results_table(display_df: pd.DataFrame, mark: float):
    show = display_df.copy()
    show["Student Mark"] = mark
    show = show.rename(
        columns={
            "college_code": "Code",
            "college_name": "College",
            "district": "District",
            "college_type": "Type",
            "branch_code": "Branch Code",
            "branch_name": "Department",
            "cutoff": "Cutoff",
            "difference": "Difference",
            "category": "Category",
        }
    )
    show["Cutoff"] = show["Cutoff"].round(2)
    show["Difference"] = show["Difference"].round(2)
    cols = [
        "Code", "College", "District", "Type", "Department",
        "Cutoff", "Student Mark", "Difference", "Category",
    ]
    st.dataframe(show[[c for c in cols if c in show.columns]], use_container_width=True, height=420)


def page_analytics(df: pd.DataFrame):
    render_header()
    st.markdown('<div class="section-title">📊 Dataset Analytics</div>', unsafe_allow_html=True)

    caste_cols = [c for c in ["oc", "bc", "bcm", "mbc", "sc", "sca", "st"] if c in df.columns]

    st.markdown("##### Cutoff Distribution by Category")
    melted = df[caste_cols].melt(var_name="Category", value_name="Cutoff").dropna()
    melted["Category"] = melted["Category"].str.upper()
    fig = px.box(
        melted, x="Category", y="Cutoff", color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"), height=400, showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Category-wise Mean Cutoff")
        means = df[caste_cols].mean().sort_values(ascending=False).reset_index()
        means.columns = ["Category", "Mean Cutoff"]
        means["Category"] = means["Category"].str.upper()
        fig2 = px.bar(
            means, x="Category", y="Mean Cutoff", color="Mean Cutoff",
            color_continuous_scale="Viridis",
        )
        fig2.update_layout(
            plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1"), height=360, coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown("##### College Type Distribution")
        type_counts = df["college_type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig3 = px.pie(
            type_counts, names="Type", values="Count", hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"),
            height=360, margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("##### District-wise Branch Records (Top 15)")
    dist_branch = df["district"].value_counts().head(15).reset_index()
    dist_branch.columns = ["District", "Records"]
    fig4 = px.bar(
        dist_branch, x="District", y="Records", color="Records",
        color_continuous_scale="Blues",
    )
    fig4.update_layout(
        plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"), height=380, coloraxis_showscale=False,
        xaxis_tickangle=-40, margin=dict(l=20, r=20, t=20, b=80),
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("##### Branch Popularity (Top 15)")
    br = df["branch_name"].value_counts().head(15).reset_index()
    br.columns = ["Branch", "Count"]
    fig5 = px.bar(
        br, x="Count", y="Branch", orientation="h", color="Count",
        color_continuous_scale="Tealgrn",
    )
    fig5.update_layout(
        plot_bgcolor="rgba(15,23,42,0.6)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1"), height=420, coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig5, use_container_width=True)
    render_footer()


def page_explore(df: pd.DataFrame):
    render_header()
    st.markdown('<div class="section-title">📚 Explore Full Dataset</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        d_sel = st.selectbox(
            "District",
            ["All"] + sorted(df["district"].dropna().unique().tolist()),
            key="ex_district",
        )
    with c2:
        t_sel = st.selectbox(
            "College Type",
            ["All"] + sorted(df["college_type"].dropna().unique().tolist()),
            key="ex_type",
        )
    with c3:
        b_sel = st.selectbox(
            "Department",
            ["All"] + sorted(df["branch_name"].dropna().unique().tolist()),
            key="ex_branch",
        )
    with c4:
        search_ex = st.text_input("🔎 Search", placeholder="College or branch…", key="ex_search")

    view = df.copy()
    if d_sel != "All":
        view = view[view["district"] == d_sel]
    if t_sel != "All":
        view = view[view["college_type"] == t_sel]
    if b_sel != "All":
        view = view[view["branch_name"] == b_sel]
    if search_ex.strip():
        q = search_ex.strip().lower()
        view = view[
            view["college_name"].str.lower().str.contains(q, na=False)
            | view["branch_name"].str.lower().str.contains(q, na=False)
        ]

    st.caption(f"Showing **{len(view):,}** of **{len(df):,}** records")
    display_cols = [
        c for c in [
            "college_code", "college_name", "district", "college_type",
            "branch_code", "branch_name", "oc", "bc", "bcm", "mbc", "sc", "sca", "st",
        ]
        if c in view.columns
    ]
    st.dataframe(view[display_cols], use_container_width=True, height=500)
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=view[display_cols].to_csv(index=False).encode("utf-8"),
        file_name="tnea_explore_filtered.csv",
        mime="text/csv",
    )
    render_footer()


def page_about():
    render_header()
    st.markdown('<div class="section-title">ℹ️ About the Project</div>', unsafe_allow_html=True)
    st.markdown(
        """
        **TNEA College Allotment Intelligence** helps students explore colleges using
        historical cutoff data by mark, category, district and department.

        #### How recommendations work
        1. Enter your cutoff mark and community (OC / BC / BCM / MBC / SC / SCA / ST)
        2. Optionally choose district and department
        3. System keeps rows where **category cutoff ≤ your mark**
        4. **Difference** = your mark − college cutoff
        5. Categories:
           - **Safe** — difference ≥ 5  
           - **Moderate** — difference ≥ 2 and &lt; 5  
           - **Reach** — difference &lt; 2  
        6. Results sorted by cutoff (highest first)

        #### Stack
        Python · Pandas · NumPy · Streamlit · Plotly

        #### Dataset
        `tnea_cutoffs.csv` — college, district, type, branch, and category cutoffs.
        Missing cutoffs are skipped for that category.
        """
    )
    st.markdown(
        """
        <div class="disclaimer">
            For educational / portfolio use only. Not an official TNEA allotment tool.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


# =============================================================================
# MAIN
# =============================================================================
def main():
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.info(
            "Put `tnea_cutoffs.csv` in the same folder as `app.py`, then restart:\n\n"
            "`streamlit run app.py`"
        )
        st.stop()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

    # Init session defaults
    defaults = {
        "pref_mark": 150.0,
        "pref_caste": "BC",
        "pref_district": "All Districts",
        "pref_branch": "All Departments",
        "pref_n_results": 20,
        "run_search": False,
        "nav_to_finder": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Go to",
            [
                "🏠 Home",
                "🎯 College Finder",
                "📊 Analytics",
                "📚 Explore Colleges",
                "ℹ️ About Project",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("### 🎯 Student Preferences")

        mark = st.number_input(
            "Cutoff Mark",
            min_value=0.0,
            max_value=200.0,
            value=float(st.session_state["pref_mark"]),
            step=0.5,
            help="Your community cutoff / mark (0–200).",
        )

        caste_options = list(CASTE_MAPPING.keys())
        caste_idx = (
            caste_options.index(st.session_state["pref_caste"])
            if st.session_state["pref_caste"] in caste_options
            else 1
        )
        caste = st.selectbox("Community / Category", caste_options, index=caste_idx)

        districts = ["All Districts"] + sorted(df["district"].dropna().unique().tolist())
        # Default index 0 = All Districts (important so users always get results first)
        d_cur = st.session_state.get("pref_district", "All Districts")
        d_idx = districts.index(d_cur) if d_cur in districts else 0
        district = st.selectbox("Preferred District", districts, index=d_idx)

        branches = ["All Departments"] + sorted(df["branch_name"].dropna().unique().tolist())
        b_cur = st.session_state.get("pref_branch", "All Departments")
        b_idx = branches.index(b_cur) if b_cur in branches else 0
        branch = st.selectbox("Preferred Department", branches, index=b_idx)

        n_results = st.slider(
            "Number of results",
            min_value=5,
            max_value=50,
            value=int(st.session_state["pref_n_results"]),
            step=5,
        )

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            find_clicked = st.button("🔍 Find My Colleges", use_container_width=True)
        with col_b:
            reset_clicked = st.button("🔄 Reset Filters", use_container_width=True)

        if find_clicked:
            if mark < 0 or mark > 200:
                st.error("⚠️ Please enter a valid cutoff mark (0–200).")
            else:
                st.session_state["pref_mark"] = float(mark)
                st.session_state["pref_caste"] = caste
                st.session_state["pref_district"] = district
                st.session_state["pref_branch"] = branch
                st.session_state["pref_n_results"] = int(n_results)
                st.session_state["run_search"] = True
                st.session_state["nav_to_finder"] = True
                st.rerun()

        if reset_clicked:
            st.session_state["pref_mark"] = 150.0
            st.session_state["pref_caste"] = "BC"
            st.session_state["pref_district"] = "All Districts"
            st.session_state["pref_branch"] = "All Departments"
            st.session_state["pref_n_results"] = 20
            st.session_state["run_search"] = False
            st.session_state["last_n_recs"] = None
            st.rerun()

        # Keep latest widget values in session (without forcing search)
        st.session_state["pref_mark"] = float(mark)
        st.session_state["pref_caste"] = caste
        st.session_state["pref_district"] = district
        st.session_state["pref_branch"] = branch
        st.session_state["pref_n_results"] = int(n_results)

        st.markdown("---")
        st.caption(
            "Tip: First search with **All Districts** + **All Departments**, "
            "then narrow filters."
        )

    if st.session_state.get("nav_to_finder"):
        page = "🎯 College Finder"
        st.session_state["nav_to_finder"] = False

    if page == "🏠 Home":
        page_home(df)
    elif page == "🎯 College Finder":
        page_college_finder(df)
    elif page == "📊 Analytics":
        page_analytics(df)
    elif page == "📚 Explore Colleges":
        page_explore(df)
    else:
        page_about()


if __name__ == "__main__":
    main()