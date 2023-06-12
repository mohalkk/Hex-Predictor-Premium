import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    f = open("auth.txt", "r")
    auth_token = f.read()
   #auth_token = "your token" 
    
    while True:
        num_spots = int(input("Spots: "))
        num_history_games = int(input("History: "))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'X-Auth-Token': auth_token
        }

        response = requests.get('https://rest-bf.blox.land/games/mines/history', headers=headers, params={'size': num_history_games, 'page': 0})

        if response.status_code == 200:
            game_data = response.json()['data']

            cell_counts = [0] * 25
            for game in game_data:
                mines = game['mineLocations']
                for mine in mines:
                    cell_counts[mine] += 1

            top_spots = sorted(range(len(cell_counts)), key=lambda i: cell_counts[i], reverse=True)[:num_spots]

            prediction = [['X' for _ in range(5)] for _ in range(5)]
            for i in top_spots:
                prediction[i//5][i%5] = 'O'

            print("Prediction:")
            for row in prediction:
                print_row = ''
                for cell in row:
                    if cell == 'X':
                        print_row += Fore.LIGHTRED_EX + cell + Style.RESET_ALL + ' '
                    else:
                        print_row += Fore.LIGHTCYAN_EX + cell + Style.RESET_ALL + ' '
                print(print_row)
            print("━━━━━━━━━")
        else:
            print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    main()
