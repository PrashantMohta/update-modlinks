import xml.etree.ElementTree as ET
import sys

name = ''
new_version = ''
new_link = ''
new_sha = ""

if len(sys.argv) < 5:
    print('''
Missing Parameters
          Usage : python update-modlinks.py <mod name> <new version> <new download link> <asset sha256>
''') 
    exit(1)
else:
    name = sys.argv[1]
    new_version = sys.argv[2]
    new_link = sys.argv[3]
    new_sha = sys.argv[4]
    
#create a valid version name for modlinks
new_version=''.join(c for c in new_version if c.isdigit() or c == ".")
version_seperators = new_version.count(".")
if(version_seperators > 3):
    print(new_version.split(".",4)[0:4])
    new_version = ".".join(new_version.split(".",4)[0:4])
else:
    need_seperators = 3 - version_seperators
    while need_seperators > 0:
        new_version = new_version + ".0"
        need_seperators-=1

print({'name':name,'version':new_version,'link':new_link , 'sha': new_sha})
tag_name = "{https://github.com/HollowKnight-Modding/HollowKnight.ModLinks/HollowKnight.ModManager}Name"
tag_version = "{https://github.com/HollowKnight-Modding/HollowKnight.ModLinks/HollowKnight.ModManager}Version"
tag_link = "{https://github.com/HollowKnight-Modding/HollowKnight.ModLinks/HollowKnight.ModManager}Link"
tag_repo = "{https://github.com/HollowKnight-Modding/HollowKnight.ModLinks/HollowKnight.ModManager}Repository"

old_modlinks_data = {'name':'','version':'','link':'' , 'sha': '','repo':''}

tree = ET.parse('ModLinks.xml')
root = tree.getroot()
for child in root:
    if child.find(tag_name).text == name :
        old_modlinks_data['name'] = child.find(tag_name).text.strip()
        old_modlinks_data['version'] = child.find(tag_version).text.strip()
        old_modlinks_data['link'] = child.find(tag_link).text.strip()
        old_modlinks_data['sha']  = child.find(tag_link).get('SHA256').strip()
        old_modlinks_data['repo']  = child.find(tag_repo).text.strip()
        break

print(old_modlinks_data)

modlink_str_orig = open('ModLinks.xml','r').read()

#split out the section for this mod to find and replace in
startIndexOld = modlink_str_orig.find("<Name>"+old_modlinks_data['name']+"</Name>")
#handle case when multiple mods share the same repository
endIndexOld = startIndexOld + modlink_str_orig[startIndexOld:].find("<![CDATA["+old_modlinks_data['repo']+"]]>")
modlink_str = modlink_str_orig[startIndexOld:endIndexOld]

if len(old_modlinks_data['version']) > 0:
    modlink_str = modlink_str.replace(old_modlinks_data['version'],new_version)

if len(old_modlinks_data['link']) > 0:
    modlink_str = modlink_str.replace(old_modlinks_data['link'],new_link)

if len(old_modlinks_data['sha']) > 0:
    modlink_str = modlink_str.replace(old_modlinks_data['sha'],new_sha)

#modlinks surgery to inject the modified entry in place of the old entry
modlink_str = modlink_str_orig[:startIndexOld] + modlink_str + modlink_str_orig[endIndexOld:]

with open("ModLinks.xml", "w") as f:
    f.write(modlink_str)