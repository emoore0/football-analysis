import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



class footie:
    data = 0
    teams = []
    
    
 
    def __init__(self,file):
        df = pd.read_csv(file)
        self.data = df
        #print(self.data)

        for i in df['HomeTeam']:
            if i in self.teams:
                continue

            else:
                self.teams.append(i)
        #return self.teams
    
    def outcomes(self,teams,result):
        home_win = dict()
        away_win = dict()
        draw = dict()
        for  idx,val in enumerate(self.data['FTR']):
            home = self.data['HomeTeam'][idx]
            away = self.data['AwayTeam'][idx]

            if val == 'H':
                home_win[home] = home_win.get(home,0) + 1
            if val == 'A':
                away_win[away] = away_win.get(away,0) + 1
            if val == 'D':
                draw[home] = draw.get(home,0) + 1
                draw[away] = draw.get(away,0) + 1

            #return draw
        if result == "home":
            sorted_hwins = dict(sorted(home_win.items(), key=lambda item:item[1],reverse=True))
            Hwins_teams = []
            Hwins_values = []
            for team in range(teams):
                Hwins_teams.append(list(sorted_hwins.keys())[team])
                Hwins_values.append(list(sorted_hwins.values())[team])
                

            #Hwins_teams = list(sorted_hwins.keys())
            #Hwins_values = list(sorted_hwins.values())

            plt.figure(figsize=(11,7))
            cmap = plt.get_cmap('plasma')  # You can change 'viridis' to other colormaps like 'plasma', 'inferno', 'magma', etc.
            colors = cmap(np.linspace(0, 1, len(Hwins_teams)))

            plt.bar(Hwins_teams,Hwins_values,color=colors)

            for i in range(len(Hwins_values)):
                plt.text(i, Hwins_values[i] + 0.5, str(Hwins_values[i]), ha='center')
            plt.xticks(fontsize=6)
            plt.xlabel('Teams')
            plt.ylabel('Home Wins')
            plt.tight_layout()
            plt.show()
        elif result == "away":
            sorted_awins = dict(sorted(away_win.items(), key=lambda item:item[1],reverse=True))
            Awins_teams = []
            Awins_values = []
            for team in range(teams):
                Awins_teams.append(list(sorted_awins.keys())[team])
                Awins_values.append(list(sorted_awins.values())[team])
                

            #Hwins_teams = list(sorted_hwins.keys())
            #Hwins_values = list(sorted_hwins.values())

            plt.figure(figsize=(11,7))
            cmap = plt.get_cmap('magma')  # You can change 'viridis' to other colormaps like 'plasma', 'inferno', 'magma', etc.
            colors = cmap(np.linspace(0, 1, len(Awins_teams)))

            plt.bar(Awins_teams,Awins_values,color=colors)

            for i in range(len(Awins_values)):
                plt.text(i, Awins_values[i] + 0.5, str(Awins_values[i]), ha='center')
            plt.xticks(fontsize=6)
            plt.xlabel('Teams')
            plt.ylabel('Away Wins')
            plt.tight_layout()
            plt.show()

    def the_best(self):
        best = pd.read_csv('The Best.csv')
        #return best['xG']

        def clean(value):
            if '+' in value:
                return value.split('+')[0]
            elif '-' in value:
                return value.split('-')[0]
            return value
        best['xG'] = best['xG'].apply(clean)
        best['xA']=best['xA'].apply(clean)
        best['xGI90'] = best['xA90'] + best['xG90']
        best['GI'] = best['A'] + best['G']
        best['G'] = pd.to_numeric(best['G'])
        best['xG'] = pd.to_numeric(best['xG'])
        
        report = ''
        report += "Welcome to The Model's best perfoming players list"
        report += '\n'
        report += 'World Class Stats\n'
        report += '\n'
        world_class = best[best['xGI90'] >1]
        sorted_world_class = world_class.sort_values(by='xGI90',ascending=False)
        report += sorted_world_class.to_string()
        report += '\n'
        report += '\n'
        report += 'Elite Stats\n'
        report += '\n'
        elite = best[(best['xGI90'] >= 0.65) & (best['xGI90'] <= 1)] 
        sorted_elite = elite.sort_values(by='xGI90', ascending=False)
        report += sorted_elite.to_string()
        report += '\n'
        report += '\n'
        report += 'Good Stats\n'
        report += '\n'
        good = best[(best['xGI90'] >= 0.5) & (best['xGI90'] < 0.65)] 
        sorted_good = good.sort_values(by='xGI90', ascending=False)
        report += sorted_good.to_string()
        report += '\n'
        report += '\n'
        report += 'Anamolous Stats\n'
        report +='\n'
        anamoly = best[((best['G'] - best['xG']) >= 2.50) & (best['GI'] > 10)]
        sorted_anamoly = anamoly.sort_values(by='GI',ascending=False)
        report += sorted_anamoly.to_string()
        report += '\n'
        report += '\n'
        report += 'Underperformers Stats\n'
        report +='\n'
        underpeformer = best[((best['xG'] - best['G']) >= 2.5) & (best['GI'] > 10)]
        sorted_underperfomer= underpeformer.sort_values(by='GI',ascending=True)
        report += sorted_underperfomer.to_string()
        


        
        

        return report
        
        




f = footie('PL 23-24 Data.csv')
#print(f.teams)
#f.outcomes(7,"home")
print(f.the_best()) 
#anything above 0.6 xG90 + xA90 is great! get this data from understat 
