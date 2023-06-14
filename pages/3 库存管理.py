from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import pymysql
from st_aggrid import AgGrid,ColumnsAutoSizeMode
from st_aggrid import AgGrid, JsCode

# engine = create_engine(
#     "mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu",
#     # encoding= "utf-8",
#     echo=True
# )    

from app.product_handler import ProductHandler

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
@st.cache_resource
def ph():
    ph = ProductHandler()
    return ph


st.set_page_config(layout='wide')

df = ph().get_product_data() 

render_image = JsCode('''                     
    function renderImage(params) {
        // Create a new image element
        var img = new Image();

        // Set the src property to the value of the cell (should be a URL pointing to an image)
        img.src = "http://192.168.50.200/resource/jiubu_media/temp/".concat(params.value);

        // Set the width and height of the image to 50 pixels
        img.width = 50;
        img.height = 50;
        console.log('liukun');
        console.log(img.src);
        console.log(params);

        // Return the image element
        return img;
    }
'''
)
                      
# Build GridOptions object
options_builder = GridOptionsBuilder.from_dataframe(df)
options_builder.configure_auto_height()
options_builder.configure_side_bar()
options_builder.configure_column('图片', cellRenderer = render_image)
options_builder.configure_selection(selection_mode = 'multiple', use_checkbox=True)
grid_options = options_builder.build()
                      

grid = AgGrid(
    df,
    fit_columns_on_grid_load=True,
    height=1800,
    enable_quicksearch=True,
    allow_unsafe_jscode=True,
    gridOptions = grid_options,
)


# sel_row = grid["selected_rows"]
# if sel_row:
#   with st.expander("Selections", expanded=True):
#     col1,col2 = st.columns(2)
#     st.table(sel_row)
#     # st.info(sel_row[0]['description'])              
#     # col1.image(sel_row[0]['image_url'],caption=sel_row[0]['name'])




selected_rows = grid["selected_rows"]

if len(selected_rows):
    st.markdown('#### Selected')
    dfs = pd.DataFrame(selected_rows)

    dfsnet = dfs.drop(columns=['_selectedRowNodeInfo', '图片'])
    AgGrid(
        dfsnet,
        enable_enterprise_modules=False,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        reload_data=True,
        key='product_selected'
    )