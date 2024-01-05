import streamlit as st
import requests
 
def ytdName(name):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v4/stock_peers?symbol={name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()
 
def ytdValue(ytdName):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v3/stock-price-change/{ytdName}?apikey={api_key}"
    response = requests.get(url)
    return response.json()
 
def ytdDescription(ytdValue):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v3/profile/{ytdValue}?apikey={api_key}"
    response = requests.get(url)
    return response.json()
 
def etfname(userinput):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v3/search-name?query={userinput}&apikey={api_key}"
    response = requests.get(url)
    return response.json()
 
 
 
# hide_st_style="""
# <style>
# #Mainenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>"""
# st.markdown(hide_st_style,unsafe_allow_html=True)
 
 
def main():
    st.title('ETF FINDER')
    user_input = st.text_input('Enter the ETF Name:')
    ytd_name=""
    if st.button('Submit'):
       
            if len(user_input) >= 5:
                try:
                    user_input = etfname(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ticker name, Please enter the ticker name.")
            try:        
                ytd_value_in = ytdValue(user_input)[0]['ytd']
                st.success(f"YTD for {user_input} is {ytd_value_in}%, it can be compared with below ")
            except Exception as e:
                k=e    
            try:
                ytd_name = ytdName(user_input)[0]['peersList']
            except Exception as e:
                st.error(f"Unable to find the alternatives for {user_input} ticker name.")
           
            table_data = []
            if ytd_name:
                yldlist=[]
                for name in ytd_name[:3]:
                    ytd_value =ytdValue(name)[0]['ytd']
                   
                    YTD_percentage=str(ytd_value)+"%"
                    ytd_description = ytdDescription(name)[0]['description']
                    table_data.append([name, YTD_percentage, ytd_description])
                    yldlist.append([name, ytd_value, ytd_description])
               
                html_table = "<table><tr><th>YTD Name</th><th>YTD Value</th><th>Description</th></tr>"
                for row in table_data[0:]:
                    html_table += "<tr>"
                    for cell in row:
                        html_table += f"<td>{cell}</td>"
                    html_table += "</tr>"
                html_table += "</table>"
                st.markdown(html_table, unsafe_allow_html=True)
                max_row = max(yldlist, key=lambda x: x[1])


                st.success(f"""Based on performance (YTD) , the best fund  is the "**{max_row[0]}**" with a return of "**{max_row[1]}%**" Year to date.
                           
                           
\nDisclaimer -  Investor should consider the risk associated and do there own risk analysis/consult there financial advisor before taking up the decision. TFO should not be responsible for any kind of Financials losses for the recommendation . The Platform is a part of TFO IT Operation and uses its own internal algorithms.
\n
\nFor any Complain please reach out to s.hameed@tfoco.com OR y.shabeeb@tfoco.com
\nFor any Suggestion please reach out to s.suman@tfoco.com""")
       
 
if __name__ == "__main__":
    main()