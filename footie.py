import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from flask import Flask, render_template_string



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
                
            #colors = cmap(np.linspace(0, 1, len(Hwins_teams)))
            fig = Figure(figsize=(12, 8))
            ax = fig.subplots()
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Hwins_teams)]
            ax.bar(Hwins_teams,Hwins_values,color=colors)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Home Wins')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Home in wins in the Premier League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            return plot
            #Hwins_teams = list(sorted_hwins.keys())
            #Hwins_values = list(sorted_hwins.values())

            # plt.figure(figsize=(11,7))
            # cmap = plt.get_cmap('plasma')  # You can change 'viridis' to other colormaps like 'plasma', 'inferno', 'magma', etc.
            # colors = cmap(np.linspace(0, 1, len(Hwins_teams)))

            # plt.bar(Hwins_teams,Hwins_values,color=colors)

            # for i in range(len(Hwins_values)):
            #     plt.text(i, Hwins_values[i] + 0.5, str(Hwins_values[i]), ha='center')
            # plt.xticks(fontsize=6)
            # plt.xlabel('Teams')
            # plt.ylabel('Home Wins')
            # plt.tight_layout()
            # plt.show()
        elif result == "away":
            sorted_awins = dict(sorted(away_win.items(), key=lambda item:item[1],reverse=True))
            Awins_teams = []
            Awins_values = []
            for team in range(teams):
                Awins_teams.append(list(sorted_awins.keys())[team])
                Awins_values.append(list(sorted_awins.values())[team])
                

            #Hwins_teams = list(sorted_hwins.keys())
            #Hwins_values = list(sorted_hwins.values())
            fig = Figure(figsize=(12, 8))
            ax = fig.subplots()
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Hwins_teams)]
            ax.bar(Awins_teams,Awins_values,color=colors)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Away Wins')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Away in wins in the Premier League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            return plot


    def the_best(self,best):
        
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
        report += "Welcome to The Model's best performing players list<br>"
        report += '<h2>World Class Stats</h2><br>'
        world_class = best[best['xGI90'] > 1]
        sorted_world_class = world_class.sort_values(by='xGI90', ascending=False)
        report += sorted_world_class.to_html(index=False)
        report += '<br>'
        report += '<h2>Elite Stats</h2><br>'
        elite = best[(best['xGI90'] >= 0.65) & (best['xGI90'] <= 1)]
        sorted_elite = elite.sort_values(by='xGI90', ascending=False)
        report += sorted_elite.to_html(index=False)
        report += '<br>'
        report += '<h2>Good Stats</h2><br>'
        good = best[(best['xGI90'] >= 0.5) & (best['xGI90'] < 0.65)]
        sorted_good = good.sort_values(by='xGI90', ascending=False)
        report += sorted_good.to_html(index=False)
        report += '<br>'
        report += '<h2>Anomalous Stats</h2><br>'
        report += '<br>'
        report += 'Players in this category have achieved stats which are very rare.'
        report += 'This indicates that these players have a special set of skills which allow them to perform in this manner<br>'
        anomaly = best[((best['G'] - best['xG']) >= 2.50) & (best['GI'] > 10)]
        sorted_anomaly = anomaly.sort_values(by='GI', ascending=False)
        report += sorted_anomaly.to_html(index=False)
        report += '<br>'
        report += '<h2>Underperformers Stats</h2><br>'
        underperformer = best[((best['xG'] - best['G']) >= 2.5) & (best['GI'] > 10)]
        sorted_underperformer = underperformer.sort_values(by='GI', ascending=True)
        report += sorted_underperformer.to_html(index=False)

        return report

    def clean_sheets(self,teams,result):
        home_cs = dict()
        away_cs = dict()
        for idx,val in enumerate(self.data['FTAG']):
                home = self.data['HomeTeam'][idx]

                if val == 0:
                    home_cs[home] = home_cs.get(home,0) + 1

        for idx,val in enumerate(self.data['FTHG']):
                away = self.data['AwayTeam'][idx]

                if val == 0:
                    away_cs[away] = away_cs.get(away,0) + 1

        if result == "home":
        
            sorted_hcs = dict(sorted(home_cs.items(), key=lambda item:item[1],reverse=True))
            Hcs_teams = []
            Hcs_values = []
            for team in range(teams):
                Hcs_teams.append(list(sorted_hcs.keys())[team])
                Hcs_values.append(list(sorted_hcs.values())[team])
                
            #colors = cmap(np.linspace(0, 1, len(Hwins_teams)))
            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colours = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Hcs_teams)]
            ax.bar(Hcs_teams,Hcs_values,color=colours)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Home Clean Sheets')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Home clean sheets in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            return plot
            
           
        elif result == "away":        
            
            sorted_acs = dict(sorted(away_cs.items(),key=lambda item:item[1],reverse=True))
            Acs_teams = []
            Acs_values = []
            for team in range(teams):
                Acs_teams.append(list(sorted_acs.keys())[team])
                Acs_values.append(list(sorted_acs.values())[team])

            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colours = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e','#16a085', '#27ae60', '#2980b9', '#8e44ad', '#2c3e50','#f1c40f', '#e67e22', '#e74c3c', '#ecf0f1', '#95a5a6','#f39c12', '#d35400', '#c0392b', '#bdc3c7', '#7f8c8d'][:len(Acs_teams)]
            ax.bar(Acs_teams,Acs_values,color=colours)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Away Clean Sheets')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Away clean sheets in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            return plot


        
app = Flask(__name__)

# Create an instance of the class with the correct relative path
f = footie('PL 24-25 Data 020924.csv')
@app.route('/')
def home():
    report = f.the_best('The Best 020924.csv')
    return render_template_string(report)
    #plot = f.clean_sheets(4,"home")
    #return plot


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


