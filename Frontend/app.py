
import streamlit as st 
import st_function as sf
import re 
import time 

#Check if Image Url is valid or not 
def Check_url(url):
    url_pattern = r"https?://\S+"
    return re.match(url_pattern, url) is not None

#Filter Box 
container = st.container()
my_expander1 = st.expander("Filter", expanded=True)
with my_expander1:
    cols = st.columns(3)
    cols[0].caption("Search options ")
    show_result = cols[1].slider("Show results", 1, 15)
    filter = cols[2].selectbox("Filter", ("Image", "Text"))

# if you want to search by Text 

if filter == "Text":
    with st.form("my_form"):
        cols = st.columns([3, 1])
        query = cols[0].text_input("How can we help you?")
        search_type = cols[1].selectbox("search type", ("fuzzy", "match"))
        submit = st.form_submit_button("Search")
        
        if submit:
            if not query:  
                st.error("Oops 😕! Please enter your search.")  # Changed the error message to include emoji and text
            else:
                start_time = time.time()
                sf.search_by_text(query, search_type, show_result) 
                end_time = time.time()
                duration_time = end_time - start_time
                duration_time_str = "{:.3f}".format(duration_time)
                st.toast("Time taken: {} seconds".format(duration_time_str))


# if you want to search by Image

if filter == "Image":
    with st.form("my_form_image"):
        st.write("Please choose one of the following options to search:")
        #Search Images by Url
        # url = st.text_input("Search by image URL")
        #Search Images by browse an image
        uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg"])
        submit = st.form_submit_button("Search")
        if submit:
            # if Check_url(url):
            #     start_time = time.time()
            #     sf.search_by_url(url, show_result)
            #     end_time = time.time()
            #     duration_time = end_time - start_time
            #     duration_time_str = "{:.3f}".format(duration_time)
            #     st.toast("Time taken: {} seconds".format(duration_time_str))
            if uploaded_file:
                uploaded = uploaded_file.read()
                start_time = time.time()
                sf.search_by_upload_image(uploaded, show_result)
                end_time = time.time()
                duration_time = end_time - start_time
                duration_time_str = "{:.3f}".format(duration_time)
                st.toast("Time taken: {} seconds".format(duration_time_str))
            else:
                st.warning("Please provide an image")

        
            
# if you want to search by Booth images and Text area 

# if filter == "Text & Image":
#     with st.form("my_form_both"):
#         cols = st.columns([2, 2])
#         query = cols[0].text_input("Filter by text")
#         search_type = cols[1].selectbox("search type", ("fuzzy", "multi_match", "match"))
#         with cols[0]:
#             st.write("Provide URL or Browse Image")
#             url = st.text_input("Search by URL : ")
#         uploaded_file = cols[1].file_uploader("Upload a file", type=["png", "jpg", "jpeg"])
#         submit = st.form_submit_button("Search")
#         if submit:
#             if Check_url(url) or uploaded_file:
#                 start_time = time.time()
#                 sf.search_by_image_and_text(
#                     uploaded=uploaded_file.read(),
#                     query=query,
#                     search_type=search_type,
#                     show_result=show_result,
#                 )
#                 end_time = time.time()
#                 elapsed_time = end_time - start_time
#                 elapsed_time_str = "{:.3f}".format(elapsed_time)
#                 st.toast("Time taken: {} seconds".format(elapsed_time_str))
#             else:
#                 st.warning("Please provide an image")