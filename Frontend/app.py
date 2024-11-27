import streamlit as st 
import st_function as sf
import re 
import time 
from PIL import Image
import io


# Function to check if the image URL is valid or not
def Check_url(url):
    url_pattern = r"https?://\S+"
    return re.match(url_pattern, url) is not None

import streamlit as st

# Custom CSS for horizontal radio buttons styled like a slider
st.markdown("""
    <style>
    .radio-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #492D30;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .radio-container label {
        margin: 0 20px;
        font-size: 16px;
        color: white;
    }

    .stRadio > div {
        flex-direction: row; /* Make the radio buttons horizontal */
    }

    .stRadio div[role='radiogroup'] {
        justify-content: space-around; /* Add spacing between options */
    }
     .stColumns {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .stColumn {
        flex: 1;
        margin-right: 10px;
    }
    .stColumn:last-child {
        margin-right: 0;
    }

    /* Style the spinner */
    .stSpinner {
        color: #00aaff;  /* Spinner color */
    }

    /* Style images to have rounded corners and shadow */
    img {
        border-radius: 10px;
        box-shadow: 0px 8px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 10px;
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Filter Box
# Sidebar for filter options
st.sidebar.markdown("<h6>🔍 Search Options</h6>", unsafe_allow_html=True)

# Slider for showing results
show_result = st.sidebar.slider("Show results", 1, 15, value=5, format="%d")  

# Radio buttons for filter selection
filter = st.sidebar.radio("Choose Filter", ("Image", "Text"), index=0)

# Use the selected filter in your main application logic
if filter == "Text":
    # Your code for handling text search
    st.write("You selected Text search.")
    # Add your existing logic for text search here

elif filter == "Image":
    # Your code for handling image search
    st.write("You selected Image search.")
    # Add your existing logic for image search here
# Show the selected filter
st.write(f"Selected filter: {filter}")

# Search by Text
if filter == "Text":
    with st.form("my_form"):
        cols = st.columns([3,1])
        query = cols[0].text_input("💬 How can we help you?", "", placeholder="Type your query here...")  # Icon added
        search_type = cols[1].selectbox("Search type", ("fuzzy", "match"))
        submit = st.form_submit_button("🔍 Search")
        
        if submit:
            if not query:
                st.error("❌ Oops 😕! Please enter your search.")  # Error message with emoji
            else:
                start_time = time.time()
                sf.search_by_text(query, search_type, show_result, cols)
                end_time = time.time()
                duration_time = end_time - start_time
                duration_time_str = "{:.3f}".format(duration_time)
                st.success(f"✅ Time taken: {duration_time_str} seconds")  # Success message with icon

# Search by Image
if filter == "Image":
    with st.form("my_form_image"):
        st.write("📸 Please choose one of the following options to search:")  # Icon added
        uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg"], help="Upload an image for search")
        submit = st.form_submit_button("🔍 Search")
        
        if submit:
            if uploaded_file:
                uploaded = uploaded_file.read()
                start_time = time.time()
                sf.search_by_upload_image(uploaded, show_result)
                end_time = time.time()
                duration_time = end_time - start_time
                duration_time_str = "{:.3f}".format(duration_time)
                st.success(f"✅ Time taken: {duration_time_str} seconds")
            else:
                st.warning("⚠️ Please provide an image")


sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
