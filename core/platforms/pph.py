import requests, bs4
import re
from user_agents import UserAgents

API_ADDR = "https://www.peopleperhour.com/freelance-jobs"

def scrape(NO_PAGE):
    
    soup = bs4.BeautifulSoup(requests.get(API_ADDR,headers={"User-Agent":UserAgents["1"]}).text,"html.parser")
    
    # find app id and key  
    # pph api format: 
    # https://www.peopleperhour.com/v2/projects/listAll?app_id=[app_id]&app_key=[app_key]&include=remoteCountry%2Cwatchlists%2ConsiteLocation&page%5Bnumber%5D=[page.no]
    app_js = None
    for link in soup.find_all("script", src=True):
        if re.search(r"app.*.js",link["src"]):
            app_js = link["src"]
            break

    if app_js is None:
        print("Cannot find app.js")
        return
    app_js_request = requests.get(app_js,headers={"User-Agent":UserAgents["1"]})

    api_app_key = re.findall(r'API_APP_KEY:"(?P<key>\w+)"',app_js_request.text)[-1] #last one is for v2 api
    api_app_id = re.findall(r'API_APP_ID:"(?P<id>\w+)"',app_js_request.text)[-1] #last one is for v2 api
    
    with open ("pph-titles.txt","w",encoding="utf-8") as f:
        for i in range(1,NO_PAGE+1):
            response = requests.get(f"https://www.peopleperhour.com/v2/projects/listAll?app_id={api_app_id}&app_key={api_app_key}&include=remoteCountry%2Cwatchlists%2ConsiteLocation&page%5Bnumber%5D={i}"
            ,headers={
                "User-Agent":UserAgents["1"],
                "Accept" : "*/*",
                "Accept-Encoding" : "gzip, deflate, br",
                "Connection" : "keep-alive"
            })
            for post in response.json()["data"]:
                f.write(post["attributes"]["title"]+"\t"+post["attributes"]["category"]["cate_name"] + "\t" + post["attributes"]["sub_category"]["subcate_name"] +"\n")
    f.close()