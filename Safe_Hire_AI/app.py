import streamlit as st
import requests
import pandas as pd

# Set up the look of the web page
st.set_page_config(page_title="SafeHire AI", page_icon="🛡️", layout="wide")

# HERO HEADER
st.title("🛡️ SafeHire AI Enterprise Suite")
st.markdown("### The Omnichannel HR Compliance Platform")
st.markdown("---")

# The URL where your FastAPI backend is running (Updated to match main.py)
API_URL = "http://127.0.0.1:8000/predict"

# Create UI Tabs for different features
tab1, tab2, tab3 = st.tabs(["📝 Single Question Check", "📊 Phase 1: Bulk CSV Audit", "🔌 Phase 2: Live Monitor (Extension)"])

# ==========================================
# --- TAB 1: SINGLE QUESTION ---
# ==========================================
with tab1:
    st.header("Quick Compliance Check")
    question_input = st.text_area("Interview Question:", placeholder="e.g., What year did you graduate high school?", height=100)

    if st.button("Check Legal Risk"):
        if question_input.strip() == "":
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(API_URL, json={"text": question_input})
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result["is_flagged"]:
                            st.error("🚨 **HIGH RISK QUESTION DETECTED**")
                            st.write(f"**Violation Category:** {result['category']}")
                            st.write(f"**Litigation Risk Score:** {result['risk_score']}")
                            st.info(f"💡 **Legally Safe Alternative:**\n\n{result['safe_alternative']}")
                        else:
                            st.success("✅ **SAFE TO ASK**")
                            st.write("This question passed the compliance check. No protected class or salary history violations detected.")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to the AI Engine. Please make sure your FastAPI server is running!")

# ==========================================
# --- TAB 2: BULK CSV UPLOAD ---
# ==========================================
with tab2:
    st.header("Bulk CSV Compliance Audit")
    st.markdown("Upload a CSV file containing an HR questionnaire to instantly audit all questions for legal compliance.")
    st.info("💡 Note: Your CSV must have a column header named **Question**.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Check if the CSV has the right column
        if 'Question' not in df.columns:
            st.error("❌ Error: Could not find a 'Question' column in your CSV. Please check your file format.")
        else:
            st.write(f"Loaded {len(df)} questions. Ready for audit.")
            
            if st.button("Run Bulk AI Audit"):
                with st.spinner("Processing questions through AI Engine..."):
                    results = []
                    
                    # Loop through each question and send it to the FastAPI backend
                    for index, row in df.iterrows():
                        q_text = str(row['Question'])
                        try:
                            response = requests.post(API_URL, json={"text": q_text})
                            if response.status_code == 200:
                                res_data = response.json()
                                results.append({
                                    "Original Question": q_text,
                                    "Status": "🚨 Flagged" if res_data["is_flagged"] else "✅ Safe",
                                    "Category": res_data["category"],
                                    "Risk Score": res_data["risk_score"],
                                    "Safe Alternative": res_data["safe_alternative"]
                                })
                            else:
                                results.append({"Original Question": q_text, "Status": "Error", "Category": "-", "Risk Score": "-", "Safe Alternative": "-"})
                        except:
                            results.append({"Original Question": q_text, "Status": "API Error", "Category": "-", "Risk Score": "-", "Safe Alternative": "-"})
                    
                    if results:
                        # Display the results as a beautiful interactive table
                        results_df = pd.DataFrame(results)
                        st.dataframe(results_df, use_container_width=True)

                        # --- ENTERPRISE DASHBOARD ANALYTICS ---
                        st.markdown("---")
                        st.subheader("📊 Enterprise Compliance Analytics")

                        # 1. Calculate the core metrics from results_df
                        total_questions = len(results_df)
                        illegal_count = len(results_df[results_df['Status'] == '🚨 Flagged']) 
                        safe_count = len(results_df[results_df['Status'] == '✅ Safe'])
                        risk_percentage = round((illegal_count / total_questions) * 100, 1) if total_questions > 0 else 0

                        # 2. Display Top-Level Metric Cards
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric(label="Total Questions", value=total_questions)
                        col2.metric(label="Safe Questions ✅", value=safe_count)
                        col3.metric(label="Violations 🚨", value=illegal_count)
                        col4.metric(label="Company Risk Score", value=f"{risk_percentage}%")

                        # 3. Generate the Violation Bar Chart
                        if illegal_count > 0:
                            st.write("### 📉 Breakdown of Legal Violations")
                            violation_counts = results_df[results_df['Status'] == '🚨 Flagged']['Category'].value_counts()
                            st.bar_chart(violation_counts, color="#ff4b4b")
                        else:
                            st.success("🎉 100% Compliant! No legal risks detected in this batch.")

# ==========================================
# --- TAB 3: EXTENSION DOWNLOAD PAGE ---
# ==========================================
with tab3:
    st.header("Live Virtual Safety Net")
    st.markdown("Equip your recruiters with our predictive AI edge-monitor for Google Meet and Zoom.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # The Download Button
        try:
            with open("SafeHire_Extension.zip", "rb") as file:
                st.download_button(
                    label="⬇️ Download Chrome Extension (ZIP)",
                    data=file,
                    file_name="SafeHire_Extension.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.error("⚠️ Please place 'SafeHire_Extension.zip' in the project folder to enable downloads.")
            
    with col2:
        st.info("""
        **How to Install the Enterprise MVP:**
        1. Download and extract the ZIP file.
        2. Open your browser and navigate to `chrome://extensions/`
        3. Enable **Developer Mode** (top right).
        4. Click **Load unpacked** and select the extracted folder.
        5. Pin the extension to your toolbar and click it to start live monitoring!
        """)