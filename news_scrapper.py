from selenium import webdriver
import time
import json
import os
from firebase_admin import firestore
from uuid import uuid4
from firebase_admin import initialize_app



all_category = {}

# To add data to firebase
cred_path = "credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
firebase_app = initialize_app()
db = firestore.client()
channelRef = db.collection('channel')
categoryRef = db.collection('category')
newsRef = db.collection('news')


PATH = "/Users/yuzu/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.medscape.com/")
driver.maximize_window()

def addDataToFirebase(data:dict):
    
    for k,v in all_category.items():
        listOfNewsReference = []
        for e in v:
            if not list(newsRef.where('title', '==', e['Title'] ).get()):
                news_id = str(uuid4())
                listOfNewsReference.append(news_id)
                newsRef.document(news_id).set({
            "id": news_id,
            "title": e['Title'],
            "newsImage": e['NewsImage'],
            "date": e['Date'],
            "content": e['Content'],
            "url": e['URL'],
            "channel": e['Channel'],
            "likes": 0,
            "comments": [],
            })
            
                
                
            if channelRef.document(e['Channel']).get().exists == False:
                channelRef.document(k).set({
                    "channel": e['Channel'],
                    "channelImage": e['ChannelImage']
                })
        if "/" not in k:
            print(listOfNewsReference)
            doc_ref_category = categoryRef.document(k).get()
            if doc_ref_category.exists:
                print(len((categoryRef.document(k).get({
                        "news"
                    }).to_dict())['news']))
                if (len((categoryRef.document(k).get({
                        "news"
                    }).to_dict())['news']) == 0 or len(listOfNewsReference) == 0 ) :
                    categoryRef.document(k).update({
                        "news": listOfNewsReference
                    })
                else:
                    categoryRef.document(k).update({
                    "news": firestore.ArrayUnion(listOfNewsReference)
                })
            else:
                categoryRef.document(k).set({
                    "name":k,
                    "news": listOfNewsReference
                }) 
            
        
        
    print(categoryRef.get())
            
# to login
# /html/body/div[5]/main/section[2]/div/div/p[2]/a
# email field: /html/body/div/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div[1]/div/div/input
# password field: /html/body/div/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div[2]/div/div[1]/input
btn = driver.find_element_by_xpath("/html/body/div[5]/main/section[2]/div/div/p[2]/a")
btn.click()
time.sleep(5)
email = driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div[1]/div/div/input")
email.send_keys("shakyasahani0@gmail.com")
password = driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div[2]/div/div[1]/input")
password.send_keys("healer3910##")
login_btn = driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[2]/button")
login_btn.click()
time.sleep(5)


# ************************ to be changed ************************
for i in range(1,36):
    time.sleep(2)
    try:
        all_btn = driver.find_element_by_id("specialtyToggle")
        all_btn.click()
    except:
        driver.back()
        all_btn = driver.find_element_by_id("specialtyToggle")
        all_btn.click()
    time.sleep(1)

    # gets the link of the news category
    # sample: /html/body/div[5]/main/section[1]/div/div/a[2]
    # /html/body/div[5]/main/section[1]/div/div/a[37]


    category_link = driver.find_element_by_xpath(f"/html/body/div[5]/main/section[1]/div/div/a[{i}]")
    category_name = category_link.text
    category_link.click()

    news_list = []
    #todo make it 8
    for j in range(1, 8):
        news_dict = {}
        try:
            # gets the link of the category title
            # sample /html/body/div[5]/main/section[4]/div/ul/li[{}]/a[2]/div
            # /html/body/div[5]/main/section[4]/div/ul/li[3]/a[2]/div

            time.sleep(3)
            try:
                news_image = driver.find_element_by_css_selector(f"#bodypadding > main > section.hp_news.latest_news > div.section-container > ul.articles > li:nth-child({j}) > a:nth-child(1) > img")
                news_dict['NewsImage'] = news_image.get_attribute("src")
            except:
                news_dict["NewsImage"] = "https://img.medscapestatic.com/publication/ap_logo.png?interpolation=lanczos-none&resize=*:85"
            
            
            driver.execute_script("window.scrollTo(0,800)")

            time.sleep(6)
            
            try:
                title_name = driver.find_element_by_css_selector(f"#bodypadding > main > section.hp_news.latest_news > div.section-container > ul.articles.column1 > li:nth-child({j}) > a:nth-child(3) > div")
            except:
                title_name = driver.find_element_by_css_selector(f"#bodypadding > main > section.hp_news.latest_news > div.section-container > ul.articles.column1 > li:nth-child({j}) > a:nth-child(2) > div")

            news_dict["Title"] = title_name.text
            title_name.click()
            time.sleep(3)

            # gets the link of the channel name
            # sample: /html/body/div[5]/div[3]/div[1]/div[1]/div[1]/div/a[2]
            # /html/body/div[5]/div[3]/div[1]/div[1]/div[1]/div/a[2]
            channel_name = driver.find_element_by_xpath("//html/body/div[5]/div[3]/div[1]/div[1]/div[1]/div/a[2]")
            news_dict["Channel"] = channel_name.text

            try:
                channel_image = driver.find_element_by_css_selector("#column-left > div.title-area.has-badge > div.badge > img")
                news_dict["ChannelImage"] = channel_image.get_attribute("src")
            except:
                news_dict["ChannelImage"] = "https://img.medscapestatic.com/publication/ap_logo.png?interpolation=lanczos-none&resize=*:85"
                
            # gets the link of the D
            # sample: /html/body/div[5]/div[3]/div[1]/div[1]/div[2]/p[2]
            D = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[1]/div[1]/div[2]/p[2]")
            news_dict['Date'] = D.text

            
            
            # gets the link of the content
            # sample: /html/body/div[5]/div[3]/div[1]/div[4]/div/div[1]/div/p[2]
            # /html/body/div[4]/div[3]/div[1]/div[4]/div/div[1]/div
            
            
            description = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[1]/div[4]/div/div[1]/div[1]")
            print(description.text)

            print("description: {description} ") 
            news_dict['Content'] = description.text

            # gets the url of current page
            news_dict['URL'] = driver.current_url
            # print(news_dict)

            # store dictionary into a list
            news_list.append(news_dict)
            time.sleep(2)
            driver.back()
        except:
            continue

    all_category[category_name] = news_list

    time.sleep(2)
    driver.back()
    
addDataToFirebase(all_category)
with open("news_data.json", 'w') as f:
    json.dump(all_category, f, indent=4)
time.sleep(3)
driver.quit()

