import Dataset
import EDA
import Predict
import streamlit as st

def main():
    tab1, tab2, tab3 = st.tabs(["Upload Dataset", "EDA", "Predict"])
    with tab1:
        Dataset.main()
    if st.session_state.name is None:
        with tab2:
            st.write('Please upload your dataset in "Upload dataset" tab first and then come back here 😊')
        with tab3:
            st.write('Please upload your dataset in "Upload dataset" tab first and then come back here 😊')
    else:
        with tab2:
            EDA.main()
        with tab3:
            Predict.main()

if __name__ == "__main__":
    main()