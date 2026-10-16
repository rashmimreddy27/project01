import streamlit as st
import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier

# ==========================================
# 1. PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Civic Issue Management",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ AI-Based Civic Issue Prioritisation")
st.write(
    "Report civic issues, estimate their priority, "
    "and identify locations with frequent complaints."
)

FILE = "complaints.csv"

COLUMNS = [
    "Issue",
    "Location",
    "Severity",
    "Days Unresolved",
    "Priority"
]

# ==========================================
# 2. TRAIN THE DEMONSTRATION AI MODEL
# ==========================================

training_data = pd.DataFrame({
    "Issue": [
        "Potholes", "Potholes", "Potholes",
        "Garbage", "Garbage", "Garbage",
        "Water Leakage", "Water Leakage", "Water Leakage",
        "Broken Streetlights", "Broken Streetlights",
        "Broken Streetlights"
    ],
    "Severity": [
        "High", "Medium", "Low",
        "High", "Medium", "Low",
        "High", "Medium", "Low",
        "High", "Medium", "Low"
    ],
    "Days Unresolved": [
        5, 2, 0,
        4, 2, 0,
        7, 3, 0,
        6, 2, 0
    ],
    "Priority": [
        "Urgent", "Medium", "Low",
        "Urgent", "Medium", "Low",
        "Urgent", "Medium", "Low",
        "Urgent", "Medium", "Low"
    ]
})

# Convert issue and severity categories into numeric columns
X = pd.get_dummies(
    training_data[["Issue", "Severity"]]
)

# Add days unresolved as a numeric feature
X["Days Unresolved"] = training_data["Days Unresolved"]

y = training_data["Priority"]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# ==========================================
# 3. CREATE OR LOAD COMPLAINT DATA
# ==========================================

if not os.path.exists(FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(
        FILE,
        index=False
    )


def load_complaints():
    """
    Load complaints while handling old CSV files
    and rows with inconsistent column counts.
    """

    try:
        complaints = pd.read_csv(
            FILE,
            on_bad_lines="warn"
        )

    except pd.errors.EmptyDataError:
        complaints = pd.DataFrame(columns=COLUMNS)

    # Handle older files without Days Unresolved
    if "Days Unresolved" not in complaints.columns:
        complaints["Days Unresolved"] = 0

    # Add any missing expected columns
    for column in COLUMNS:
        if column not in complaints.columns:
            complaints[column] = 0 if column == "Days Unresolved" else ""

    # Keep the expected columns in a consistent order
    complaints = complaints[COLUMNS]

    # Convert the days column into numbers
    complaints["Days Unresolved"] = pd.to_numeric(
        complaints["Days Unresolved"],
        errors="coerce"
    ).fillna(0).astype(int)

    return complaints


complaints = load_complaints()

# ==========================================
# 4. COMPLAINT SUBMISSION FORM
# ==========================================

st.header("📝 Submit a Civic Complaint")

with st.form("complaint_form"):

    issue = st.selectbox(
        "Select the issue",
        [
            "Potholes",
            "Garbage",
            "Water Leakage",
            "Broken Streetlights"
        ]
    )

    location = st.text_input(
        "Enter the location",
        placeholder="Example: Main Road"
    )

    severity = st.selectbox(
        "Select severity",
        ["High", "Medium", "Low"]
    )

    days_unresolved = st.number_input(
        "Days the issue has remained unresolved",
        min_value=0,
        max_value=365,
        value=0,
        step=1
    )

    submitted = st.form_submit_button(
        "Submit Complaint"
    )

    if submitted:

        if not location.strip():
            st.warning("Please enter the location.")

        else:
            # Prepare input for the AI model
            new_issue = pd.DataFrame({
                "Issue": [issue],
                "Severity": [severity]
            })

            encoded_issue = pd.get_dummies(
                new_issue
            ).reindex(
                columns=[
                    column for column in X.columns
                    if column != "Days Unresolved"
                ],
                fill_value=0
            )

            # Add the days unresolved feature
            encoded_issue["Days Unresolved"] = days_unresolved

            # Ensure columns exactly match the training features
            encoded_issue = encoded_issue.reindex(
                columns=X.columns,
                fill_value=0
            )

            # Predict priority
            priority = model.predict(encoded_issue)[0]

            # Create the new complaint record
            new_complaint = pd.DataFrame([{
                "Issue": issue,
                "Location": location.strip(),
                "Severity": severity,
                "Days Unresolved": days_unresolved,
                "Priority": priority
            }])

            # Add it to the current records
            complaints = pd.concat(
                [complaints, new_complaint],
                ignore_index=True
            )

            # Save using a consistent five-column format
            complaints.to_csv(
                FILE,
                index=False
            )

            st.success(
                f"Complaint saved! Demonstration model priority: {priority}"
            )

            st.info(
                "This priority is a prototype prediction, "
                "not an official civic authority decision."
            )

# ==========================================
# 5. DISPLAY ALL COMPLAINTS
# ==========================================

st.header("📋 All Submitted Complaints")

# Reload the data after form submission
complaints = load_complaints()

if complaints.empty:
    st.info("No complaints have been submitted yet.")

else:
    st.dataframe(
        complaints,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# 6. HOTSPOT ANALYSIS
# ==========================================

st.header("📍 Civic Issue Hotspot Analysis")

if complaints.empty:
    st.info("Submit complaints to analyse hotspots.")

else:
    hotspot_data = (
        complaints.groupby("Location")
        .size()
        .reset_index(name="Number of Complaints")
        .sort_values(
            by="Number of Complaints",
            ascending=False
        )
    )

    st.subheader("Complaints by Location")

    st.dataframe(
        hotspot_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        hotspot_data.set_index("Location")[
            "Number of Complaints"
        ]
    )

    if not hotspot_data.empty:
        st.write(
            "**Most reported location:**",
            hotspot_data.iloc[0]["Location"]
        )

# ==========================================
# 7. DASHBOARD
# ==========================================

st.header("📊 Civic Issues Dashboard")

total_complaints = len(complaints)

urgent_complaints = len(
    complaints[complaints["Priority"] == "Urgent"]
)

if not complaints.empty:
    most_reported_location = (
        complaints["Location"]
        .value_counts()
        .idxmax()
    )

    average_days = complaints["Days Unresolved"].mean()

else:
    most_reported_location = "No complaints yet"
    average_days = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Complaints",
    total_complaints
)

col2.metric(
    "Urgent Complaints",
    urgent_complaints
)

col3.metric(
    "Top Complaint Location",
    most_reported_location
)

col4.metric(
    "Average Days Unresolved",
    f"{average_days:.1f}"
)

# ==========================================
# 8. DASHBOARD CHARTS
# ==========================================

st.subheader("Complaints by Issue")

issue_counts = complaints["Issue"].value_counts()

if not issue_counts.empty:
    st.bar_chart(issue_counts)
else:
    st.info("No issue data available yet.")

st.subheader("Complaints by Location")

location_counts = complaints["Location"].value_counts()

if not location_counts.empty:
    st.bar_chart(location_counts)
else:
    st.info("No location data available yet.")

st.subheader("Complaints by Severity")

severity_counts = complaints["Severity"].value_counts()

if not severity_counts.empty:
    st.bar_chart(severity_counts)
else:
    st.info("No severity data available yet.")

# ==========================================
# 9. COMPLAINTS BY PRIORITY
# ==========================================

st.subheader("Complaints by Predicted Priority")

priority_counts = complaints["Priority"].value_counts()

if not priority_counts.empty:
    st.bar_chart(priority_counts)
else:
    st.info("No priority data available yet.")

# ==========================================
# END OF APPLICATION
# ==========================================