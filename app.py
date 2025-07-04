import streamlit as st
from utils.auth import init_db, create_user, authenticate_user
from utils.docgen import load_file, generate_ml_doc, generate_sar_repo
import io

# Initialize DB
init_db()

st.set_page_config(page_title="Sandbox: Document Generator")

# Authentication State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("User Authentication")

    auth_choice = st.radio("Select action", ["Login", "Sign Up"])

    if auth_choice == "Sign Up":
        st.subheader("Create a new account")
        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if new_user and new_pass:
                if create_user(new_user, new_pass):
                    st.success("Account created successfully. Please log in.")
                else:
                    st.error("Username already exists or error occurred.")
            else:
                st.warning("Please enter username and password.")

    elif auth_choice == "Login":
        st.subheader("Login")
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if authenticate_user(user, pwd):
                st.session_state.logged_in = True
                st.session_state.username = user
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

else:
    st.title("Sandbox: Document Generator")
    st.write(f"Welcome, **{st.session_state.username}**!")

    uploaded_file = st.file_uploader("Upload a document (.txt, .csv, .xlsx)", type=["txt", "csv", "xlsx"])

    if uploaded_file:
        data = load_file(uploaded_file)
        if data is None:
            st.error("Unsupported file type.")
        else:
            st.header("Preview Uploaded Data")
            if isinstance(data, str):
                st.text(data)
            else:
                st.dataframe(data)

            st.header("Select Template to Generate")

            template_choice = st.selectbox("Choose template", ["ML Documentation", "SAR Repository"])

            if st.button("Generate Document"):
                if template_choice == "ML Documentation":
                    result = generate_ml_doc(data)
                else:
                    result = generate_sar_repo(data)

                st.subheader(f"{template_choice} Preview")
                st.markdown(result)

                # Download button
                buffer = io.StringIO()
                buffer.write(result)
                st.download_button(label="Download Document", data=buffer.getvalue(), file_name=f"{template_choice.replace(' ','_')}.txt")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
