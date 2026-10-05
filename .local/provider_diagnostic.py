import httpx
for url,params in [('https://api.jikan.moe/v4/anime',{'q':'Cowboy Bebop','page':1,'limit':12,'sfw':'true'}),('https://openlibrary.org/search.json',{'q':'Pride and Prejudice','page':1,'limit':12,'fields':'key,title,author_name,first_publish_year,cover_i,number_of_pages_median'})]:
    try:
        r=httpx.get(url,params=params,timeout=30,headers={'User-Agent':'Codeboxd/1.0'})
        print(url,r.status_code,r.text[:180])
    except Exception as e: print(type(e).__name__,str(e))
