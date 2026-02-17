import requests
import sys
import os

class Cartola:
    def __init__(self):
        self.url = "https://v3.football.api-sports.io/"
        self.headers = {
            "X-RapidAPI-Key": os.getenv("FUTEBOL_API_KEY")
        }
        self.data = None
        self.response = None
      
    def make_call(self, additional, query):
        """
        Send GET request to the API and return JSON response.
        Returns None if request fails.
        """
        self.response = requests.get(
            url=self.url + additional,
            headers=self.headers,
            params=query
        )

        if self.response.status_code == 200:
            self.data = self.response.json()
        else:
            print("Erro:", self.response.status_code)
            print(self.response.text)
            self.data = None
    
    def search_team(self, name):
        """
        Search for teams by name using the API-Football service.
        Prints team name, id and country.
        """
        self.make_call("teams", {"search":name})

        if self.response.status_code == 200:
            for team in self.data["response"]:
                print("Nome:", team["team"]["name"])
                print("ID:", team["team"]["id"])
                print("País:", team["team"]["country"])
                print("-" * 20)
        else:
            print(self.response.text)

    def view_games(self, team_a, team_b):
        """
        Calculate win/draw probabilities based on
        the last 20 finished head-to-head matches.
        """
        h2h = f"{team_a}-{team_b}"
        self.make_call("fixtures/headtohead", {'h2h' : h2h})
        
        wins_team_a = 0 
        wins_team_b = 0 
        draws = 0
        
        if self.response.status_code == 200:
            matches = self.data["response"]

            finished_matches = [
                match for match in matches
                if match["fixture"]["status"]["short"] == "FT"
            ]

            sorted_finished_matches = sorted(
                finished_matches,
                key=lambda x: x["fixture"]["date"],
                reverse=True
            )

            last_twenty = sorted_finished_matches[:20]

            if len(last_twenty) == 0:
                print("Not enough matches.")
                return

            team_a_name = None
            team_b_name = None
            team_a = int(team_a)

            for match in last_twenty:
                home_id = match["teams"]["home"]["id"]
                home_name = match["teams"]["home"]["name"]
                away_name = match["teams"]["away"]["name"]

                if home_id == team_a:
                    team_a_name = home_name
                    team_b_name = away_name
                    goals_a = match["goals"]["home"]
                    goals_b = match["goals"]["away"]
                else:
                    team_a_name = away_name
                    team_b_name = home_name
                    goals_a = match["goals"]["away"]
                    goals_b = match["goals"]["home"]

                if goals_a > goals_b:
                    wins_team_a += 1
                elif goals_a < goals_b:
                    wins_team_b += 1
                else:
                    draws += 1

            total_matches = len(last_twenty)

            print("\nProbability (based on last 20 matches):")
            print(f"{team_a_name}: {(wins_team_a/total_matches)*100:.1f}%")
            print(f"Draw: {(draws/total_matches)*100:.1f}%")
            print(f"{team_b_name}: {(wins_team_b/total_matches)*100:.1f}%")
        else:
            print(self.response.text)


if __name__ == "__main__":
    cartola = Cartola()
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("python main.py search <team_name>")
        print("python main.py view <team_id_a> <team_id_b>")
        sys.exit(1)

    if sys.argv[1] == 'search':
        cartola.search_team(sys.argv[2])
    elif sys.argv[1] == 'view':
        cartola.view_games(sys.argv[2], sys.argv[3])
        