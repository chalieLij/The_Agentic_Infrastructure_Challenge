import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import random

# Page Config
st.set_page_config(
    page_title="Project Chimera: Swarm Command",
    page_icon="🤖",
    layout="wide",
)

# --- 1. Header ---
st.title("Project Chimera: Swarm Command")
st.markdown("---")

# --- Mock Data Generators based on specs/technical.md ---

def get_mock_trends():
    """
    Generates mock trend data matching the Trend Fetcher Service "Response (200 OK)" schema.
    Returns a pandas DataFrame for easy visualization.
    """
    trends = [
        {
            "rank": 1,
            "keyword": "AI Agents",
            "volume": 85000,
            "sentiment_score": 0.85,
            "related_hashtags": ["#AI", "#Agents", "#Tech"],
        },
        {
            "rank": 2,
            "keyword": "Python 4.0",
            "volume": 62000,
            "sentiment_score": 0.45,  # Slightly controversial?
            "related_hashtags": ["#Python", "#Coding"],
        },
        {
            "rank": 3,
            "keyword": "Sustainable Tech",
            "volume": 45000,
            "sentiment_score": 0.92,
            "related_hashtags": ["#GreenTech", "#Sustainability"],
        },
        {
            "rank": 4,
            "keyword": "Crypto Regulation",
            "volume": 95000,
            "sentiment_score": -0.30, # Negative sentiment
            "related_hashtags": ["#Crypto", "#Regulation"],
        },
        {
            "rank": 5,
            "keyword": "VR Gaming",
            "volume": 30000,
            "sentiment_score": 0.60,
            "related_hashtags": ["#VR", "#Gaming"],
        }
    ]
    return pd.DataFrame(trends)

def get_mock_agent_status():
    """
    Mocks the OpenClaw 'Heartbeat' protocol status.
    No strict schema in technical.md, but inferred from requirements.
    """
    return [
        {
            "agent_id": "Influencer-Alpha",
            "role": "Influencer",
            "status": "BUSY",
            "last_heartbeat": datetime.now().strftime("%H:%M:%S"),
            "current_task": "Generating video script"
        },
        {
            "agent_id": "Researcher-Beta",
            "role": "Researcher",
            "status": "AVAILABLE",
            "last_heartbeat": (datetime.now() - timedelta(seconds=5)).strftime("%H:%M:%S"),
            "current_task": "Idle"
        },
        {
            "agent_id": "Reviewer-Gamma",
            "role": "Reviewer",
            "status": "AVAILABLE",
            "last_heartbeat": (datetime.now() - timedelta(seconds=2)).strftime("%H:%M:%S"),
            "current_task": "Idle"
        }
    ]

def get_mock_tasks():
    """
    Generates mock tasks matching the 'Agent Task Schema' in specs/technical.md.
    """
    return [
        {
            "task_id": str(uuid.uuid4()),
            "task_type": "generate_content",
            "priority": "high",
            "status": "in_progress",
            "assigned_worker_id": "Influencer-Alpha",
            "created_at": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "goal_description": "Create viral video about AI"
        },
        {
            "task_id": str(uuid.uuid4()),
            "task_type": "execute_transaction",
            "priority": "medium",
            "status": "pending",
            "assigned_worker_id": "Unassigned",
            "created_at": (datetime.now() - timedelta(minutes=45)).isoformat(),
            "goal_description": "Purchase stock photos"
        },
        {
            "task_id": str(uuid.uuid4()),
            "task_type": "reply_comment",
            "priority": "low",
            "status": "complete",
            "assigned_worker_id": "Influencer-Alpha",
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "goal_description": "Reply to top comment on latest post"
        }
    ]

# --- 2. Trend Monitor ---
st.header("📈 Trend Monitor")
st.caption("Live feed from Trend Fetcher Service (Mock)")

df_trends = get_mock_trends()

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Top Trend", df_trends.iloc[0]['keyword'], f"{df_trends.iloc[0]['volume']:,} searches")
with col2:
    avg_sentiment = df_trends['sentiment_score'].mean()
    st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
with col3:
    st.metric("Active Trends", len(df_trends))

# Visualizing Sentiment vs Keyword
st.subheader("Sentiment Analysis")
st.bar_chart(data=df_trends, x="keyword", y="sentiment_score", color="#4CAF50")

# Detailed Data Table
with st.expander("View Raw Trend Data"):
    st.dataframe(df_trends, use_container_width=True)


st.markdown("---")

# --- 3. Agent Status (OpenClaw Heartbeat) ---
st.header("❤️ Agent Status (OpenClaw)")
agents = get_mock_agent_status()

# Create a grid layout for agents
cols = st.columns(len(agents))

for i, agent in enumerate(agents):
    with cols[i]:
        # Determine color based on status
        status_color = "green" if agent["status"] == "AVAILABLE" else "red"
        st.markdown(f"### :{status_color}[{agent['role']}]")
        st.write(f"**ID:** `{agent['agent_id']}`")
        
        if agent["status"] == "AVAILABLE":
            st.success(f"Status: {agent['status']}")
        else:
            st.warning(f"Status: {agent['status']}")
            
        st.text(f"Last Heartbeat: {agent['last_heartbeat']}")
        st.caption(f"Task: {agent['current_task']}")

st.markdown("---")

# --- 4. Task Queue ---
st.header("📋 Task Queue")
tasks = get_mock_tasks()
df_tasks = pd.DataFrame(tasks)

# Style the dataframe based on status? 
# Streamlit dataframe styling is simple, let's just show it.
# We can map status to emojis for better visual
status_map = {
    "pending": "⏳ Pending",
    "in_progress": "🔄 In Progress",
    "complete": "✅ Complete",
    "review": "👀 Review"
}
df_tasks['status_display'] = df_tasks['status'].map(status_map)

# Reorder columns for display
display_cols = ["status_display", "priority", "task_type", "assigned_worker_id", "goal_description", "created_at"]
st.dataframe(
    df_tasks[display_cols],
    use_container_width=True,
    column_config={
        "created_at": st.column_config.DatetimeColumn("Created At", format="D MMM, HH:mm"),
        "priority": st.column_config.TextColumn("Priority"),
    },
    hide_index=True
)

# Add a mock "Add Task" button to simulate interaction
if st.button("➕ Inject Mock Task"):
    st.toast("New task injected into queue (Simulated)", icon="✅")
