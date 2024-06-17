#this file contains all the web scraping methods that have to do with PLAYER data.

#imports:
from bs4 import BeautifulSoup
import requests

class Player:
    #class initialization
    def __init__(self, playername):
        self.playername = playername
        self.playerletter = playername.split()[1][0]
        self.playercode = self.setPlayerCode()
        self.url = None
        self.soup = None
        self._initialize_soup()

    #method to set the player code (this is to locate the specific url on basketball-reference that holds the player's data.)
    def setPlayerCode(self):
        lst = self.playername.split()
        playercode = ""
        counter = 0
        for i in lst[1]:
            if counter >= 5:
                break
            counter += 1
            playercode += i
        playercode += lst[0][0] + lst[0][1]
        return playercode

    #initializing the beautiful soup object that will scrape the data.
    def _initialize_soup(self):
        try:
            self.url = requests.get(f"https://www.basketball-reference.com/players/{self.playerletter}/{self.playercode}01.html")
            if self.url.status_code!=200:
                raise Exception("Player data not found.")
            self.soup = BeautifulSoup(self.url.text, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching player data: {e}")
            self.url = None
            self.soup = None

    #method to fetch a player's profile data.
    def playerProfile(self):
        if self.soup:
            playerImage = self.soup.find("div", class_ ="media-item").find("img")["src"]
            name_tag = self.soup.find("strong")
            name = name_tag.text if name_tag else "N/A"

            # twitter_tag = self.soup.find("a", href="https://twitter.com/ZachLaVine")
            # twitter = twitter_tag.text if twitter_tag else "N/A"
            #
            # instagram_tag = self.soup.find("a", href="https://instagram.com/zachlavine8")
            # instagram = instagram_tag.text if instagram_tag else "N/A"

            allstrongs = self.soup.find_all("strong")
            position = "NA"
            shooting = "NA"
            HS = "NA"
            college = "NA"
            experience = "NA"
            color = "#FFFFFF"
            for strongthing in allstrongs:
                if strongthing.text.strip() == "Position:":
                    text =  strongthing.next_sibling.strip().replace("\n","").replace("    ▪", "")
                    position = text if text else "NA"
                elif strongthing.text.strip() == "Shoots:":
                    text = strongthing.next_sibling.strip().replace("\n","").replace("    ▪", "")
                    shooting = text if text else "NA"
                elif strongthing.text.strip() == "College:":
                    text = strongthing.next_sibling.next_sibling.text
                    college = text if text else "NA"
                elif strongthing.text.strip() == "High School:":
                    text = strongthing.next_sibling.strip().replace("\n","").replace("    ▪", "")
                    HS = text if text else "NA"
                elif strongthing.text.strip() == "Experience:":
                    text = strongthing.next_sibling.strip().replace("\n","").replace("    ▪", "")
                    experience =  text if text else "NA"

            seasonGames = 0
            careerGames = 0
            seasonPPG = 0
            careerPPG = 0
            seasonRPG = 0
            careerRPG = 0
            seasonAPG = 0
            careerAPG = 0
            seasonFG = 0
            careerFG = 0
            season3 = 0
            career3 = 0
            seasonft = 0
            careerft = 0
            seasonefg = 0
            careerefg = 0
            seasonper = 0
            careerper = 0
            seasonws = 0
            careerws = 0


            #first set of stats
            finalSet = []
            firstpoptips = self.soup.find_all("div", class_ = "p1")
            for tip in firstpoptips:
                allps = tip.find_all("p")
                for i in allps:
                    finalSet.append(i.text.strip())

            secondpoptips = self.soup.find_all("div", class_ = "p2")
            for tip in secondpoptips:
                allps = tip.find_all("p")
                for i in allps:
                    finalSet.append(i.text.strip())

            seasonGames = finalSet[0] if finalSet[0] else 0
            careerGames = finalSet[1] if finalSet[1] else 0
            seasonPPG = finalSet[2] if finalSet[2] else 0
            careerPPG = finalSet[3] if finalSet[3] else 0
            seasonRPG = finalSet[4] if finalSet[4] else 0
            careerRPG = finalSet[5] if finalSet[5] else 0
            seasonAPG = finalSet[6] if finalSet[6] else 0
            careerAPG = finalSet[7] if finalSet[7] else 0
            seasonFG = finalSet[8] if finalSet[8] else 0
            careerFG = finalSet[9] if finalSet[9] else 0
            season3 = finalSet[10] if finalSet[10] else 0
            career3 = finalSet[11] if finalSet[11] else 0 
            seasonft = finalSet[12] if finalSet[12] else 0
            careerft = finalSet[13] if finalSet[13] else 0

            player_info = {
                "Name": name,
                "Position": position,
                "Shooting arm": shooting,
                "College": college,
                "HS": HS,
                "Experience" : experience,
                "Image": playerImage,
                "TeamColor":color,
                "Season Games":seasonGames,
                "Career Games": careerGames,
                "Career PPG": careerPPG,
                "Season PPG": seasonPPG,
                "Career RPG": careerRPG,
                "Season RPG": seasonRPG,
                "Career APG": careerAPG,
                "Season APG": seasonAPG,
                "Career FG%": careerFG,
                "Season FG%": seasonFG,
                "Career 3FG%": career3,
                "Season 3FG%": season3,
                "Career FT%": careerft,
                "Season FT%": seasonft,
            }
            return player_info
        else:
            print("Player data not available")

    #getting the stats for the last few games for a player.
    def lastFewGames(self):
        table = self.soup.find_all("table")[0] ##the code below can be used to get any table on the page, just change the index on this line.
        myrows = table.find_all('tr')
        finaldata = []
        for row in myrows:
            data = row.find_all('td')
            rowdata = [data.text.strip() for data in data]
            finaldata.append(rowdata)
        finaldata.pop(0)
        return finaldata

player = Player("zach lavine")
print(player.lastFewGames())