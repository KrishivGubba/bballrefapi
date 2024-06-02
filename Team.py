# Importing necessary libraries
from bs4 import BeautifulSoup
import requests

class TeamScraper:
    def __init__(self, teamcode):
        # Initialize the TeamScraper with the team code (e.g., Chicago Bulls have the team code CHI)
        self.teamcode = teamcode

    # Create the BeautifulSoup object to scrape the required data from a given URL
    def initializeSoup(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    # Get the roster of the team for a specified year
    def getRoster(self, year):
        try:
            allplayers = []
            # Initialize BeautifulSoup for the team's page of the specified year
            soup = self.initializeSoup(f"https://www.basketball-reference.com/teams/{self.teamcode}/{year}.html")
            tables = soup.find_all("table")
            roster = tables[0]  # Assuming the first table contains the roster
            rows = roster.find_all("tr")
            for row in rows:
                data = row.find_all("td")
                data1 = [data.text.strip() for data in data]
                allplayers.append(data1[0:2])  # Extract the first two columns (Player and Position)
            allplayers.pop(0)  # Remove the header row
            for i in allplayers:
                # Convert position abbreviations to full names
                match i[1]:
                    case "PG":
                        i[1]= "Point Guard"
                    case "C":
                        i[1] = "Center"
                    case "SG":
                        i[1] = "Shooting Guard"
                    case "SF":
                        i[1] = "Small Forward"
                    case "PF":
                        i[1] = "Power Forward"
            res = {}
            # Create a dictionary with player names as keys and positions as values
            for i in range(len(allplayers)):
                res[allplayers[i][0]] = allplayers[i][1]
            return res
        except:
            return None

    # Get the season averages of the team for a specified year
    def getSeasonAverages(self, year):
        # Dictionary mapping team codes to their StatMuse codes
        nba_codes = {
            "BOS": "boston-celtics-1",
            "CLE": "cleveland-cavaliers-42",
            "MIL": "milwaukee-bucks-39",
            "NYK": "new-york-knicks-5",
            "PHI": "philadelphia-76ers-21",
            "IND": "indiana-pacers-30",
            "MIA": "miami-heat-48",
            "ORL": "orlando-magic-50",
            "CHI": "chicago-bulls-25",
            "ATL": "atlanta-hawks-22",
            "BRK": "brooklyn-nets-33",
            "TOR": "toronto-raptors-51",
            "CHA": "charlotte-hornets-53",
            "WAS": "washington-wizards-24",
            "DET": "detroit-pistons-13",
            "MIN": "minnesota-timberwolves-49",
            "OKC": "oklahoma-city-thunder-38",
            "LAC": "la-clippers-41",
            "DEN": "denver-nuggets-28",
            "NOP": "new-orleans-pelicans-47",
            "DAL": "dallas-mavericks-46",
            "SAC": "sacramento-kings-16",
            "PHO": "phoenix-suns-40",
            "LAL": "los-angeles-lakers-15",
            "GSW": "golden-state-warriors-6",
            "UTA": "utah-jazz-45",
            "HOU": "houston-rockets-37",
            "MEM": "memphis-grizzlies-52",
            "POR": "portland-trail-blazers-43",
            "SAS": "san-antonio-spurs-27"
        }
        # Initialize BeautifulSoup for the team's StatMuse page of the specified year
        soup = self.initializeSoup(f"https://www.statmuse.com/nba/team/{nba_codes[self.teamcode]}/{year}")
        # Extract the season averages data
        lst = soup.find_all("tbody", class_="divide-y divide-[#c7c8ca] leading-[22px]")[2].find_all("td", class_="text-right px-2 py-1")
        values = []
        for i in lst[0:20]:
            values.append(i.text.strip())

        # Initialize BeautifulSoup for the team's Basketball Reference page
        soup1 = self.initializeSoup(f"https://www.basketball-reference.com/teams/{self.teamcode}/")
        allas = soup1.find_all("tr")
        lst = []
        seasonLst = []
        for i in allas:
            lst.append(i.find_all("td", attrs={"data-stat":"win_loss_pct"}))
            seasonLst.append(i.find("th", attrs={"data-stat":"season"}).find("a"))
        lst.pop(0)
       

team = TeamScraper("CHI")
print(team.getRoster(1999))