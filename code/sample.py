# Our aim is scrape as many For Rent ads as we can to create a list of prospective landlords.
# I’ll show a scrape for two examples from Kijiji.  Note other websites are encouraged for use.  To keep things simple, I’ll take several shortcuts like feed the URLs to be scraped myself instead of automatically and only scrape the address, price, and the numbers of bedrooms/bathrooms.  I just want to get a feel for what the end product might look like and the steps to get there.


# First time setup ------------------------------
# pip install beautifulsoup4
# pip install lxml
# pip install future

# Script ----------------------------------------
from bs4 import BeautifulSoup
import csv

# Get a copy of the first example we'll scrape locally (this would need to be automated)
# https://www.kijiji.ca/v-apartments-condos/ottawa/beautiful-clean-house-for-rent/1510669287
# https://www.kijiji.ca/v-apartments-condos/ottawa/eastwood-park-apartments-3-bedroom-apartment-for-rent/1508660354

page_file = ["Beautiful & Clean House for Rent Long Term Rentals Ottawa Kijiji.htm", "Eastwood Park Apartments - 3 Bedroom Apartment for Rent Long Term Rentals Ottawa Kijiji.htm"]

# extract fields we want 
with open("landlords.csv", "w", newline='') as csvfile:

    f = csv.writer(csvfile)
    # using the field names from the template from Alliance to End Homelessness found in https://public.3.basecamp.com/p/5KcRbBj2gFpYEuwF11vH9uin
    f.writerow(["Address", "Building Type", "Rental Type", "Rent $", "Bathroom"]) 

    for page in page_file:

        soup = BeautifulSoup(open(page), features="lxml")

        try: 
            # get address
            address = soup.find("span", {"class": "address-3617944557"}).get_text()

            # get house type, # bedrooms, and # bathrooms
            rooms = soup.findAll("span", {"class": "noLabelValue-3861810455"})    
            house_type = rooms[0].get_text()
            bedrooms = rooms[1].get_text()
            bathrooms = rooms[2].get_text()

            # get price
            price = soup.find("div", {"class": "priceWrapper-1165431705"}).findChild().get_text()

        except: 
            print("bad string{}".format(page))
            continue

        f.writerow([address, house_type, bedrooms, price, bathrooms])
