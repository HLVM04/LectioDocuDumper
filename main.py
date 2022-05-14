import requests
from bs4 import BeautifulSoup
from pathlib import Path
import threading


schoolId = input('Skole ID: ')
elevId = input('Elev ID: ')
sessionId = input('Session ID: ')

cookies = {
    'LI': 't',
    'LastLoginExamno': str(schoolId),
    'ASP.NET_SessionId': sessionId,
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,da;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
}

params = {
    'elevid': str(elevId),
}
response = requests.get('https://www.lectio.dk/lectio/137/DokumentOversigt.aspx', params=params, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

treeContainer = soup.find('div', attrs={'id': 's_m_Content_Content_FolderTreeView'})
Path('output').mkdir(parents=True, exist_ok=True)

def traverseTree(folder, currentDir):
    for subfolder in folder.findChildren('div', recursive=False):
        subfoldername = subfolder.find('div', attrs={'class': 'TreeNode-title'}).text.strip()
        Path(currentDir+'/'+subfoldername).mkdir(parents=True, exist_ok=True)

        if len(subfolder.contents) > 1: # This checks if there are sub-subfolders
            traverseTree(subfolder.contents[1], currentDir+'/'+subfoldername)
        
        if 'lec-node-id' in subfolder.attrs:
            getDocuments(subfolder.attrs['lec-node-id'], currentDir+'/'+subfoldername)


def getDocuments(folderId, directory):
    params = {
        'elevid': str(elevId),
        'folderid': folderId,
    }
    response = requests.get('https://www.lectio.dk/lectio/137/DokumentOversigt.aspx', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    documentContainer = soup.find('div', attrs={'class': 'documentchooser-foldercontent-col'})

    for i in documentContainer.find_all('td', attrs={'class':'noWrap'}):
        for o in i.find_all('a'):
            if 'dokumenthent' in o.attrs['href']:
                print(o.attrs['href'], o.text)
                #threading.Thread(target=downloadDocument, args=("https://lectio.dk"+o.attrs['href'], directory, o.text)).start() # Warning: Multi-threading makes too many requests at once, and so Lectio bans you temporarily
                downloadDocument("https://lectio.dk"+o.attrs['href'], directory, o.text)


def downloadDocument(url, directory, name):
    response = requests.get(url, cookies=cookies, headers=headers)
    with open(directory+'/'+name, 'wb') as f:
        f.write(response.content)

traverseTree(treeContainer, 'output')
    