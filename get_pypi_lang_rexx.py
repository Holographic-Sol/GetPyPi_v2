# Written by Benjamin Jack Cullen aka holographic_sol

import os
import time
import codecs
import requests
from bs4 import BeautifulSoup
import distutils.dir_util
import urllib.request


def main_funk(dl_loc):
    # Set Initial URL
    url = "https://pypi.org/search/?q=&o=&c=Programming+Language+%3A%3A+Rexx"

    # print('-source:', url)

    # Initial BeautifulSoup Configuration
    rHead = requests.get(url)
    data = rHead.text
    soup = BeautifulSoup(data, "html.parser")

    # print("-- crawling for page number href's...")

    # Initiate A List For Href Data We Can Use To Generate URL's And Crawl Further
    pg_list_1 = []

    # Default Is False And Should Only Be True If There Is More Than One Page
    page_bool = False

    # Parse Data Retrieved By Beautiful Soup
    for link in soup.find_all('a'):
        href = (link.get('href'))

        # Condition Statements For Refining Results
        if href != None:
            if 'page=' in href:
                if href not in pg_list_1:
                    # Isolate Numbers We Can Use For Predicting All Other Necessary URL's
                    idx = href.rfind('=')
                    var = href[idx + 1:]

                    # Append Isolated Numbers To A List Ready To Be Compared
                    pg_list_1.append(var)
                    page_bool = True

    # Initiate A List For Predicted URL's To Be Stored In
    pg_list_2 = []

    if page_bool is True:

        # Compare Numbers In List To Find the Highest Number Only If More Than One Page
        page_max = int(max(pg_list_1))

        # Set Iteration Count So We Only Generate The Number Of URL's We Predict Addresses For
        i = 0

        # First Page Stored Outside Of Loop
        pg_list_2.append(url)

        # Loop Predicting & Generating URL's
        while i <= page_max:
            str_i = str(i)
            page_url = url + '&page=' + str_i
            pg_list_2.append(page_url)
            i += 1
    else:
        # There Is Only One Page!? Manually Set Page Max And Populate The List With Base URL
        page_max = 0
        pg_list_2.append(url)

    # Initiate A List Ready To Store Module URL's
    pkg_url = []

    # Set Page Iteration Count
    i = 0

    # Loop Over Each Item In Page List Number 2
    for pg_list_2s in pg_list_2:

        # Each Iteration Re-Configures URL Using Predicted URL List
        url = pg_list_2[i]
        # print('-- crawling page:', i, '/', page_max, ' url:', url)

        # Re-Configure Beautiful Soup
        rHead = requests.get(url)
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")

        # Parse Data Retrieved By Beautiful Soup
        for link in soup.find_all('a'):
            href = (link.get('href'))

            # Set Condition For Accepted Strings
            if href != None and '/project/' in href:
                var = 'https://pypi.org' + href
                pkg_url.append(var)

                # Affirmation Module URL In Page Has Been Found And Next Intent Is To Redirect And Crawl Module URL
                # print('\n-- crawling project url:', var)

                # String Manipulation For Retrieving Project Name
                pjt_n = var.replace('https://pypi.org/project/', '')
                pjt_n = pjt_n.replace('/', '')
                # print('Project Name:', pjt_n)

                # Create Unique Directory & Complimentary Description File (Use When Look For Suitable Archived Modules)
                fname = pjt_n + '.txt'
                save_var = dl_loc + '\\' + pjt_n
                distutils.dir_util.mkpath(save_var)
                fullpath = save_var + '\\' + fname

                # Append String To Var To Reach Module Download Address
                dl_url = var + '#files'

                # Re-Configure Beautifil Soup
                rHead = requests.get(dl_url)
                data = rHead.text
                soup = BeautifulSoup(data, "html.parser")

                # Iteration Count Downloads Per Module
                i_2 = 1

                for link in soup.find_all('a'):
                    href2 = (link.get('href'))

                    # Set Condition For Accepted Strings
                    if href2 != None and 'https://files.pythonhosted.org/packages/' in href2:

                        # Count Download Files Per Module
                        # print('Project Download File {}:'.format(i_2), href2)

                        # String Manipulation To Create Suitable Path & File Names
                        idx2 = href2.rfind('/')
                        pac_name_ver = href2[idx2+1:]
                        dl_fullpath = save_var + '\\' + pac_name_ver

                        # Drop in Here If Module Version Does Not Exist Locally
                        if not os.path.exists(dl_fullpath):

                            # Scrub Old Project Description
                            codecs.open(fullpath, 'w', encoding="utf-8").close()

                            # Append String To Var To Reach Module Description Address
                            des_url = var + '#description'

                            # Re-Configure Beautiful Soup
                            rHead = requests.get(des_url)
                            data = rHead.text
                            soup = BeautifulSoup(data, "html.parser")

                            # Use Codecs Module To Write The Description File From Harvested Data Using Beautiful Soup
                            with codecs.open(fullpath, 'a', encoding="utf-8") as fo:
                                for row in soup.find_all('p'):
                                    text = row.get_text().strip()
                                    fo.write(text)
                            fo.close()

                            # Download Package(s)
                            print('page:', i, '/', page_max, 'saving:', pac_name_ver)
                            urllib.request.urlretrieve(href2, dl_fullpath)

                        # Drop In Here If Module Version Already Exists Locally
                        elif os.path.exists(dl_fullpath):
                            print('page:', i, '/', page_max, 'skipping:', pac_name_ver)

                        # Iteration Count Downloads Per Module
                        i_2 += 1

        # Page Iteration Count
        i += 1

    # print('-- complete.')


# Read Configuration File
with open('config.txt', 'r') as fo:
    for line in fo:
        line = line.strip()
        if line.startswith('DEST: ') and os.path.exists(line.replace('DEST: ', '')):
            dl_loc = line.replace('DEST: ', '')
            dl_loc = dl_loc + "/lang_rexx"
            distutils.dir_util.mkpath(dl_loc)
            main_funk(dl_loc)
        else:
            print('-- bad configuration file...')
