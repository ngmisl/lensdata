import json

import requests as re
import streamlit as st

url = "https://api.lens.dev/"

headers = {"content-type": "application/json"}

# json flatten helper function
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


# Header
def header():
    st.markdown("# Lens Data")


# Sidebar defined here
def sideBar():
    with st.sidebar:
        st.markdown("### Socials")
        st.markdown("* [ngmisl.lens](https://lenster.xyz/u/ngmisl.lens)")
        st.markdown("* [ngmisl.twitter](https://twitter.com/ngmisl)")
        st.markdown("* [ngmisl.github](https://github.com/ngmisl/)")


# Total Protocol stats
def totalProtocol():
    query = """ query globalProtocolStats { globalProtocolStats {
    totalProfiles
    totalPosts
    totalComments
    totalCollects
    totalMirrors }
} """

    r = re.post(url, json={"query": query}, headers=headers)

    json_data = json.loads(r.text)
    flat = flatten_json(json_data)

    # Layout Start columns
    # Layout references: https://docs.streamlit.io/library/api-reference/layout

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        col1.write("Total Profiles")
        col1.write(flat["data_globalProtocolStats_totalProfiles"])
    with col2:
        col2.write("Total Posts")
        col2.write(flat["data_globalProtocolStats_totalPosts"])
    with col3:
        col3.write("Total Comments")
        col3.write(flat["data_globalProtocolStats_totalComments"])
    with col4:
        col4.write("Total Collects")
        col4.write(flat["data_globalProtocolStats_totalCollects"])
    with col5:
        col5.write("Total Mirrors")
        col5.write(flat["data_globalProtocolStats_totalMirrors"])


def topFollowed():

    # Top Followers
    query_followers = """ query ExploreProfiles {
  exploreProfiles(request: { sortCriteria: MOST_FOLLOWERS }) {
    items {
      id
      name
      bio
      isDefault
      attributes {
        displayType
        traitType
        key
        value
      }
      followNftAddress
      metadata
      handle
      picture {
        ... on NftImage {
          contractAddress
          tokenId
          uri
          chainId
          verified
        }
        ... on MediaSet {
          original {
            url
            mimeType
          }
        }
      }
      coverPicture {
        ... on NftImage {
          contractAddress
          tokenId
          uri
          chainId
          verified
        }
        ... on MediaSet {
          original {
            url
            mimeType
          }
        }
      }
      ownedBy
      dispatcher {
        address
        canUseRelay
      }
      stats {
        totalFollowers
        totalFollowing
        totalPosts
        totalComments
        totalMirrors
        totalPublications
        totalCollects
      }
      followModule {
        ... on FeeFollowModuleSettings {
          type
          contractAddress
          amount {
            asset {
              name
              symbol
              decimals
              address
            }
            value
          }
          recipient
        }
        ... on ProfileFollowModuleSettings {
        type
        }
        ... on RevertFollowModuleSettings {
        type
        }
      }
    }
    pageInfo {
      prev
      next
      totalCount
    }
  }
} """

    r_followers = re.post(url, json={"query": query_followers}, headers=headers)

    json_data_followers = json.loads(r_followers.text)
    flat_followers = flatten_json(json_data_followers)

    # Layout Start columns
    # Layout references: https://docs.streamlit.io/library/api-reference/layout
    
    st.markdown("---")

    #    st.write(flat_followers)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        col1.write("Top Followed")
        col1.write(
            f'1. [{flat_followers["data_exploreProfiles_items_0_handle"]}](https://lenster.xyz/u/{flat_followers["data_exploreProfiles_items_0_handle"]}) {flat_followers["data_exploreProfiles_items_0_stats_totalFollowers"]}'
        )
        col1.write(
            f'2. [{flat_followers["data_exploreProfiles_items_1_handle"]}](https://lenster.xyz/u/{flat_followers["data_exploreProfiles_items_1_handle"]}) {flat_followers["data_exploreProfiles_items_1_stats_totalFollowers"]}'
        )
        col1.write(
            f'3. [{flat_followers["data_exploreProfiles_items_2_handle"]}](https://lenster.xyz/u/{flat_followers["data_exploreProfiles_items_2_handle"]}) {flat_followers["data_exploreProfiles_items_2_stats_totalFollowers"]}'
        )
        col1.write(
            f'4. [{flat_followers["data_exploreProfiles_items_3_handle"]}](https://lenster.xyz/u/{flat_followers["data_exploreProfiles_items_3_handle"]}) {flat_followers["data_exploreProfiles_items_3_stats_totalFollowers"]}'
        )
        col1.write(
            f'5. [{flat_followers["data_exploreProfiles_items_4_handle"]}](https://lenster.xyz/u/{flat_followers["data_exploreProfiles_items_4_handle"]}) {flat_followers["data_exploreProfiles_items_4_stats_totalFollowers"]}'
        )


# App Layout
def main():
    header()
    sideBar()
    totalProtocol()
    topFollowed()


if __name__ == "__main__":
    main()
