
import streamlit as st
import pandas as pd

# Step 7: Set configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 04",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for UI styling
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* Subtle divider spacing */
    hr {
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Step 11: Add CSV files
def load_student_data():
    try:
        data = pd.read_csv("Student.csv")
        return data
    except FileNotFoundError:
        st.error(
            "Student.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


# Load student data
student_df = load_student_data()


# Step 9: Add a risk level function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"


# Add risk level column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)


# Add initialize
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []


# Step 11: Redesigned Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="margin: 0; font-size: 26px;">🎓 EduRisk</h1>
            <p style="color: #6c757d; font-size: 13px; margin-top: 4px;">Analytics & Risk Monitoring</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    raw_page = st.radio(
        "MAIN MENU",
        [
            "🏠 Home",
            "📊 Dashboard",
            "👥 Student Data",
            "🎯 Risk Checker",
            "ℹ️ About"
        ]
    )

    st.divider()
    st.caption("🚀 **Lab 02** | Streamlit App")
    st.caption("v1.0.0 • Data Science Web App")


# Map selected option back to clean page string
if "Home" in raw_page:
    selected_page = "Home"
elif "Dashboard" in raw_page:
    selected_page = "Dashboard"
elif "Student Data" in raw_page:
    selected_page = "Student Data"
elif "Risk Checker" in raw_page:
    selected_page = "Risk Checker"
else:
    selected_page = "About"


# Step 12: Homepage
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Reliable Risk Checker with Forms and Session State")
    st.write("Welcome to Lab 04.")

    st.write(
        "In this lab, the app improves the Risk Checker page using "
        "Streamlit forms, input validation, and session state."
    )

    st.success("Lab 04 app is running successfully!")


# Step 13: Dashboard Page
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard gives a quick overview of student performance "
        "using data loaded from Student.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()

    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.write("This table shows student data loaded from Student.csv.")
    st.dataframe(student_df)

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

    st.divider()
    st.markdown("### Interactive Filters")

    # FILTER WIDGETS
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        course_list = ["All"] + sorted(
            student_df["Course"].unique().tolist()
        )
        selected_course = st.selectbox("Select Course", course_list)

    with f_col2:
        risk_list = ["All", "Low Risk", "Medium Risk", "High Risk"]
        selected_risk = st.selectbox("Select Risk Level", risk_list)

    with f_col3:
        min_attendance = st.slider("Min Attendance (%)", 0, 100, 0)

    with f_col4:
        min_score = st.slider("Min Score", 0, 100, 0)

    # FILTER LOGIC
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        (filtered_df["Attendance"] >= min_attendance) &
        (filtered_df["Score"] >= min_score)
    ]

    # METRICS SECTION
    total_students = len(filtered_df)

    avg_score = (
        filtered_df["Score"].mean()
        if total_students > 0 else 0
    )

    avg_attendance = (
        filtered_df["Attendance"].mean()
        if total_students > 0 else 0
    )

    high_risk_count = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.markdown("### Filtered Key Metrics")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Students", total_students)
    m2.metric("Avg Score", f"{avg_score:.1f}")
    m3.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    m4.metric("High Risk", high_risk_count)

    st.divider()

    # CHARTS SECTION
    st.markdown("### Analytics & Visualizations")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Student Scores Overview**")

        if total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart, color="#4F46E5")
        else:
            st.warning("No data matches the selected filters.")

    with chart_col2:
        st.markdown("**Risk Distribution**")

        if total_students > 0:
            risk_count = filtered_df["Risk Level"].value_counts()
            st.bar_chart(risk_count, color="#EF4444")
        else:
            st.warning("No data matches the selected filters.")

    st.divider()

    # DATASET SECTION
    st.markdown("### Dataset Details")

    show_data = st.toggle("Show Filtered Dataset", True)

    if show_data:
        if total_students > 0:
            st.dataframe(filtered_df, use_container_width=True)

            csv = filtered_df.to_csv(index=False)

            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name="filtered_student_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No records match your filters.")
    else:
        st.info("Filtered dataset is currently hidden.")


# Step 24: Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from Student.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)


# Step 25: Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    # Only ONE form with this key
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    # Check if the form is submitted
    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")

        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )

            # Create result dictionary
            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

            # Save result to session state
            st.session_state["risk_history"].append(result)

            # Display risk feedback
            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            # Display student information
            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

    # Recent Risk Checks
    st.subheader("Recent Risk Checks")

    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )

        st.dataframe(history_df)

        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")
    else:
        st.info("No risk checks yet.")

    # Ethics Reminder
    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )


# Step 26: Redesigned About Page
else:
    st.title("About")

    st.write("This app is part of Lab 04.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Forms, Validation, and Session State")

    st.info(
        "This version improves the Risk Checker page using Streamlit forms, "
        "input validation, and session state."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )
