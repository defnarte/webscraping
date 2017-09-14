from bs4 import BeautifulSoup # From beautifulsoup 4 import beautiful soup (module name)
import urllib.request as ur # urllib is a built-in module for retriving urls, we import it as ur (shorter and easier to call)
from nltk.corpus import stopwords
import re
from time import sleep
from collections import Counter # Keep track of our term counts

"""
Workflow
1) Receive a key word(job) and enter it into jobstreet.com.sg
2) Browse through the list of job postings and scrape the html from each posting
3) 
"""
website = "https://www.jobstreet.com.sg/en/job/avpsenior-associate-data-science-engineer-corporate-treasury-group-finance-170002nq-6026076?fr=21"

def text_cleaner(website):
    """
        Use BeautifulSoup to obtain raw html from the site and convert it to text
        Input: Website
        Output: Cleaned text (no html formatting eg <p>,<tp>)
    """
    site = ur.urlopen(website).read()
    soup = BeautifulSoup(site,"html.parser") # Get the html from the website

    for script in soup(["script","style"]):
        script.extract()

    text = soup.get_text()


    lines = [line.strip() for line in text.splitlines()]

    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out  
        

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
        
        
    # Now clean out all of the unicode junk (this line works great!!!)
        

    text = text.decode('utf-8', 'ignore') # Need this as some websites aren't formatted

       
        
    text = re.sub("[^a-zA-Z.+3]"," ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
                                                # Also include + for C++
        
       
    text = text.lower().split()  # Go to lower case and split them apart
    stop_words = set(stopwords.words("english"))
    text = [w for w in text if not w in stop_words]
    text = list(set(text))

    return text
text = text_cleaner(website)

# Part 2
job_search = input("Enter a search term: ")
base_url = "https://www.jobstreet.com.sg/en/job-search/job-vacancy.php?key="
search_url = "https://www.jobstreet.com.sg/en/job-search/job-vacancy.php?key=" + job_search
search_site = ur.urlopen(search_url).read()
soup = BeautifulSoup(search_site,"html.parser")

job_urls = [link.get('href')for link in soup.find_all("a")]
job_urls = [x for x in job_urls if x is not None] # Remove None entries (they sometimes appear)

job_descriptions=[]
for j in range(0,len(job_urls)):
    if (job_urls[j].find('/job/')) != -1:
        description = text_cleaner(job_urls[j])
        if description:
            job_descriptions.append(description)
        sleep(1)

doc_frequency = Counter() # This will create a full counter of our terms. 
[doc_frequency.update(item) for item in job_descriptions] # List comp
        
prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                'Ruby':doc_frequency['ruby'],
                'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala']})
                  
analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                    'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                    'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3']})  

hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
            'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
            'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
            'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
            'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})
            
database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                'MongoDB':doc_frequency['mongodb']})

overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict # Combine our Counter objects
    
print(doc_frequency)
