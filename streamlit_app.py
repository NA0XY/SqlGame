import streamlit as st
import requests
import pandas as pd

API_URL = 'http://localhost:5000'

st.set_page_config(
    page_title="🔍 SQL Murder Mystery",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 SQL Murder Mystery")
st.caption("A database detective game. Help solve the case using SQL!")

left, right = st.columns([2.5, 1.6], gap="large")

with left:
    st.header("🕵️‍♂️ Case File")
    st.markdown("""
    **Victim:** John Smith  
    **Location:** Downtown Hotel, Room 302  
    **Date:** May 1, 2025  
    **Time:** ~2:15 AM  
    **Cause:** Blunt force trauma to the head  
    **Detective:** James Green

    *You are the database analyst. Use SQL to help solve the murder!*

    **Database Tables:**  
    - Person  
    - Crime  
    - Evidence  
    - Interviews  
    - Alibis  
    - Relationships  
    - PhoneRecords
    """)

    st.header("💻 Investigation Terminal")
    with st.expander("💡 Example Queries & Tips", expanded=False):
        st.markdown("""
        - `SELECT * FROM Crime;`  
        - `SELECT * FROM Evidence;`  
        - `SELECT * FROM Person;`  
        - `SELECT p.Name, a.* FROM Alibis a JOIN Person p ON a.PersonID = p.PersonID;`  
        - `SELECT * FROM PhoneRecords WHERE time > '2025-05-01 00:00';`  
        """)
        st.info("**Tip:** Start by examining the crime scene and then explore connections between suspects and the victim.")

    query = st.text_area("Enter your SQL SELECT query:", height=120, key="sql_query")

    if st.button("🚀 Execute Query"):
        if not query.strip():
            st.error("Please enter a query.")
        elif not query.strip().lower().startswith("select"):
            st.error("Only SELECT queries are allowed.")
        else:
            try:
                with st.spinner("Running your query..."):
                    response = requests.post(f"{API_URL}/api/execute-query", json={"query": query})
                    data = response.json()
                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    results = data.get("results", [])
                    if results:
                        df = pd.DataFrame(results)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Query executed successfully but returned no results.")
            except Exception as e:
                st.error(f"Failed to execute query: {e}")

with right:
    st.header("📝 Case Notes")
    if "case_notes" not in st.session_state:
        st.session_state["case_notes"] = ""
    st.text_area(
        "Jot down your findings and theories here:",
        key="case_notes",
        height=220
    )

    st.header("🔐 Submit Your Solution")
    st.write("When you're confident, enter the PersonID of the murderer:")

    murderer_id = st.text_input("PersonID:", key="solution_input")

    if st.button("✅ Check Solution"):
        if not murderer_id.strip():
            st.error("Please enter a PersonID.")
        elif not murderer_id.strip().isdigit():
            st.error("Please enter a valid numeric PersonID.")
        else:
            try:
                response = requests.post(f"{API_URL}/api/check-solution", json={"murdererId": int(murderer_id)})
                data = response.json()
                if data.get("correct"):
                    st.balloons()
                    st.success(data.get("message", "🎉 Correct! You solved the case!"))
                else:
                    st.warning(data.get("message", "That's not correct. Keep investigating!"))
            except Exception as e:
                st.error(f"Failed to check solution: {e}")

st.markdown("---")
st.caption("Created for SQL sleuths. Happy investigating! 🕵️‍♀️")
