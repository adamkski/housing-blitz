import json 

import requests 

from bs4 import BeautifulSoup

def get_all_ad_hrefs(url = f"https://www.airbnb.ca/s/Ottawa--ON/homes?page=1"):
    page_number=1
    all_hrefs, all_titles=[],[]
    base = 'https://www.airbnb.ca'
    while 1:
        
        print(f'Collecting links to advertisement from page number {page_number}.', end="")
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'lxml') 
        print("...", end="")
        data1=soup.findAll('script', {'type':'application/json'}) 
        
        links = [i.get('href') for i in soup.findAll('a', {"class":'_gjfol0'})]
        print("...")
        titles = [i.text.strip() for i in soup.findAll('div',{'class':'_1c2n35az'})]

        print(f"collection from page number {page_number} complete!\n")
        #if (prev_links == links):
        #    break
        #else:
        #    prev_links = links
        #    all_hrefs.extend(links)
        #    all_titles.extend(titles)
        #    if page_number == 3:
        #        break
        next_page = soup.findAll('a', {'class':'_1cnw8os'})
        if next_page[-1].get('aria-label') == "Next":
            url = base+next_page[-1].get('href')
            all_hrefs.extend(links)
            all_titles.extend(titles)
        elif next_page[-1].get('aria-label') == "Previous":
            print("\n\nCOLLECTION COMPLETE!!")
            break
        page_number += 1
    return all_hrefs, all_titles


def get_advertisement_json():

    url = (f"https://www.airbnb.ca/s/Ottawa--ON/homes?page={page_number}")

    base = 'https://www.airbnb.ca'
    
    hrefs, titles = get_all_ad_hrefs(url)
    
    soup = BeautifulSoup(response.content, 'lxml') 

    data1=soup.findAll('script', {'type':'application/json'}) 

    links = [i.get('href') for i in soup.findAll('a', {"class":'_gjfol0'})]
    
    #links = [i.get('href') for i in links]

    titles = [i.text.strip() for i in soup.findAll('div',{'class':'_1c2n35az'})]


    response1 = requests.get(base+links[10].get('href'))

    def showtypes(data):
     for i in data.keys():
      if type(data[i]) == str or type(data[i]) == dict or type(data[i]) == list:
       print(f"{i}: {type(data[i])}, has length: {len(data[i])}\n")
      else:
       print(f"{i}: {type(data[i])}\n")

    soup1=BeautifulSoup(response1.content, 'lxml') 

    data1=soup1.findAll('script', {'type':'application/json'}) 

    data1 = json.loads(data1[3].text.strip()) 
    pass

def get_advertisement_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    
    javascripted_data = soup.find_all('script', {'type': 'application/json'})
    
    main_data = json.loads(javascripted_data[3].text.strip())
    
    from_niobeMinimalClientData = main_data['niobeMinimalClientData']

    denormalized_key_niobeMinimalClientData = from_niobeMinimalClientData[0][1]
    
    data_within = denormalized_key_niobeMinimalClientData['data']
    
    merlin = data_within['merlin']
    
    pdpsects = merlin['pdpSections']
    
    sections = pdpsects['sections'] 
    
    #sectionplacements = pdpsects['sectionPlacements']
    
    for i in sections:
        keylist = list(i['section'].keys())
        if 'htmlDescription' in keylist:
            descdict = i['section']
    
    return descDict
    
def main(links, titles):
    base = 'https://www.airbnb.ca'
    
    airbnb_data = []
    
    print(f'Collecting data from each of the {len(links)} advertisement collected!\n')
    skipped = 0
    for index, link in enumerate(links):
        an_ad = {}
        an_ad['url'] = base+link
        an_ad['title'] = titles[index]
        try:
            an_ad['description_js'] = get_advertisement_details(an_ad['url'])
        except Exception as e:
            print(f'{index}: url: {base+link} caused {e} error!\n')
            skipped += 1
        airbnb_data.append(an_ad)
    print(f'\n\n TOTAL SKIPPED DATA = {skipped}')
    return airbnb_data

if __name__ == "__main__":
    print('Module Loaded!')
    url='https://www.airbnb.ca/s/Ottawa--ON/homes?page=1'
    links, titles = get_all_ad_hrefs(url)
    data = main(links=links,
                titles = titles)
    
    with open('airbnb_collection_json.json', 'w') as f:
        json.dump(data, f)