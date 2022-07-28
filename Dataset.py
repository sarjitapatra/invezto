import pymongo
import streamlit as st
import pandas as pd
import datetime
import toml
import yfinance as yf
from yahoofinancials import YahooFinancials

@st.experimental_singleton
def init_connection():

    USER_NAME = st.secrets["mongo"]["username"]
    PASSWORD = st.secrets["mongo"]["password"]
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

@st.experimental_memo(show_spinner = False, suppress_st_warning = True)
def upload_ticker(_db, name, choice):
        dataframe = yf.download(choice)
        dataframe.insert(loc = 0, column = "Date", value = pd.to_datetime(dataframe.index))
        idx = list(map(str, range(dataframe.shape[0])))
        dataframe.index = idx
        set_data(_db, name, dataframe) 

@st.experimental_memo(show_spinner = False, suppress_st_warning = True)
def upload_data(_db, dataframe, name):

        set_data(_db, name, dataframe)
        st.success('File successfully uploaded!')

def show(_db, name):
    if st.checkbox('Show me the dataframe'):
        collection = _db.get_collection(name)
        df = pd.DataFrame(list(collection.find({}))).astype({"_id": str})
        df = df.drop(columns = ["_id"])
        n = st.slider('How many rows do you want to see?', 1, df.shape[0])
        st.write("The first ", n, "rows of your entered file are shown :")
        st.write(df.head(n))        


def main():

    op = st.radio('Select your method of data upload', ('I want data from tickers', 'I want to upload custom data'))

    if op == 'I want data from tickers':
        if 'name' not in st.session_state:
            st.session_state.name = None

        choice = st.radio('Select a ticker', ("None", "MRNA", "PFE", "JNJ", "GOOGL", 
          "FB", "AAPL", "COST", "WMT", "KR", "JPM", 
          "BAC", "HSBC"))

        if choice != "None":
            db = init_connection()
            now = str(datetime.datetime.now())
            name = choice + now
            st.session_state.name = name
            with st.spinner('Please wait...'):
                upload_ticker(db, name, choice)
            show(db, st.session_state.name)
        else:
            st.error("Please enter a ticker value")

    else:
        if 'name' not in st.session_state:
            st.session_state.name = None

        st.header("Choose the .csv file")

        uploaded_file = st.file_uploader("Choose a file (Only .xls, .xlsx or .csv format accepted)")
        
        if uploaded_file is not None:

            db = init_connection()
            type = uploaded_file.name.split(".")
            now = str(datetime.datetime.now())
            if type[-1] == "xlsx":
                name = type[0] + now
                st.session_state.name = name 
                dataframe = pd.read_excel(uploaded_file, engine = 'openpyxl')
                with st.spinner('Please wait...'):
                    upload_data(db, dataframe, name)
                show(db, name)
            elif type[-1] == "xls":
                name = type[0] + now
                st.session_state.name = name 
                dataframe = pd.read_excel(uploaded_file)
                with st.spinner('Please wait...'):
                    upload_data(db, dataframe, name)
                show(db, name)
            elif type[-1] == "csv":
                name = type[0] + now
                st.session_state.name = name
                dataframe = pd.read_csv(uploaded_file, parse_dates = ["Date"])
                with st.spinner('Please wait...'):
                    upload_data(db, dataframe, name)
                show(db, name)
            else:
                st.error("Please upload a valid .xls, .xlsx or .csv file")


if __name__ == "__main__":
    main()