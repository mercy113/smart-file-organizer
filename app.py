import streamlit as st
from pathlib import Path
from datetime import datetime
import subprocess
import json
import os
import signal
import textwrap


def render_html(content):
    """Render HTML without unwanted Markdown indentation."""
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True,
    )



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path("/mnt/d/smart-file-organizer")

ORGANIZER = BASE_DIR / "organizer.py"
DUPLICATE_FINDER = BASE_DIR / "duplicate_finder.py"
METADATA = BASE_DIR / "metadata.py"
BENCHMARK = BASE_DIR / "benchmark.py"
MONITOR = BASE_DIR / "file_monitor.py"
RECOVERY = BASE_DIR / "recovery.py"
RUN_SCRIPT = BASE_DIR / "run_organizer.sh"

HISTORY_FILE = BASE_DIR / "logs" / "move_history.json"


# ============================================================
# DARK PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    /* ================= GLOBAL ================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(37, 99, 235, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.12),
                transparent 30%
            ),
            #070b16;

        color: #e5e7eb;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: #080d19;
        border-right: 1px solid rgba(96,165,250,.12);
    }

    section[data-testid="stSidebar"] * {
        color: #cbd5e1;
    }

    /* ================= HERO ================= */

    .hero {
        position: relative;
        padding: 38px;
        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,.98),
                rgba(17,24,39,.94)
            );

        border: 1px solid rgba(96,165,250,.16);

        box-shadow:
            0 25px 70px rgba(0,0,0,.35);

        overflow: hidden;
        margin-bottom: 28px;
    }

    .hero::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;

        height: 4px;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #7c3aed,
                #facc15
            );
    }

    .hero-label {
        color: #60a5fa;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 850;
        line-height: 1.05;
        color: #f8fafc;
        margin-top: 10px;
    }

    .gradient-text {
        background:
            linear-gradient(
                90deg,
                #60a5fa,
                #a78bfa,
                #facc15
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #94a3b8;
        font-size: 1rem;
        max-width: 850px;
        line-height: 1.6;
        margin-top: 14px;
    }

    /* ================= STATUS ================= */

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 7px 13px;

        border-radius: 999px;

        background: rgba(34,197,94,.08);
        border: 1px solid rgba(34,197,94,.22);

        color: #86efac;

        font-size: .8rem;
        font-weight: 700;

        margin-top: 18px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 12px #22c55e;
    }

    /* ================= SECTION ================= */

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 28px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: .88rem;
        margin-bottom: 18px;
    }

    /* ================= METRICS ================= */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,.98),
                rgba(17,24,39,.94)
            );

        border: 1px solid rgba(96,165,250,.13);

        border-radius: 18px;

        padding: 21px;

        min-height: 115px;

        box-shadow:
            0 15px 40px rgba(0,0,0,.2);
    }

    .metric-icon {
        font-size: 1.3rem;
    }

    .metric-label {
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: .72rem;
        font-weight: 700;
        margin-top: 5px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 850;
        margin-top: 5px;
    }

    /* ================= FEATURE CARDS ================= */

    .feature-card {
        background:
            linear-gradient(
                145deg,
                rgba(17,27,52,.95),
                rgba(11,18,35,.98)
            );

        border: 1px solid rgba(96,165,250,.14);

        border-radius: 20px;

        padding: 25px;

        min-height: 190px;

        box-shadow:
            0 15px 40px rgba(0,0,0,.23);
    }

    .feature-icon {
        font-size: 2rem;
    }

    .feature-title {
        color: #f8fafc;
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: 8px;
    }

    .feature-text {
        color: #94a3b8;
        font-size: .87rem;
        line-height: 1.55;
        margin-top: 7px;
    }

    /* ================= TECHNOLOGY ================= */

    .tech-card {
        padding: 15px;
        text-align: center;

        background: rgba(15,23,42,.85);

        border: 1px solid rgba(96,165,250,.12);

        border-radius: 14px;

        color: #cbd5e1;

        font-size: .85rem;
        font-weight: 700;
    }

    /* ================= BUTTONS ================= */

    .stButton > button {
        width: 100%;

        min-height: 46px;

        border-radius: 12px;

        background: #111c34;

        border: 1px solid rgba(96,165,250,.2);

        color: #e2e8f0;

        font-weight: 750;

        transition: all .2s ease;
    }

    .stButton > button:hover {
        background: #172554;
        border-color: #60a5fa;
        color: white;
        transform: translateY(-1px);
    }

    /* ================= INPUTS ================= */

    div[data-baseweb="input"] {
        background: #0f172a;
        border-radius: 12px;
    }

    /* ================= CODE ================= */

    code {
        color: #93c5fd;
    }

    /* ================= FOOTER ================= */

    .footer {
        text-align: center;
        color: #475569;
        padding: 40px 0 10px;
        font-size: .78rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "monitor_process" not in st.session_state:
    st.session_state.monitor_process = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_script(script, folder=None):

    try:

        input_data = ""

        if folder:
            input_data = str(folder) + "\n"

        result = subprocess.run(
            ["python3", str(script)],
            input=input_data,
            text=True,
            capture_output=True,
            cwd=str(BASE_DIR),
            timeout=120
        )

        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired:

        return (
            "",
            "Process timed out.",
            1
        )

    except Exception as e:

        return (
            "",
            str(e),
            1
        )


def get_files(folder):

    path = Path(folder)

    if not path.exists():
        return []

    return [
        f
        for f in path.rglob("*")
        if f.is_file()
    ]


def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    except Exception:

        return []


def count_categories(folder):

    files = get_files(folder)

    categories = {
        "Documents": 0,
        "Images": 0,
        "Videos": 0,
        "Audio": 0,
        "Archives": 0,
        "Others": 0
    }

    extensions = {
        "Documents": [
            ".pdf", ".doc", ".docx",
            ".txt", ".csv"
        ],

        "Images": [
            ".jpg", ".jpeg",
            ".png", ".gif"
        ],

        "Videos": [
            ".mp4", ".mkv",
            ".avi", ".mov"
        ],

        "Audio": [
            ".mp3", ".wav", ".flac"
        ],

        "Archives": [
            ".zip", ".rar", ".7z"
        ]
    }

    for file in files:

        ext = file.suffix.lower()

        found = False

        for category, exts in extensions.items():

            if ext in exts:

                categories[category] += 1
                found = True
                break

        if not found:
            categories["Others"] += 1

    return categories


def navigate(page):

    st.session_state.page = page


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:1.35rem;
            font-weight:850;
            color:#f8fafc;
        ">
        📁 Smart File Organizer
        </div>

        <div style="
            color:#64748b;
            margin-top:6px;
            font-size:.82rem;
        ">
        Intelligent Linux File Management
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("NAVIGATION")

    if st.button(
        "🏠  Dashboard",
        use_container_width=True
    ):
        navigate("Dashboard")

    st.markdown(
        "**CORE OPERATIONS**"
    )

    if st.button(
        "📂  File Organizer",
        use_container_width=True
    ):
        navigate("Organizer")

    if st.button(
        "🔍  Duplicate Finder",
        use_container_width=True
    ):
        navigate("Duplicates")

    if st.button(
        "📄  File Intelligence",
        use_container_width=True
    ):
        navigate("Metadata")

    if st.button(
        "⚡  Performance",
        use_container_width=True
    ):
        navigate("Benchmark")

    st.markdown(
        "**AUTOMATION & MONITORING**"
    )

    if st.button(
        "👀  File Monitor",
        use_container_width=True
    ):
        navigate("Monitor")

    if st.button(
        "⏰  Cron Automation",
        use_container_width=True
    ):
        navigate("Cron")

    st.markdown(
        "**RECOVERY**"
    )

    if st.button(
        "↩️  Recovery Center",
        use_container_width=True
    ):
        navigate("Recovery")

    st.markdown(
        "**SYSTEM**"
    )

    if st.button(
        "⚙️  Project Info",
        use_container_width=True
    ):
        navigate("Project Info")

    st.divider()

    st.success("● SYSTEM ONLINE")

    st.caption("Linux / WSL2")
    st.caption("Python 3")
    st.caption("Streamlit")


# ============================================================
# COMMON WORKSPACE
# ============================================================

workspace = st.text_input(
    "Workspace",
    value="/mnt/d/organizer-demo",
    label_visibility="collapsed"
)

workspace_path = Path(workspace)

files = get_files(workspace)

total_files = len(files)

total_size = sum(
    f.stat().st_size
    for f in files
    if f.exists()
)

history = load_history()

categories = count_categories(workspace)


# ============================================================
# HERO
# ============================================================

# ============================================================
# DASHBOARD HERO
# ============================================================

if st.session_state.page == "Dashboard":
    st.html("""
        <div class="hero">
            <div class="hero-label">
                AI • AUTOMATION • FILE SYSTEM
            </div>

            <div class="hero-title">
                Smart <span class="gradient-text">File Organizer</span>
            </div>

            <div class="hero-description">
                Intelligent Linux-based file management platform
                for automated organization, duplicate detection,
                metadata analysis, performance benchmarking,
                real-time monitoring and recovery.
            </div>

            <div class="status">
                <span class="status-dot"></span>
                SYSTEM ONLINE
            </div>
        </div>
    """)
    # ============================================================
    # DASHBOARD
    # ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="section-title">📊 System Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Real-time workspace summary</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">📄</div>
                <div class="metric-label">
                    Total Files
                </div>
                <div class="metric-value">
                    {total_files}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💾</div>
                <div class="metric-label">
                    Storage
                </div>
                <div class="metric-value">
                    {total_size / 1024:.1f} KB
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">📜</div>
                <div class="metric-label">
                    Movements
                </div>
                <div class="metric-value">
                    {len(history)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🗂️</div>
                <div class="metric-label">
                    Categories
                </div>
                <div class="metric-value">
                    {sum(1 for x in categories.values() if x > 0)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # CORE OPERATIONS

    st.markdown(
        '<div class="section-title">🧩 Core Operations</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">File processing and intelligence tools</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📂</div>
                <div class="feature-title">
                    File Organizer
                </div>
                <div class="feature-text">
                    Automatically categorize files into
                    Documents, Images, Videos, Audio,
                    Archives and Others.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN ORGANIZER →",
            key="dashboard_organizer"
        ):
            navigate("Organizer")
            st.rerun()

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">
                    Duplicate Finder
                </div>
                <div class="feature-text">
                    Detect identical files using
                    SHA-256 content hashing.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN DUPLICATE FINDER →",
            key="dashboard_duplicate"
        ):
            navigate("Duplicates")
            st.rerun()

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">
                    File Intelligence
                </div>
                <div class="feature-text">
                    Inspect file size, extensions,
                    modification dates and metadata.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN FILE INTELLIGENCE →",
            key="dashboard_metadata"
        ):
            navigate("Metadata")
            st.rerun()

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">
                    Performance Benchmark
                </div>
                <div class="feature-text">
                    Measure file processing performance
                    and compare execution modes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN PERFORMANCE →",
            key="dashboard_benchmark"
        ):
            navigate("Benchmark")
            st.rerun()

    # AUTOMATION

    st.markdown(
        '<div class="section-title">⚙️ Automation & Monitoring</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">👀</div>
                <div class="feature-title">
                    Real-Time File Monitor
                </div>
                <div class="feature-text">
                    Monitor a folder and detect new files
                    automatically.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN FILE MONITOR →",
            key="dashboard_monitor"
        ):
            navigate("Monitor")
            st.rerun()

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⏰</div>
                <div class="feature-title">
                    Cron Automation
                </div>
                <div class="feature-text">
                    Schedule automatic organization jobs
                    using Linux cron.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN CRON AUTOMATION →",
            key="dashboard_cron"
        ):
            navigate("Cron")
            st.rerun()

    # RECOVERY

    st.markdown(
        '<div class="section-title">↩️ Recovery Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">↩️</div>
            <div class="feature-title">
                Recovery & Movement History
            </div>
            <div class="feature-text">
                Review previous file movements and
                safely undo the latest operation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "OPEN RECOVERY CENTER →",
        key="dashboard_recovery"
    ):
        navigate("Recovery")
        st.rerun()


# ============================================================
# ORGANIZER PAGE
# ============================================================

elif st.session_state.page == "Organizer":

    st.markdown(
        '<div class="section-title">📂 File Organizer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Automatically classify and move files into organized categories.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        f"Workspace: {workspace}"
    )

    if st.button(
        "🚀 RUN FILE ORGANIZER",
        key="run_organizer"
    ):

        with st.spinner(
            "Organizing files..."
        ):

            output, error, code = run_script(
                ORGANIZER,
                workspace
            )

        if code == 0:

            st.success(
                "File organization completed successfully."
            )

            if output:
                st.code(
                    output,
                    language="text"
                )

        else:

            st.error(
                "Organizer encountered an error."
            )

            if error:
                st.code(
                    error,
                    language="text"
                )

    st.markdown("### 📊 Categories")

    cols = st.columns(3)

    for i, (category, count) in enumerate(
        categories.items()
    ):

        with cols[i % 3]:

            st.metric(
                category,
                count
            )


# ============================================================
# DUPLICATE FINDER
# ============================================================

elif st.session_state.page == "Duplicates":

    st.markdown(
        '<div class="section-title">🔍 Duplicate Finder</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        SHA-256 based content comparison for identifying
        duplicate files.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔎 SCAN FOR DUPLICATES",
        key="scan_duplicates"
    ):

        with st.spinner(
            "Scanning files using SHA-256..."
        ):

            output, error, code = run_script(
                DUPLICATE_FINDER,
                workspace
            )

        if output:
            st.code(
                output,
                language="text"
            )

        if error:
            st.error(error)

        if code == 0:
            st.success(
                "Duplicate scan completed."
            )


# ============================================================
# METADATA PAGE
# ============================================================

elif st.session_state.page == "Metadata":

    st.markdown(
        '<div class="section-title">📄 File Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Analyze file names, extensions, sizes and modification times.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "📊 ANALYZE FILE METADATA",
        key="metadata_button"
    ):

        with st.spinner(
            "Reading file metadata..."
        ):

            output, error, code = run_script(
                METADATA,
                workspace
            )

        if output:

            st.code(
                output,
                language="text"
            )

        if error:

            st.error(error)


# ============================================================
# BENCHMARK PAGE
# ============================================================

elif st.session_state.page == "Benchmark":

    st.markdown(
        '<div class="section-title">⚡ Performance Benchmark</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Measure the performance of your file processing implementation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "The benchmark uses the project's benchmark.py implementation."
    )

    if st.button(
        "🏁 RUN PERFORMANCE BENCHMARK",
        key="benchmark_button"
    ):

        with st.spinner(
            "Running benchmark..."
        ):

            output, error, code = run_script(
                BENCHMARK,
                workspace
            )

        if output:

            st.code(
                output,
                language="text"
            )

        if error:

            st.error(error)


# ============================================================
# FILE MONITOR
# ============================================================

elif st.session_state.page == "Monitor":

    st.markdown(
        '<div class="section-title">👀 Real-Time File Monitor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Monitor a directory for newly created files.
        </div>
        """,
        unsafe_allow_html=True
    )

    process = st.session_state.monitor_process

    if process is not None:

        if process.poll() is None:

            st.success(
                "🟢 File monitor is currently running."
            )

        else:

            st.session_state.monitor_process = None

            st.info(
                "File monitor is not running."
            )

    else:

        st.info(
            "File monitor is currently stopped."
        )

    if st.button(
        "▶️ START FILE MONITOR",
        key="start_monitor"
    ):

        process = subprocess.Popen(
            ["python3", str(MONITOR)],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            cwd=str(BASE_DIR)
        )

        process.stdin.write(
            str(workspace) + "\n"
        )

        process.stdin.flush()

        st.session_state.monitor_process = process

        st.success(
            "File monitor started."
        )

        st.rerun()

    if st.button(
        "⏹️ STOP FILE MONITOR",
        key="stop_monitor"
    ):

        process = st.session_state.monitor_process

        if process is not None:

            if process.poll() is None:

                process.terminate()

            st.session_state.monitor_process = None

            st.success(
                "File monitor stopped."
            )

            st.rerun()

        else:

            st.info(
                "No active monitor process."
            )


# ============================================================
# CRON PAGE
# ============================================================

elif st.session_state.page == "Cron":

    st.markdown(
        '<div class="section-title">⏰ Cron Automation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Linux scheduled automation for the Smart File Organizer.
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        cron = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )

        cron_output = cron.stdout

    except Exception as e:

        cron_output = str(e)

    if cron_output:

        st.success(
            "✓ Cron configuration detected."
        )

        st.code(
            cron_output,
            language="bash"
        )

    else:

        st.warning(
            "No active crontab configuration detected."
        )

    if st.button(
        "🔄 REFRESH CRON STATUS",
        key="refresh_cron"
    ):

        st.rerun()

    st.markdown("### 🛠 Automation Script")

    if RUN_SCRIPT.exists():

        st.success(
            "✓ run_organizer.sh is available."
        )

        st.code(
            RUN_SCRIPT.read_text(),
            language="bash"
        )

    else:

        st.error(
            "run_organizer.sh not found."
        )

    st.markdown("### 📜 Cron Logs")

    cron_log = BASE_DIR / "logs" / "cron.log"

    if cron_log.exists():

        try:

            content = cron_log.read_text(
                errors="ignore"
            )

            st.code(
                content[-5000:],
                language="text"
            )

        except Exception as e:

            st.error(str(e))

    else:

        st.info(
            "No cron log available yet."
        )


# ============================================================
# RECOVERY PAGE
# ============================================================

elif st.session_state.page == "Recovery":

    st.markdown(
        '<div class="section-title">↩️ Recovery Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Review file movement history and safely undo operations.
        </div>
        """,
        unsafe_allow_html=True
    )

    history = load_history()

    st.metric(
        "Recorded Movements",
        len(history)
    )

    if history:

        for index, move in enumerate(
            reversed(history),
            start=1
        ):

            source = move.get(
                "source",
                "Unknown"
            )

            destination = move.get(
                "destination",
                "Unknown"
            )

            with st.expander(
                f"Movement {index}"
            ):

                st.write(
                    f"**FROM:** `{source}`"
                )

                st.write(
                    f"**TO:** `{destination}`"
                )

    else:

        st.info(
            "No movement history available."
        )

    st.divider()

    if st.button(
        "↩️ UNDO LAST MOVE",
        key="undo_move"
    ):

        try:

            result = subprocess.run(
                ["python3", str(RECOVERY)],
                input="undo\n",
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=30
            )

            if result.stdout:

                st.code(
                    result.stdout,
                    language="text"
                )

            if result.stderr:

                st.error(
                    result.stderr
                )

        except Exception as e:

            st.error(str(e))


# ============================================================
# PROJECT INFO
# ============================================================

elif st.session_state.page == "Project Info":

    st.markdown(
        '<div class="section-title">⚙️ Project Information</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Smart File Organizer — Linux File Management Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### 🎯 Project Objective

        Smart File Organizer is a Python-based Linux file
        management system designed to automate file organization,
        identify duplicates, analyze metadata, monitor directories,
        benchmark performance and provide recovery capabilities.
        """
    )

    st.markdown("### 🧩 Project Modules")

    modules = [
        ("📂", "File Organizer",
         "Automatic file classification"),

        ("🔍", "Duplicate Finder",
         "SHA-256 based duplicate detection"),

        ("📄", "Metadata",
         "File intelligence and analysis"),

        ("⚡", "Benchmark",
         "Performance measurement"),

        ("👀", "File Monitor",
         "Real-time file monitoring"),

        ("⏰", "Cron",
         "Scheduled automation"),

        ("↩️", "Recovery",
         "Movement history and undo")
    ]

    for icon, name, description in modules:

        st.markdown(
            f"""
            <div class="feature-card"
                 style="min-height:100px;margin-bottom:12px;">

                <div class="feature-icon">
                    {icon}
                </div>

                <div class="feature-title">
                    {name}
                </div>

                <div class="feature-text">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### ⚡ Technology Stack")

    tech = st.columns(4)

    technologies = [
        "🐍 Python",
        "🐧 Linux",
        "🔷 WSL2",
        "🎨 Streamlit",
        "🔐 SHA-256",
        "⚡ Threading",
        "💻 Bash",
        "⏰ Cron"
    ]

    for i, technology in enumerate(technologies):

        with tech[i % 4]:

            st.markdown(
                f"""
                <div class="tech-card">
                    {technology}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Smart File Organizer
        <br>
        Linux • Automation • File Intelligence • Recovery
        <br><br>
        M.Tech CSE Project
    </div>
    """,
    unsafe_allow_html=True
)
