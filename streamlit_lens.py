import json

import requests as re
import streamlit as st

query = """ query globalProtocolStats {
  globalProtocolStats {
    totalProfiles
    totalPosts
    totalComments
    totalCollects
    totalMirrors
  }
} """

url = "https://api.lens.dev/"

headers = {"content-type": "application/json"}

r = re.post(url, json={"query": query}, headers=headers)


def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


st.write(""" # Lens Data """)

json_data = json.loads(r.text)
flat = flatten_json(json_data)

st.text("Total Profiles: {}".format(flat["data_globalProtocolStats_totalProfiles"]))
st.text("Total Posts: {}".format(flat["data_globalProtocolStats_totalPosts"]))
st.text("Total Comments: {}".format(flat["data_globalProtocolStats_totalComments"]))
st.text("Total Collects: {}".format(flat["data_globalProtocolStats_totalCollects"]))
st.text("Total Profiles: {}".format(flat["data_globalProtocolStats_totalProfiles"]))
