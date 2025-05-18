import webbrowser

loaded_sites={}

search=input("Search ->").lower()
to_find=search.split(' ')


with open("urls.txt",'r',encoding='utf-8') as file:
    lines=file.readlines()
    site=""
    missed=[]

    for i in to_find:
        if len(i)>0:
            missed.append(i)
        
    for line in lines:
        line=line.replace('\n','')
        if len(line)==0:
            continue
        if len(line)>6:
            if line[:3] == line[-3:] and "===" == line[:3]:
                #print(site,missed)
                if len(missed)>0:
                    if len(site)>0:
                        loaded_sites.pop(site)
                        
                    missed=[]
                    
                site=line[3:-3]
                loaded_sites[site]=0
                for i in to_find:
                    if len(i)>0:
                        missed.append(i)
                    
                continue
            
        word=line.split(' ')
        if len(word)<2 or len(word[0])==0:
            continue

        if word[0].lower() in to_find:
            loaded_sites[site]+=int(word[1])
            if word[0].lower() in missed:
                missed.remove(word[0].lower())

    if len(site)>0 and len(missed)>0:
        loaded_sites.pop(site)
        
biggest=['link',-1]

for link,weight in loaded_sites.items():
    if weight>biggest[1]:
        biggest=[link,weight]

if not(biggest[1]==-1):
    print(list(loaded_sites.keys()))
    print('\n\n',biggest)


    input("Press Enter to open")
    webbrowser.open(biggest[0])
else:
    input("No refences found :(")
