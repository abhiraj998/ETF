import streamlit as st
import requests
import openai
import os
import re

apiKey = os.environ.get("Api_key")
# print(apiKey)
# apiKey = ""
 
def ytdName(name):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"give TOP 3 alternatives of {name} ETF, strictly within the same sector as {name}, return the results as a list only and i need only ticker names"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give ticker name only and consider the alternatives within the same sector"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print(generated_text)
    matches = re.sub(r'\d+\.?', '', generated_text).split('\n')
    print(type(matches))
    return matches
 
 
 
def Sector(sector):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"return only the sector name for {sector} ETF?"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give the answer strictly in the following format 'the name etf focuses on sector name"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    pattern = r'(?<=focuses on\s)(.*)'
    match = re.search(pattern, generated_text)
 
    return  match.group(1).lstrip("the")
 
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
 
 
 
hide_deploy_button_style = """
<style>
.st-emotion-cache-1wbqy5l.e17vllj40 { display: none !important; }
 
</style>
"""
st.markdown(hide_deploy_button_style, unsafe_allow_html=True)


 
 
def main():
    st.title('ETF ADVISORY')
    user_input = st.text_input('Enter only ETF Ticker:')
    ytd_name=""
    if st.button('Submit'):
       
        if len(user_input) >= 5:
                try:
                    user_input = etfname(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ticker name, Please enter the ticker name.")
       
        try:        
            ytd_value_in = ytdValue(user_input)[0]['ytd']
            Userisin = ytdDescription(user_input)[0]['isin']
            st.success(f"""The YTD value for {user_input} ({Userisin}) is  {ytd_value_in}%, It focuses on the {Sector(user_input).replace(".",",")}. It can be compared with below """)
            st.write('<p style= "color: red"> DISCLAIMER : *YTD Calculation is done from 02 Jan 2024</p>',unsafe_allow_html=True)
        except Exception as e:
            print(e)
        try:
            ytd_name = ytdName(user_input)
        except Exception as e:
            print(e)
            st.error(f"Unable to find the alternatives for {user_input} ticker name.")
       
        table_data = []
        if ytd_name:
            yldlist=[]
            for name in ytd_name:
                ytd_value =(ytdValue(name.strip(" "))[0]['ytd'])
                YTD_percentage=str(ytd_value)+"%"
                ytd_Sector = Sector(name)
                ytd_description = ytdDescription(name.strip(" "))[0]['description']
                ytd_ISIN = ytdDescription(name.strip(" "))[0]['isin']
                table_data.append([name.strip(" "), ytd_ISIN, YTD_percentage,ytd_Sector, ytd_description])
                yldlist.append([name.strip(" "), ytd_value, ytd_description])
           
            html_table = "<table><tr style='background:#B99855;color:#fff'><th>Ticker Name</th><th>ISIN</th><th>YTD Value</th><th>Sector</th><th>Description</th></tr>"
            for row in table_data[0:]:
                html_table += "<tr>"
                for cell in row:
                    html_table += f"<td>{cell}</td>"
                html_table += "</tr>"
            html_table += "</table>"
            st.markdown(html_table, unsafe_allow_html=True)
            max_row = max(yldlist, key=lambda x: x[1])
            max_value = max(max_row[1], ytd_value_in)
 
            if max_value == ytd_value_in:
                ytd_final = user_input
                ytd_value_final = max_value
            else:
                ytd_final = max_row[0]
                ytd_value_final = max_value
               
 
            st.success(f"""
            Based on performance (YTD) , the best fund  is the "**{ytd_final}**" with a return of "**{ytd_value_final}%**" Year to date.
            \nDisclaimer -  Investor should consider the risk associated and do there own risk analysis/consult there financial advisor before taking up the decision. TFO should not be responsible for any kind of Financials losses for the recommendation . The Platform is a part of TFO IT Operation and uses its own internal algorithms.
            \n
            \nFor any Complain please reach out to s.hameed@tfoco.com OR y.shabeeb@tfoco.com
            \nFor any Suggestion please reach out to s.suman@tfoco.com""")
               
 
if __name__ == "__main__":
    main()
