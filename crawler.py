# question 1

def get_page(url):
  try:
    import urllib.request
    page = urllib.request.urlopen(url).read()
    page = page.decode("utf-8")
    return page
  except:
    return ""


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
      url, endpos = get_next_target(page)
      if url:
        links.append(url)
        page = page[endpos:]
      else:
        break
    return links


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def add_toIndex(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def getclearpage(content):
  title = content[content.find("<title>")+7:content.find("</title>")]
  body = content[content.find("<body>")+6:content.find("</body>")]
  while body.find(">") != -1:
    start =  body.find("<")
    end =  body.find(">")
    body = body[:start] + body[end+1:]
  return title + body


def addPageToIndex(index, url, content):
  content = getclearpage(content)
  words = content.split()
  for word in words:
    add_toIndex(index, word, url)


def crawlWeb(seed):
  tocrawl = [seed]
  crawled = []
  index = {}
  graph = {}
  while tocrawl:
    page = tocrawl.pop()
    if page not in crawled:
      content = get_page(page)
      addPageToIndex(index, page, content)
      outlinks = get_all_links(content)
      graph[page] = outlinks
      union(tocrawl, get_all_links(content))
      crawled.append(page)
  return index, graph

# The returned graph is a directed graph where
# each URL acts as a node and is mapped to a list of URLs,
# forming the edges. The graph represents the interconnected
# structure of the web.


def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

index, graph = crawlWeb("https://searchengineplaces.com.tr/")

# 1b

output = f"The graph has {len(graph)} elements. These are:\n"

index = 1
for page in graph:
    outlinks = graph[page]
    output += f"\t{index}. [{page}]:{outlinks}\n"
    index += 1

print(output)

# 1c
def computeRanks(graph):
  d = 0.8
  N = len(graph)
  numloops = 10
  ranks = {}
  for page in graph:
    ranks[page] = 1/N

  for i in range(0, numloops):
    newranks = {}
    for page in graph:
      newrank = (1-d)/N
      for node in graph:
        if page in graph[node]:
          newrank = newrank + d*(ranks[node]/len(graph[node]))
      newranks[page] = newrank
    ranks = newranks
  return newranks

index , graph = crawlWeb ("https://searchengineplaces.com.tr/")
ranks = computeRanks ( graph )
print ( ranks )

ranks = computeRanks(graph)

output = ""
for page in ranks:
    rank = ranks[page]
    output += f"The rank of the page [{page}]: {rank}\n"
output

print(output)

# 1d
def rankedLookup(index, key, graph):
    ranks = computeRanks(graph)

    if key not in index:
        return []
    pages = list(set(index[key]))
    def get_rank(page):
        return ranks[page]
    sorted_pages = sorted(pages, key=get_rank, reverse=True)

    return sorted_pages

results = rankedLookup ( index , "in", graph )
for result in results :
  print ( result )

# 1e
def lookup(index, key, *args):


    warning_message = ("""This procedure takes 4 outputs these are:
1-An index
2-A key
3-A graph
4-A computing procedure respectively.
You have 2 option to use this lookup procedure: with or without ranking.
-If you intented to use it without page rank be sure you have given two inputs, index and key, respectively.
-If you intented to use it with page rank be sure you have given all four input in the given order.
INVALID INPUT COMBINATION: Please check the inputs."""
    )

    if len(args) == 0:
        if key in index:
            return list(set(index[key]))
        return []


    elif len(args) == 1:
        print(warning_message)

    elif len(args) == 2:
      graph, compute_ranks = args
      if key not in index:
        return []
      return rankedLookup(index, key, graph)

# Test1

see = lookup ( index , "in", graph , computeRanks ) # ATTENTION !!!!!
for e in see :
  print ( e )

# Test for duplicate outputs

assert rankedLookup( index , "in", graph ) == lookup( index , "in", graph , computeRanks )

# Test 2

see1 = lookup ( index , "in")
for e in see1 :
  print(e)

# Test 3

lookup ( index , "in", graph )

# Test 4

lookup ( index , "in", computeRanks )
