import requests
from requests.auth import HTTPBasicAuth
from pyquery import PyQuery
from zipfile import ZipFile
from io import BytesIO
from os import mkdir
from os.path import join, exists
from subprocess import Popen
from json import load
import atexit
from sys import exit

# region configload
# Open and read configuration file
try:
    with open("config.json", encoding="utf-8") as f:
        config = load(f)
except FileNotFoundError:
    print("config.json nem található!")
    exit()

# Validate path since it is user provided
if(not exists(config["save_path"])):
    raise IOError("Invalid path!")

# Init configuration variables
url = config["biro_url"]
username = config["username"]
password = config["password"]
if("editor" in config.keys()):
    editor = config["editor"]
else:
    editor = False
logindata = None
# endregion

# region login


def login(url, username, password):
    req = requests.post(
        url + "beleptet.php",
        allow_redirects=False,
        data={
            "loginnev": username,
            "passwd": password,
            "y": 0,
            "x": 0
        }
    )
    if req.status_code == 302:
        return req.cookies
    else:
        ""


def logout(url, cookiejar):
    print("Kijelentkezés...")
    requests.post(
        url + "kilepes.php",
        cookies=cookiejar
    )


logindata = login(url, username, password)
# Register logout function as an exit handler
if(logindata):
    atexit.register(logout, url, logindata)
# endregion


# region htmlparse
class Task():
    subject = None
    task = None
    deadline = None
    points = None
    downloadUrl = None


def parse(html):
    # Parse the table from the HTML code and load into objects
    subject = None
    tasks = []
    pq = PyQuery(html)
    for tr in pq("#content>table>tr"):
        # We need an offset, because the subject name is contained in a data
        # cell but it doesn't occur in every line, so we need to check for it
        offset = 0
        if tr[0].attrib:
            subject = tr[0].text
            offset += 1
        tmp = Task()
        tmp.subject = subject
        tmp.task = tr[0+offset].text
        tmp.downloadUrl = tr[2+offset][0].attrib["href"]
        tmp.deadline = tr[3+offset].text
        tmp.points = tr[4+offset].text.replace(" ", "").replace("\n", "")
        tasks.append(tmp)
    return tasks


html = requests.get(url + "feladat_keres.php", cookies=logindata)
tasks = parse(html.text.replace("\r\n", "\n"))
# endregion

# region output
# Size of each column in the output
paddings = [
    3,
    35,
    44,
    21,
    10
]

output_f = "{:^{paddings[0]}}|{:^{paddings[1]}}|{:^{paddings[2]}}|{:^{paddings[3]}}|{:^{paddings[4]}}|"

print(output_f.format(
    "#", "Tantárgy", "Feladat", "Határidő", "Pontszám",
    paddings=paddings))

# Print horizontal separators
for padding in paddings:
    print("-"*padding+"|", end="")

# Prints tasks
i = 0
for task in tasks:
    print(output_f.format(
        i,
        task.subject,
        task.task,
        task.deadline,
        task.points,
        paddings=paddings
    ))
    i += 1
# endregion

# region select
selection = input("\nAdjon meg egy feladatazonosítót, vagy válassza az (u)tolsót vagy a (k)ilépést: ")
while(not(
    selection == "u" or
    selection == "k" or
    (selection.isdigit() and int(selection) < len(tasks))
)):
    selection = input("\nHibás bemenetet adott meg, próbáld újra: ")

if(selection == "k"):
    # Exit from program
    exit()
elif(selection == "u"):
    # Choose last task
    selection = -1
else:
    # Choose task by ID
    selection = int(selection)

# endregion

# region download
print("Választott feladat: {}, letöltés folyamatban...".format(
    tasks[selection].task
))
# Download task zip file
file = requests.get(
    url + tasks[selection].downloadUrl,
    auth=HTTPBasicAuth(
        username,
        password
    )
).content
print("Letöltés kész!")
# Reformat name
foldername = tasks[selection].deadline.replace(" ", "_").replace(":", "-")
# Create valid, cross-OS path
path = join(config["save_path"], foldername)
try:
    mkdir(path)
except FileExistsError:
    print("Hiba! A mappa már létezik!")
    exit()
# Unzip file content into folder
print("Kicsomagolás folyamatban...")
zipfile_ob = ZipFile(BytesIO(file))
zipfile_ob.extractall(path)
print("Kicsomagolás kész!")
# endregion

# region editor
# Open chosen code editor
if(editor):
    print("Kódszerkesztő megnyitása...")
    Popen([editor, path], shell=True)
# endregion
