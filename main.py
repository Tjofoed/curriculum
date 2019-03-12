import urllib.request, json, subprocess, os, glob
import git

def getCloneUrls():
    cloneUrlList = []
    # get sourcecode from api
    response = urllib.request.urlopen('https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100')
    # decode into utf-8
    html = response.read().decode('utf-8')
    file = open('urls.txt', 'w+')
    file.write(html)
    # open file after saving it
    newFile = open('urls.txt', 'r')
    for line in newFile:
        # split words in order to check the words on each line
        words = line.split('"')
        index = 0
        for word in words:
            # search for the 'clone_url' part
            if "clone_url" in word:
                # save the link from the line
                cloneUrlList.append(words[index +2])
            index = index + 1
    return cloneUrlList

def cloneGits(cloneUrlList):
    for url in cloneUrlList:
        # slice the folder name from the url list
        folderName = url[49:-4]
        # if folder exists, do git pull
        if os.path.exists(folderName):
            os.chdir(folderName)
            # go into folder and pull items
            subprocess.run('git pull ' + url)
            os.chdir('..')
        # else clone folders to directory
        else:
            subprocess.run('git clone ' + url)

def getReadmes():
    readmeList = []
    # check every folder for readme files and add to list
    for filename in glob.iglob('*/README.md', recursive=True):
        readmeList.append(filename)
    return readmeList

def getReqReading(readmeList):
    reqReadingList = []
    # search every readme file
    for readme in readmeList:
        with open(readme) as file:
            for line in file:
                # search lines for the string 'required reading'
                if "Required reading" in line:
                    for line in file:
                        # add lines to the list untill newline or #
                        if line.startswith("\n" or "#"):
                            break
                        elif line.startswith("*"):
                            reqReadingList.append(line)
    return reqReadingList

def reqReadingFile(reqReadingList):
    reqReadingSet = set()
    # add list to set in order to get rid of dublicates
    for line in reqReadingList:
        reqReadingSet.add(line)
    # add header to file
    file = open("required_reading.md", "w+")
    file.write("# Required Reading\n> Python Elective I Spring 2019\n\n")
    # lowercase every line and then capitalize the first letter
    print(sorted(reqReadingSet))
    for line in sorted(reqReadingSet):
        lowerLine = line.lower()
        capLine = lowerLine.lower().replace(lowerLine[3], lowerLine[3].capitalize(), 1)
        file.write(capLine)

def gitConnect():
    # git commands to add/commit and push if repository already exists
    if os.path.exists('.git'):
        subprocess.run('git add ./required_reading.md')
        subprocess.run('git add ./main.py')
        subprocess.run('git commit -m "Update')
        subprocess.run('git push --force origin master')
    # else initialize git and remote add
    else:
        subprocess.run('git init')
        subprocess.run('git add ./required_reading.md')
        subprocess.run('git add ./main.py')
        subprocess.run('git commit -m "Update readme"')
        subprocess.run('git remote add origin https://github.com/Tjofoed/curriculum.git')
        subprocess.run('git push --force -u origin master')

def main():
    # cloneUrlList = getCloneUrls()
    # cloneGits(cloneUrlList)
    # readmeList = getReadmes()
    # reqReadingList = getReqReading(readmeList)
    # reqReadingFile(reqReadingList)
    gitConnect()

if __name__ == '__main__':
    main()