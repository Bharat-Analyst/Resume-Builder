import streamlit as st

upload = "Read.txt"

with open(upload,"r") as f:
    f_content = f.readline()
    print(f_content)
