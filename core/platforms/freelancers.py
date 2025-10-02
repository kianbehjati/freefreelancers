import bs4, requests
from user_agents import UserAgents

def get_api_start_index(page_no):
    # api page is determined by index , index = pageNo * 50(item per page count)
    index = (page_no - 1) * 50
    API_ADDR = f"https://www.freelancer.com/ajax/table/project_contest_datatable.php?tag=&type=false&budget_min=false&budget_max=false&contest_budget_min=false&contest_budget_max=false&hourlyrate_min=false&hourlyrate_max=false&hourlyProjectDuration=false&skills_chosen=false&languages=false&status=open&vicinity=false&countries=false&lat=false&lon=false&iDisplayStart={index}&iDisplayLength=50&iSortingCols=1&iSortCol_0=6&sSortDir_0=desc&format_version=3&"
    return API_ADDR


def scrape(NO_PAGE):
    with open ("freelancer-titles.txt","w",encoding="utf-8") as f:
        for i in range(1,NO_PAGE+1):
            API_ADDR = get_api_start_index(i)
            response = requests.get(API_ADDR
            ,headers={
                "User-Agent":UserAgents["1"],
                "Accept" : "*/*",
                "Accept-Encoding" : "gzip, deflate, br",
                "Connection" : "keep-alive"
            })
            for post in response.json()["aaData"]:
                
                title = post["project_name"]
                skills = [skill["name"] for skill in post["skills_info"][:3]]
                f.write(title+"\t"+str(skills[:3])+"\n")
    f.close()