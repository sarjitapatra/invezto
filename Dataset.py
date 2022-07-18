import pymongo
import streamlit as st
import pandas as pd
import datetime

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    env_vars = [] # or dict {}
    with open('secrets.env') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            env_vars.append({'name': key, 'value': value}) # Save to a list

    USER_NAME = env_vars[0]["value"]
    PASSWORD = env_vars[1]["value"]
    conn_str = 'mongodb+srv://' + USER_NAME + ':' + PASSWORD + '@cluster0.e85qmcu.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(conn_str)
    database = client.Stock_Price
    return database

@st.experimental_memo(show_spinner = False)
def set_data(_db, name, dataframe):

    _db.create_collection(name)
    my_collection = _db.get_collection(name)
    my_collection.insert_many(dataframe.to_dict('records'))
    return

def upload_and_show_data(dataframe, name):

        with st.spinner('Please wait while we upload your dataset...'):
            db = init_connection()
            set_data(db, name, dataframe)

        st.success('File successfully uploaded!')

        if st.checkbox('Show me the dataframe'):
            collection = db.get_collection(name)
            df = pd.DataFrame(list(collection.find({}))).astype({"_id": str})
            df.drop(columns = ["_id"])
            n = st.slider('How many rows do you want to see?', 1, dataframe.shape[0])
            st.write("The first ", n, "rows of your entered file are shown :")
            st.write(dataframe.head(n))
        
        return


def main():

    if 'name' not in st.session_state:
        st.session_state.name = None

    st.header("Choose the .csv file")

    uploaded_file = st.file_uploader("Choose a file (Only .xls, .xlsx or .csv format accepted)")
    
    if uploaded_file is not None:

        type = uploaded_file.name.split(".")
        now = str(datetime.datetime.now())
        if type[-1] == "xlsx":
            name = type[0] + now
            st.session_state.name = name 
            dataframe = pd.read_excel(uploaded_file, engine = 'openpyxl')
            upload_and_show_data(dataframe, name)
        elif type[-1] == "xls":
            name = type[0] + now
            st.session_state.name = name 
            dataframe = pd.read_excel(uploaded_file)
            upload_and_show_data(dataframe, name)
        elif type[-1] == "csv":
            name = type[0] + now
            st.session_state.name = name
            dataframe = pd.read_csv(uploaded_file, parse_dates = ["Date"])
            upload_and_show_data(dataframe, name)
        else:
            st.error("Please upload a valid .xls, .xlsx or .csv file")


if __name__ == "__main__":
    main()