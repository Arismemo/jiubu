import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st
# Dummy data
data = {'name': ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II', 'The Dark Knight'],
        'year': [1994, 1972, 1974, 2008],
        'description': ['Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                        'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                        'The early life and career of Vito Corleone in 1920s New York is portrayed while his son, Michael, expands and tightens his grip on the family crime syndicate.',
                        'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham, the Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.'],
        'rating': [9.2, 9.2, 9.0, 9.0],
        'image_url': [
            "https://i.imgur.com/fH2LHvo.png",
            "https://i.imgur.com/bvHZX5j.png",
            "https://i.imgur.com/D7xDwT9.png",
            "https://i.imgur.com/D7xDwT9.png",
                      ]}
df = pd.DataFrame(data)



render_image = JsCode('''
                      
    function renderImage(params) {
    // Create a new image element
    var img = new Image();

    // Set the src property to the value of the cell (should be a URL pointing to an image)
    img.src = params.value;

    // Set the width and height of the image to 50 pixels
    img.width = 50;
    img.height = 50;

    // Return the image element
    return img;
    }
'''
)

# Build GridOptions object
options_builder = GridOptionsBuilder.from_dataframe(df)
options_builder.configure_column('image_url', cellRenderer = render_image)
options_builder.configure_selection(selection_mode="single", use_checkbox=True)
grid_options = options_builder.build()

# Create AgGrid component
grid = AgGrid(df, 
                gridOptions = grid_options,
                allow_unsafe_jscode=True,
                height=200, width=500, theme='streamlit')


sel_row = grid["selected_rows"]
if sel_row:
  with st.expander("Selections", expanded=True):
    col1,col2 = st.columns(2)
    st.info(sel_row[0]['description'])              
    col1.image(sel_row[0]['image_url'],caption=sel_row[0]['name'])