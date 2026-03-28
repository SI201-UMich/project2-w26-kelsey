# SI 201 HW4 (Library Checkout System)
# Your name: Shivani Patel, Kelsey Lin, Mariah Cooperwood 
# Your student id: #0399 0808, #---, 32843209 
# Your email: shivapa@umich.edu, --- lanelle@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
# I asked Google Gemini for debugging help and code structure on certain parts of my code including the extra credit headers and url and loading_list nested if loops order but not the code itself.
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# Yes because I ensured the code itself was written by me and mainly refered to class slideshow and runestone notes for help, and only resorted to AI for structure and debugging.
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Shivani

    Load file data from html_path and parse through it to find listing titles and listing ids.
    
    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    f = open(html_path, encoding="utf-8-sig")
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('a')
    collect_info = []
    for tag in tags:
        link = tag.get('href')
        if link != None and '/rooms/' in link:
            parts = link.split('/rooms/')
            listing_id = parts[1].split('?')[0]
            title_id = tag.get('aria-labelledby')
            if title_id != None:
                title_tag = soup.find('div', id=title_id)
                if title_tag != None:
                    title = title_tag.text.strip()
                    collect_info.append((title, listing_id))
    return collect_info
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Mariah

    Parse through listing_<id>.html to extract listing details.
    
    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    #opening and reading in the file. 
    dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(dir, "html_files", f"listing_{listing_id}.html")
    
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()
        
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    
    policy_number = "Pending"

    if "Exempt" in text:
        policy_number = "Exempt"
    else:
        policy_match = re.search(r"(20\d{2}-00\d{4}STR|STR-000\d{4})", text)
        if policy_match:
            policy_number = policy_match.group()

    host_type = "regular"
    if "Superhost" in text:
        host_type = "Superhost"
    else:
        host_type = "regular"
    host_name = ""
    room_type = "Entire Room"

    # looking for a heading or div with "hosted by"
    host_line = ""

    for tag in soup.find_all(["h2", "div"]):
        if tag.get_text() and "hosted by" in tag.get_text().lower():
            host_line = tag.get_text(" ", strip=True)
            break

    if host_line != "":
        parts = host_line.split("hosted by")

        if len(parts) == 2:
            listing_subtitle = parts[0].strip()
            host_name = parts[1].strip()

            if "private" in listing_subtitle.lower():
                room_type = "Private Room"
            elif "shared" in listing_subtitle.lower():
                room_type = "Shared Room"
            else:
                room_type = "Entire Room"

   #initializing location_rating as a float. 
    location_rating = 0.0

    # trying JSON-style pattern and html
    location_match = re.search(r'"label":"Location","accessibilityLabel":"([0-9.]+) out of 5.0"', html)
    if location_match:
        location_rating = float(location_match.group(1))
    else:
        location_match = re.search(r'Location.*?aria-label="([0-9.]+) out of 5.0"', html, re.DOTALL)
        if location_match:
            location_rating = float(location_match.group(1))

    # returning the nested dictionary 
    return {
        listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }
    }
            

    


def create_listing_database(html_path) -> list[tuple]:
    """
    Mariah

    Use prior functions to gather all necessary information and create a database of listings.
    
    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:

    sorted_data = sorted(data, key = lambda x: x[6], reverse = True)
    header = ["Listing Title" , "Listing ID" , "Policy Number" , "Host Type" "Host , Name" , "Room Type" , "Location Rating"]
    f = open(filename, 'w', newlin ='', encoding = 'utf-8-sig')
    try:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerrows(sorted_data)
    finally:
        f.close()
        # can you do this part without use with and just use open() and close()? how
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Kelsey

    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    room = {}
    for listing in data:
        type = listing[5]
        location = listing[6]

        if location != 0.0:
            status = room.get(type, [0.0, 0])
            room[type][0] += location
            room[type][1] += 1
            room[type] = status
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Kelsey

    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid = []
    policy1 = r'^20\d{2}-00\d{4}STR$'
    policy2 = r'^STR-000\d{4}$'

    for listing in data:
        id = listing[1]
        num = listing[2]

        if num == "Pending" or num == "Exempt":
            continue

        if not(re.match(policy1, num) or re.match(policy2, num)):
            invalid.append(id)
            
        return invalid
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    Shivani

    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar?q=" + query
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = soup.find_all('h3')
    collect_info = []
    for tag in tags:
        info = tag.text.strip()
        if info != '':
            collect_info.append(info)
    return collect_info
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # Shivani

        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        results = load_listing_results(self.search_results_path)
        self.assertEqual(len(results), 18)
        self.assertEqual(results[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # Mariah

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # Mariah

        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")
        #Shivani

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        output_csv(self.detailed_data, out_path)
        with open(out_path, encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.assertEqual(rows[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"])


        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        #Kelsey

        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        #Kelsey
        
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass
# This is a test case generated by AI to check if my extra credit runs
    def test_google_scholar_searcher_airbnb(self):
        result = google_scholar_searcher("Airbnb")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for title in result:
            self.assertIsInstance(title, str)
            self.assertTrue(len(title) > 0)

def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)