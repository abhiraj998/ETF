import streamlit as st
import requests
import openai
import os
import re
# st.write(
#     "Has environment variables been set:",
#     os.environ["api_key"] == st.secrets["api_key"]
# )



 
apiKey = os.environ.get("Api_key")
# print(apiKey)

 
def ytdName(name):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"give TOP 3 alternatives of {name} ETF, strictly within the same sector as {name}, return the results as a list only and i need only ticker names"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give ticker name only and consider the alternatives within the same sector, give"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print(generated_text)
    matches = re.sub(r'[\d+\.?]','', generated_text).split('\n')
    return matches

def MFPeers(name):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"give TOP 3 alternatives of {name} mutual funds, strictly within the same sector as {name}, return the results as a list only and i need only ticker names"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give ticker name only and consider the alternatives within the same sector."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print(generated_text)
    matches = re.sub(r'[\d+\.?]','', generated_text).split('\n')
    return matches

def stock_peers(stock_name):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url =f"https://financialmodelingprep.com/api/v4/stock_peers?symbol={stock_name}&apikey={api_key}".replace(" ","")
    response = requests.get(url)
    return  response.json()
 
 
 

def etf_sector(sector):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"return only the sector name for {sector} ETF?"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give the answer strictly in the following format 'the name etf focuses on sector name'"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print("generated_text = ",generated_text)
    pattern = re.compile(r'(?i)focuses\s(?:on\s(?:the\s)?)?(.*)')
    match = re.search(pattern, generated_text)
    if match != None:
        match = match.group(1).capitalize().strip(".")
    print("match = ",match)
    return match

def stock_sector(sector):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"return only the sector name for {sector} Stock?"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give the answer strictly in the following format 'the name Stock focuses on sector name'"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print("generated_text = ",generated_text)
    pattern = re.compile(r'(?i)focuses\s(?:on\s(?:the\s)?)?(.*)')
    match = re.search(pattern, generated_text)
    if match != None:
        match = match.group(1).capitalize().strip(".")
    print("match = ",match)
    return match

def mf_sector(sector):
    api_key = apiKey
    openai.api_key = api_key
    prompt_text = f"return only the sector name for {sector} Stock?"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "give the answer strictly in the following format 'the name mutual fund focuses on sector name'"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1
    )
    generated_text = response['choices'][0]['message']['content']
    print("generated_text = ",generated_text)
    pattern = re.compile(r'(?i)focuses\s(?:on\s(?:the\s)?)?(.*)')
    match = re.search(pattern, generated_text)
    if match != None:
        match = match.group(1).capitalize().strip(".")
    print("match = ",match)
    return match
 
def ytdValue(ytdName):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v3/stock-price-change/{ytdName}?apikey={api_key}"
    response = requests.get(url)
    return response.json()

def stock_price_change(stock_name):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url=f"https://financialmodelingprep.com/api/v3/stock-price-change/{stock_name}?apikey={api_key}".replace(" ","")
    response = requests.get(url)
    return  response.json()

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

def NameFromISIN(userinput):
    api_key = "7fd525b1eb69a710a24dd46dc1080e99"
    url = f"https://financialmodelingprep.com/api/v4/search/isin?isin={userinput}&apikey={api_key}"
    response = requests.get(url)
    return response.json()
 
 
 
hide_st_style="""
<style>
Mainenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)


 
 
def main():
    # st.title('ETF ADVISORY')
    user_input = st.text_input('Enter only Ticker:')
    ytd_name=""
    col1, col2 = st.columns(2)


    
    if st.button('ETF'):

        if len(user_input) > 5:
            if any(i.isdigit() for i in user_input)==True:
                try:
                    user_input = NameFromISIN(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ISIN, Please enter the ticker name.")
            else:
                try:
                    user_input = etfname(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ticker name, Please enter the ticker name.")
       

        try:        
            ytd_value_in = ytdValue(user_input)[0]['1Y']
            Userisin = ytdDescription(user_input)[0]['isin']
            st.success(f"""The YTD value for {user_input} ({Userisin}) is  {ytd_value_in}%, It focuses on the {etf_sector(user_input).replace(".",",")}. {ytdDescription(user_input.strip())[0]['description']}. It can be compared with below """)
            st.write('<p style= "color: red"> DISCLAIMER : *YTD Calculation is done for last 365 days</p>',unsafe_allow_html=True)
        except Exception as e:
            print(e)
        try:
            ytd_name = ytdName(user_input)
        except Exception as e:
            # print(e)
            st.error(f"Unable to find the alternatives for {user_input} ticker name.")
       
        table_data = []
        if ytd_name:
            yldlist=[]
            for name in ytd_name:
                pattern=r'[^a-zA-Z0-9\s]+'
                print(name)
                name= re.sub(pattern,'', name)
                ytd_value =ytdValue(name.strip())[0]['1Y']
                YTD_percentage=str(ytd_value)+"%"
                ytd_Sector = etf_sector(name)
                ytd_description = ytdDescription(name.strip())[0]['description']
                ytd_CompanyName = ytdDescription(name.strip())[0]['companyName']
                ytd_ISIN = ytdDescription(name.strip())[0]['isin']
                table_data.append([name.strip(), ytd_ISIN, ytd_CompanyName, YTD_percentage,ytd_Sector, ytd_description])
                yldlist.append([name.strip(), ytd_value, ytd_description])
           
            html_table = "<table><tr style='background:#B99855;color:#fff'><th>Ticker Name</th><th>ISIN</th><th>Company Name</th><th>1 Year Performance</th><th>Sector</th><th>Description</th></tr>"
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
            \nDisclaimer -  Investor should consider the risk associated and do there own risk analysis/consult there financial advisor before taking up the decision. """)

    if st.button('Mutual Fund'):
        if len(user_input) > 5:
            if any(i.isdigit() for i in user_input)==True:
                try:
                    user_input = NameFromISIN(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ISIN, Please enter the ticker name.")
            else:
                try:
                    user_input = etfname(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ticker name, Please enter the ticker name.")
        

        try:        
            ytd_value_in = ytdValue(user_input)[0]['1Y']
            Userisin = ytdDescription(user_input)[0]['isin']
            st.success(f"""The YTD value for {user_input} ({Userisin}) is  {ytd_value_in}%, It focuses on the {mf_sector(user_input).replace(".",",")}. {ytdDescription(user_input.strip())[0]['description']}. It can be compared with below """)
            st.write('<p style= "color: red"> DISCLAIMER : *YTD Calculation is done for last 365 days</p>',unsafe_allow_html=True)
        except Exception as e:
            print(e)
        try:
            ytd_name = MFPeers(user_input)
        except Exception as e:
            # print(e)
            st.error(f"Unable to find the alternatives for {user_input} ticker name.")
    
        table_data = []
        if ytd_name:
            yldlist=[]
            for name in ytd_name:
                pattern=r'[^a-zA-Z0-9\s]+'
                print(name)
                name= re.sub(pattern,'', name)
                print(name)
                ytd_value =ytdValue(name.strip())[0]['1Y']
                YTD_percentage=str(ytd_value)+"%"
                ytd_Sector = mf_sector(name)
                ytd_description = ytdDescription(name.strip())[0]['description']
                ytd_CompanyName = ytdDescription(name.strip())[0]['companyName']
                ytd_ISIN = ytdDescription(name.strip())[0]['isin']
                table_data.append([name.strip(), ytd_ISIN, ytd_CompanyName, YTD_percentage,ytd_Sector, ytd_description])
                yldlist.append([name.strip(), ytd_value, ytd_description])
        
            html_table = "<table><tr style='background:#B99855;color:#fff'><th>Ticker Name</th><th>ISIN</th><th>Company Name</th><th>1 Year Performance</th><th>Sector</th><th>Description</th></tr>"
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
            \nDisclaimer -  Investor should consider the risk associated and do there own risk analysis/consult there financial advisor before taking up the decision. """)
                
    if st.button('STOCK'):
        if len(user_input) > 5:
            if any(i.isdigit() for i in user_input)==True:
                try:
                    user_input = NameFromISIN(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ISIN, Please enter the ticker name.")
            else:
                try:
                    user_input = etfname(user_input)[0]['symbol']
                except Exception as e:
                    st.error(f"Can't find {user_input} ticker name, Please enter the ticker name.")
       
       
       
        try:        
            ytd_value_in = stock_price_change(user_input)[0]['1Y']
            Userisin = ytdDescription(user_input)[0]['isin']
            st.success(f"""The YTD value for {user_input} ({Userisin}) is  {ytd_value_in}%, It focuses on the {stock_sector(user_input).replace(".",",")}. {ytdDescription(user_input.strip())[0]['description']}. It can be compared with below """)
            st.write('<p style= "color: red"> DISCLAIMER : *YTD Calculation is done for last 365 days</p>',unsafe_allow_html=True)
        except Exception as e:
            print(e)
        try:
            # ytd_name = stock_peers(user_input)
            ytd_name = stock_peers(user_input)[0]['peersList']
        except Exception as e:
            # print(e)
            st.error(f"Unable to find the alternatives for {user_input} ticker name.")
       
        table_data = []
        if ytd_name:
            yldlist=[]
            for name in ytd_name[:3]:
                print(name)
                ytd_value =stock_price_change(name)[0]['1Y']
                YTD_percentage=str(ytd_value)+"%"
                ytd_Sector = stock_sector(name)
                ytd_description = ytdDescription(name.strip(" "))[0]['description']
                ytd_CompanyName = ytdDescription(name.strip(" "))[0]['companyName']
                ytd_ISIN = ytdDescription(name.strip(" "))[0]['isin']
                table_data.append([name.strip(" "), ytd_ISIN, ytd_CompanyName, YTD_percentage,ytd_Sector, ytd_description])
                yldlist.append([name.strip(" "), ytd_value, ytd_description])
           
            html_table = "<table><tr style='background:#B99855;color:#fff'><th>Ticker Name</th><th>ISIN</th><th>Company Name</th><th>1 Year Performance</th><th>Sector</th><th>Description</th></tr>"
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
            \nDisclaimer -  Investor should consider the risk associated and do there own risk analysis/consult there financial advisor before taking up the decision. """)
          
if __name__ == "__main__":
    main()
