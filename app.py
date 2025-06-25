import streamlit as st
import pandas as pd
import os
import subprocess

st.set_page_config(page_title="PNpilot Bot", layout="centered")
st.title("🛩️ PNpilot - Aircraft Parts Scraper")

# Upload CSV file
uploaded_file = st.file_uploader("📤 Upload your CSV with 'Part Number' column:", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # Limit how many parts to process
    limit = st.slider("🔢 Select how many part numbers to process (batch limit)", 10, len(df), 100)
    df = df.head(limit)

    # Save limited file to disk
    df.to_csv("input_parts.csv", index=False)

    if st.button("🚀 Run Scraper"):
        st.info("⏳ Running PNpilot bot. Please wait...")

        # Clear old results and processed if exist
        for file in ["pnpilot_results.csv", "processed.txt", "failed.txt"]:
            if os.path.exists(file):
                os.remove(file)

        try:
            result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
            st.success("✅ Scraper finished successfully!")

            if os.path.exists("pnpilot_results.csv"):
                result_df = pd.read_csv("pnpilot_results.csv")
                st.dataframe(result_df.head())

                csv_download = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Result CSV",
                    data=csv_download,
                    file_name="pnpilot_results.csv",
                    mime="text/csv"
                )

            if os.path.exists("failed.txt"):
                failed_parts = open("failed.txt", "r").read().splitlines()
                if failed_parts:
                    st.warning(f"⚠️ {len(failed_parts)} part numbers failed during scraping.")
                    st.download_button(
                        label="📥 Download Failed Part Numbers",
                        data="\n".join(failed_parts),
                        file_name="failed_parts.txt",
                        mime="text/plain"
                    )
        except Exception as e:
            st.error(f"❌ Error during run: {e}")
            st.text(result.stdout)
            st.text(result.stderr)

    st.markdown("""
        ---
        ### ⚠️ Tips to Avoid CAPTCHA & IP Ban:
        - 🕒 Use the slider to **limit the batch size** (e.g., 100 per run)
        - ⏱️ Bot introduces **random delays** between requests (2–4 seconds)
        - 🔄 Uses **random User-Agent headers** to simulate real users
        - 💡 Use proxies if scraping large volumes daily
        - 🔒 If CAPTCHA appears, part number will be skipped & saved in `failed.txt`
        - 🔁 You can re-upload the failed list for retrying later
        
        """)
else:
    st.warning("⬆️ Please upload a CSV file to begin.")
