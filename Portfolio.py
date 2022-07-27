import streamlit as st
import Build
import Optimize

def main():
    tab1, tab2 = st.tabs(["Build", "Optimize"])
    with tab1:
        Build.main()
    with tab2:
        Optimize.main()


if __name__ == "__main__":
    main()