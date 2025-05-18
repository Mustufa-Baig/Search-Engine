from urllib.request import urlopen
from bs4 import BeautifulSoup
import webbrowser

url = input("Seed ->")
found={}
mains={}

limit=int(input("Limit ->"))

sparse_mode=False

print("Scanning",limit,'pages...')

def read_html(link):
    try:
        response = urlopen(link)
        html_content = response.read().decode('utf-8')
        
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(e)
        soup=""

    return soup
        

def find_urls(link,limit=limit,found=found,mains=mains):
    queue=[link]
    num=0
    cont_not_scanned=[link]
    
    while len(queue)>0:
        try:
            current=queue.pop(0)
            response = urlopen(current)
            html_content = response.read().decode('utf-8')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Example: Print the title of the page
            percentage=int(100.0*num/float(limit))
            try:
                print("\n"+str(percentage)+"%  Page ->",soup.title.text)
            except:
                print("\n"+str(percentage)+"%  Page ->",current)


            try:
                content=""
                ps=soup.find_all('p')+soup.find_all('h1')+soup.find_all('h2')+soup.find_all('h3')+soup.find_all('h4')
                for p in ps:
                    text=str(p).split('<')
                    for t in text:
                        cont=t.split('>')
                        if len(cont)==2:
                            if len(cont[1])>0:
                                content+=cont[1]+' '
                found[current]=content
            except:
                pass

            cont_not_scanned.remove(current)

                            
            # Example: Find all links on the page
            if len(soup.find_all('a'))>0:
                for l in soup.find_all('a'):
                    url=l.get('href')
                    if type(url)==str:
                        if "http" in url:
                            main=url.split("//")[1]
                            if "/" in main:
                                main=main.split('/')[0]
                            
                            if not(url in found or "wp-content" in url):
                                if main in mains:
                                    if mains[main]>=limit:
                                        continue
                                    else:
                                        mains[main]+=1
                                else:
                                    mains[main]=0
                                    
                                #print(num," = ",url)
                                found[url]=""
                                queue.append(url)
                                cont_not_scanned.append(url)
                                num+=1
                                if num>=limit:
                                    print(cont_not_scanned)
                                    if len(cont_not_scanned)>0:
                                        n=0
                                        for site in cont_not_scanned:
                                            n+=1
                                            soup=read_html(site)
                                            if type(soup)==str:
                                                continue
                                            
                                            try:
                                                content=""
                                                ps=soup.find_all('p')+soup.find_all('h1')+soup.find_all('h2')+soup.find_all('h3')+soup.find_all('h4')
                                                for p in ps:
                                                    text=str(p).split('<')
                                                    for t in text:
                                                        cont=t.split('>')
                                                        if len(cont)==2:
                                                            if len(cont[1])>0:
                                                                content+=cont[1]+' '
                                                found[site]=content
                                                #print(site," // ",content)
                                                print(n,"/",len(cont_not_scanned)," done")
                                            except Exception as e:
                                                print(n,"fail ->",e)
                                            

                                    return 'done'
                                
        except Exception as e:
            print(f"\nError: {e}")

        
urls=find_urls(url)
print("\n====\nDONE\n====")



print(mains)




def make_ref(text):
    ref_table={}
    text=text.replace('\t',' ').replace('\n',' ')
    words=text.split(" ")
    for word in words:
        if len(word)==0 or word==' ':
            continue
        if word in ref_table:
            ref_table[word]+=1
        else:
            ref_table[word]=0

    text=""

    for word,count in ref_table.items():
        if sparse_mode and count<=1:
            continue
        text+=word+" "+str(count)+'\n'

    return text

with open('urls.txt','w',encoding="utf-8") as file:
    for link,txt in found.items():
        text=""
        for e in txt:
            text+=str(e)
            #print(str(e))
        text+='\n'
        text='==='+link+'===\n'+make_ref(text)
        
        try:
            file.write(text)
        except Exception as e:
            print(e)


input("Done")
