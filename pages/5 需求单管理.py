
# # import streamlit as st
# # from streamlit_modal import Modal

# # import streamlit.components.v1 as components


# # modal = Modal("Demo Modal", key = 'test')
# # open_modal = st.button("Open")
# # if open_modal:
# #     modal.open()

# # if modal.is_open():
# #     with modal.container():
# #         st.write("Text goes here")

# #         html_string = '''
# #         <h1>HTML string in RED</h1>

# #         <script language="javascript">
# #           document.querySelector("h1").style.color = "red";
# #         </script>
# #         '''
# #         components.html(html_string)

# #         st.write("Some fancy text")
# #         value = st.checkbox("Check me")
# #         st.write(f"Checkbox checked: {value}")






# import streamlit as st
# from streamlit_custom_notification_box import custom_notification_box
# st.subheader("Component with constant args")

# styles = {'material-icons':{'color': 'red'},
#           'text-icon-link-close-container': {'box-shadow': '#3896de 0px 4px'},
#           'notification-text': {'':''},
#           'close-button':{'':''},
#           'link':{'':''}}

# custom_notification_box(icon='info', textDisplay='We are almost done with your registration...', externalLink='more info', url='#', styles=styles, key="foo")









import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes
st.header("Cropper Demo")
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

if img_file:
    img = Image.open(img_file)
    if not realtime_update:
        st.write("Double click to save crop")
    # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    
    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)