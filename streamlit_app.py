
import streamlit as st
from datetime import datetime
from src.pipelines.pipeline import research_pipeline


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchOS | AI Research Workspace",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #101114;
        color: #f4f4f5;
    }

    [data-testid="stSidebar"] {
        background: #17181d;
        border-right: 1px solid #292a31;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #d4d4d8;
    }

    .brand {
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #a1a1aa;
        font-size: 14px;
        line-height: 1.6;
    }

    .hero {
        text-align: center;
        padding: 50px 0 24px 0;
    }

    .hero h1 {
        font-size: clamp(32px, 4vw, 48px);
        font-weight: 700;
        letter-spacing: -2px;
        color: #fafafa;
        margin-bottom: 12px;
    }

    .hero p {
        color: #a1a1aa;
        font-size: 16px;
    }

    .panel {
        background: #191a20;
        border: 1px solid #30313a;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .eyebrow {
        color: #a1a1aa;
        font-size: 11px;
        letter-spacing: 1.5px;
        font-weight: 600;
        text-transform: uppercase;
    }

    div[data-testid="stMetric"] {
        background: #191a20;
        border: 1px solid #30313a;
        border-radius: 12px;
        padding: 16px;
    }

    .stButton > button[kind="primary"] {
        background: #c4b5fd;
        color: #18181b;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    .stButton > button[kind="primary"]:hover {
        background: #a78bfa;
        color: #18181b;
    }

    .stTextArea textarea {
        background: #191a20;
        color: #fafafa;
        border: 1px solid #383943;
        border-radius: 12px;
    }

    [data-testid="stExpander"] {
        background: #191a20;
        border: 1px solid #30313a;
        border-radius: 12px;
    }

    hr {
        border-color: #30313a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">◈ ResearchOS</div>',
        unsafe_allow_html=True,
    )
    st.caption("MULTI-AGENT RESEARCH WORKSPACE")

    st.divider()

    if st.button("＋  New research", use_container_width=True):
        st.session_state.current_result = None
        st.session_state.current_topic = ""
        st.rerun()

    st.markdown("#### YOUR WORKFLOW")

    workflow = [
        ("01", "Web search", "Find relevant information"),
        ("02", "Page scraper", "Extract detailed content"),
        ("03", "Report writer", "Synthesize the findings"),
        ("04", "AI critic", "Evaluate report quality"),
    ]

    for number, name, description in workflow:
        st.markdown(
            f"""
            <div style="
                padding: 10px 0;
                border-bottom: 1px solid #30313a;
            ">
                <div style="font-size:13px;color:#e4e4e7;">
                    <span style="color:#c4b5fd;">{number}</span>
                    &nbsp;&nbsp;{name}
                </div>
                <div style="
                    font-size:11px;
                    color:#a1a1aa;
                    margin:4px 0 0 30px;
                ">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("#### RECENT RESEARCH")

    if not st.session_state.research_history:
        st.caption("Your completed research will appear here.")
    else:
        for index, item in enumerate(
            reversed(st.session_state.research_history)
        ):
            if st.button(
                item["topic"][:38],
                key=f"history_{index}",
                use_container_width=True,
            ):
                st.session_state.current_result = item["result"]
                st.session_state.current_topic = item["topic"]
                st.rerun()

    st.divider()
    st.caption("Powered by Gemini · LangChain · Tavily")


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>Research anything.</h1>
        <p>
            Deploy your AI research team to search, read,
            synthesize, and evaluate information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# RESEARCH INPUT
# --------------------------------------------------

with st.container():
    st.markdown(
        '<div class="eyebrow">START A RESEARCH TASK</div>',
        unsafe_allow_html=True,
    )

    with st.form("research_form"):
        topic = st.text_area(
            "Research topic",
            value=st.session_state.current_topic,
            placeholder=(
                "Example: Latest advancements in AI agents, "
                "their applications, limitations, and market trends..."
            ),
            height=120,
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            st.caption(
                "Your agents will search the web, scrape source "
                "pages, write a report, and critique the result."
            )

        with col2:
            submitted = st.form_submit_button(
                "Run research  ↗",
                type="primary",
                use_container_width=True,
            )


# --------------------------------------------------
# EXECUTE RESEARCH
# --------------------------------------------------

if submitted:
    if not topic.strip():
        st.warning("Enter a research topic first.")
    else:
        st.session_state.current_topic = topic.strip()

        try:
            with st.status(
                "Your research team is working...",
                expanded=True,
            ) as status:
                st.write("Preparing research workflow...")
                st.write("Searching and gathering information...")

                # Execute the actual existing pipeline.
                result = research_pipeline(topic.strip())

                status.update(
                    label="Research workflow completed",
                    state="complete",
                    expanded=False,
                )

            st.session_state.current_result = result

            st.session_state.research_history.append({
                "topic": topic.strip(),
                "result": result,
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
            })

        except Exception as exc:
            st.error(
                "The research pipeline failed. Check the terminal "
                "logs and verify your API keys and agent configuration."
            )
            # Technical details stay in the server logs.
            print(f"Research pipeline error: {exc}")


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

result = st.session_state.current_result
current_topic = st.session_state.current_topic

if result:
    st.divider()

    st.markdown(
        f"### Research report\n**Topic:** {current_topic}"
    )

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    st.caption(f"Research workspace · {created_at}")

    search_results = result.get("search_results", "")
    scraped_content = result.get("scraped_content", "")
    report = result.get("report", "")
    critique = result.get("critique", "")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Workflow stages", "4")

    with col2:
        st.metric(
            "Search results",
            "Available" if search_results else "Missing",
        )

    with col3:
        st.metric(
            "Source content",
            "Available" if scraped_content else "Missing",
        )

    with col4:
        st.metric(
            "Report critique",
            "Available" if critique else "Missing",
        )

    st.write("")

    tab_report, tab_critique, tab_sources, tab_activity = st.tabs([
        "📄 Research report",
        "🧠 Critique",
        "🔎 Research evidence",
        "⚙️ Workflow details",
    ])

    with tab_report:
        if report:
            st.markdown(report)

            st.download_button(
                "Download report as Markdown",
                data=f"# {current_topic}\n\n{report}",
                file_name="research_report.md",
                mime="text/markdown",
                type="primary",
            )
        else:
            st.info("The writer did not return a report.")

    with tab_critique:
        if critique:
            st.markdown(critique)
        else:
            st.info("No critique is available.")

    with tab_sources:
        st.markdown("#### Web search results")
        if search_results:
            st.text(search_results)
        else:
            st.info("No search results were returned.")

        st.divider()

        st.markdown("#### Scraped content")
        if scraped_content:
            st.text(scraped_content)
        else:
            st.info("No scraped content was returned.")

    with tab_activity:
        st.markdown("#### Workflow execution")

        stages = [
            ("01", "Web search", search_results),
            ("02", "Page scraping", scraped_content),
            ("03", "Report writing", report),
            ("04", "Report critique", critique),
        ]

        for number, title, content in stages:
            with st.expander(
                f"{number} · {title}",
                expanded=False,
            ):
                if content:
                    st.success("Output available")
                    st.caption(f"{len(content):,} characters")
                else:
                    st.warning("No output available")

    st.caption(
        "AI-generated research may contain inaccuracies. "
        "Verify important claims against the original sources."
    )

else:
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="panel">
                <div style="font-size:22px;">⌕</div>
                <h4>Search the web</h4>
                <p class="subtitle">
                    Discover relevant information using your
                    Tavily-powered search agent.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="panel">
                <div style="font-size:22px;">▤</div>
                <h4>Read and synthesize</h4>
                <p class="subtitle">
                    Extract webpage content and create a
                    structured research report.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="panel">
                <div style="font-size:22px;">✓</div>
                <h4>Evaluate quality</h4>
                <p class="subtitle">
                    Ask a separate AI critic to identify
                    strengths and areas for improvement.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
