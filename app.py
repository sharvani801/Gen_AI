import streamlit as st
import requests


st.set_page_config(
    page_title="GitHub Code Explainer",
    page_icon="💻",
    layout="wide"
)


st.title("💻 GitHub Code Explainer")
st.write(
    "Enter a GitHub repository URL and get a simple explanation "
    "using a locally running GenAI model."
)


github_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)


if st.button("🚀 Explain Repository", type="primary"):

    if not github_url:
        st.warning("Please enter a GitHub repository URL.")

    else:

        with st.spinner(
            "Cloning repository and generating explanation..."
        ):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/explain",
                    json={
                        "github_url": github_url
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Repository analyzed successfully!")

                    st.subheader("📋 Project Explanation")

                    st.markdown(data["explanation"])

                    st.subheader("📁 Files Analyzed")

                    for file in data["files_analyzed"]:
                        st.write(f"- `{file}`")

                else:

                    st.error(
                        f"Backend error: {response.text}"
                    )

            except Exception as e:

                st.error(f"Connection error: {e}")