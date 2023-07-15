import sys 
import time
import requests
from bs4 import BeautifulSoup

github_link = input("Enter the GitHub user link: ")
try:
    response=requests.get(github_link)
except Exception as e:
    error_type,error_obj,error_info=sys.exc_info()    
    print("Error for link: ",github_link)
    print(error_type,'Line:',error_info.tb_lineno)

time.sleep(2)
soup = BeautifulSoup(response.content, "html.parser")
img_element = soup.find("img", class_="avatar-user")
# Check if the profile image element was found
if img_element:
    # Get the source (URL) of the profile image
    image_url = img_element["src"]
        
    # Print the profile image URL
    print("Profile Image URL:", image_url)
else:    
    print("Failed to retrieve the GitHub profile page.")
