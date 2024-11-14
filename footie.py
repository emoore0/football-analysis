import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from flask import Flask, render_template_string



class footie:
    data = 0
    
    def __init__(self,file):
        df = pd.read_csv(file)
        self.data = df
        #print(self.data)
        
        if all(col in self.data.columns for col in ['Home', 'Away', 'Res', 'HG', 'AG']):
            self.data.rename(columns={"Home": "HomeTeam", "Away": "AwayTeam", "Res": "FTR", "HG": "FTHG", "AG": "FTAG"}, inplace=True)

    
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
            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Hwins_teams)]
            ax.bar(Hwins_teams,Hwins_values,color=colors)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Home Wins')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Home in wins in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            plot += '<br>'
            return plot
            
        elif result == "away":
            sorted_awins = dict(sorted(away_win.items(), key=lambda item:item[1],reverse=True))
            Awins_teams = []
            Awins_values = []
            for team in range(teams):
                Awins_teams.append(list(sorted_awins.keys())[team])
                Awins_values.append(list(sorted_awins.values())[team])
                

            #Hwins_teams = list(sorted_hwins.keys())
            #Hwins_values = list(sorted_hwins.values())
            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Awins_teams)]
            ax.bar(Awins_teams,Awins_values,color=colors)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Away Wins')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Away in wins in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            plot += '<br>'
            return plot


    def btts(self,teams):
        teamz = dict()

        for idx,val in enumerate(zip(self.data['FTHG'],self.data['FTAG'])):
            home = self.data['HomeTeam'][idx]
            away = self.data['AwayTeam'][idx]
            if val[0] != 0 and val[1] != 0:
                teamz[home] = teamz.get(home,0) + 1
                teamz[away] = teamz.get(away,0) + 1

        sorted_teams = dict(sorted(teamz.items(), key=lambda item:item[1],reverse=True))
        team_who_scored = []
        teams_values = []
        for team in range(teams):
            team_who_scored.append(list(sorted_teams.keys())[team])
            teams_values.append(list(sorted_teams.values())[team])
            

        fig = Figure(figsize=(16, 8))
        ax = fig.subplots()
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(team_who_scored)]
        ax.bar(team_who_scored,teams_values,color=colors)
        ax.set_xlabel('Teams')
        ax.set_ylabel('Matches where both teams scored')
        buf = BytesIO()
        fig.savefig(buf,format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        plot = '<h1>Most BTTS games this season</h1><br>'
        plot += f"<img src='data:image/png;base64,{data}'/>"
        plot += '<br>'
        return plot

    def clean(self,value):
        if '+' in value:
            return value.split('+')[0]
        elif '-' in value:
            return value.split('-')[0]
        return value
    


    def the_best(self,file):
        best = pd.read_csv(file)
        best.drop(best.columns[best.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)


        best['xG'] = best['xG'].apply(self.clean)
        best['xA']=best['xA'].apply(self.clean)

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
        report += '<br>'
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
            plot += '<br>'
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
            plot += '<br>'
            
            return plot
            
    def games(self,team):
        teams = dict()
        hteams = dict()
        ateams = dict()
        for idx,val in enumerate(self.data['HomeTeam']):
            home = self.data['HomeTeam'][idx]
            away = self.data['AwayTeam'][idx]

            if team == "home":
                hteams[home] = hteams.get(home,0) + 1
            

            elif team == "away":
                ateams[away] = ateams.get(away,0) + 1
            
                
            else:
                teams[home] = teams.get(home,0) + 1
                teams[away] = teams.get(away,0) + 1
                
        if team == "home":
            return hteams
        elif team == "away":
            return ateams
        else:
            return teams
            

    def corners(self,teams,result):
        team_list = self.games("home")
        home_corners = dict()
        away_corners = dict()
        for idx,val in enumerate(self.data['HC']):
            home = self.data['HomeTeam'][idx]
            
            home_corners[home] =  home_corners.get(home,0)
            home_corners[home] = home_corners[home] + self.data['HC'][idx]
            home_corners[home] = home_corners[home]/team_list[home]

        for idx,val in enumerate(self.data['AC']):
            away = self.data['AwayTeam'][idx]

            away_corners[away] =  away_corners.get(away,0)
            away_corners[away] = away_corners[away] + self.data['AC'][idx]
            away_corners[away] = away_corners[away]/team_list[away]


        if result == "home":
            
            sorted_hcorners = dict(sorted(home_corners.items(), key=lambda item:item[1],reverse=True))
            Hcorners_teams = []
            Hcorners_values = []
            for team in range(teams):
                Hcorners_teams.append(list(sorted_hcorners.keys())[team])
                Hcorners_values.append(list(sorted_hcorners.values())[team])
                
            #colors = cmap(np.linspace(0, 1, len(Hwins_teams)))
            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colours = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Hcorners_teams)]
            ax.bar(Hcorners_teams,Hcorners_values,color=colours)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Home Corners')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Home Corners  in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            plot += '<br>'
            return plot
            
        if result == "away":

            sorted_acorners = dict(sorted(away_corners.items(), key=lambda item:item[1],reverse=True))
            Acorners_teams = []
            Acorners_values = []
            for team in range(teams):
                Acorners_teams.append(list(sorted_acorners.keys())[team])
                Acorners_values.append(list(sorted_acorners.values())[team])
                
            #colors = cmap(np.linspace(0, 1, len(Hwins_teams)))
            fig = Figure(figsize=(16, 8))
            ax = fig.subplots()
            colours = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f','#9b59b6', '#34495e', '#16a085', '#e67e22','#95a5a6', '#d35400', '#c0392b', '#7f8c8d','#2c3e50', '#27ae60', '#8e44ad', '#1abc9c','#f39c12', '#bdc3c7', '#2980b9', '#e84393'][:len(Acorners_teams)]
            ax.bar(Acorners_teams,Acorners_values,color=colours)
            ax.set_xlabel('Teams')
            ax.set_ylabel('Away Corners')
            buf = BytesIO()
            fig.savefig(buf,format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plot = '<h1>Most Away Corners in the League</h1><br>'
            plot += f"<img src='data:image/png;base64,{data}'/>"
            plot += '<br>'
            return plot   
        


        
app = Flask(__name__)

# Create an instance of the class with the correct relative path
a = footie('./data/ARG.csv')
b = footie('./data/BRA.csv')
c = footie('./data/DNK.csv')
d = footie('./data/FRA.csv')
e = footie('./data/SPA.csv')
f = footie('./data/ITA.csv')
g = footie('./data/GRE.csv')
h = footie('./data/GER.csv')
i = footie('./data/POR.csv')
j = footie('./data/Championship.csv')
k = footie('./data/BRA.csv')
l = footie('./data/NET.csv')
n = footie('./data/SCO.csv')
o = footie('./data/ENG.csv')
p = footie('./data/IRL.csv')
q = footie('./data/SWE.csv')
r = footie('./data/SWZ.csv')

@app.route('/')
def home():
    plot = '<h1>Argentina</h1><br>'
    plot += a.btts(5)
    
    plot += '<h1>Brazil</h1><br>'
    plot += b.btts(5)

    plot += '<h1>Denmark</h1><br>'
    plot += c.btts(5)

    plot += '<h1>France</h1><br>'
    plot += d.btts(5)

    
    #return render_template_string(report)
    plot += '<h1>Spain</h1><br>'
    # plot += e.outcomes(7,"home")
    plot += e.btts(5)
     
   
    # plot += e.outcomes(7,"away")
     
    
    # plot += e.clean_sheets(5,"home")
     
 
    # plot += e.clean_sheets(5,"away")
     
  
    plot += '<h1>Italy</h1><br>'
    plot += f.btts(5)
    # plot += f.outcomes(7,"home")
     

    # plot += f.outcomes(7,"away")
     

    # plot += f.clean_sheets(5,"home")
     

    # plot += f.clean_sheets(5,"away")
     

    plot += '<h1>Greece</h1><br>'
    # plot += g.outcomes(7,"home")
    plot += g.btts(5) 

    # plot += g.outcomes(7,"away")
     

    # plot += g.clean_sheets(5,"home")
    

    # plot += g.clean_sheets(5,"away")
    

    plot += '<h1>Germany</h1><br>'
    # plot += h.outcomes(7,"home")
    plot += h.btts(5)
    

    # plot += h.outcomes(7,"away")
 

    # plot += h.clean_sheets(5,"home")
    
    
    # plot += h.clean_sheets(5,"away")
   

    plot += '<h1>Portugal</h1><br>'
    # plot += i.outcomes(7,"home")
    plot += i.btts(5)
    

    # plot += i.outcomes(7,"away")
 

    # plot += i.clean_sheets(5,"home")
 

    # plot += i.clean_sheets(5,"away")
    
 
    
    plot += '<h1>Netherlands</h1><br>'
    # plot += l.outcomes(7,"home")
    plot += l.btts(5)

   
    # plot += l.outcomes(7,"away")
    
    
    # plot += l.clean_sheets(5,"home")


    
    # plot += l.clean_sheets(5,"away")
   
    
    
    plot += '<h1>Scotland</h1><br>'
    # plot += n.outcomes(7,"home")
    plot += n.btts(5)
  
  
    # plot += n.outcomes(7,"away")

    
    # plot += n.clean_sheets(5,"home")
 
    
    # plot += n.clean_sheets(5,"away")
    
  
    
    plot += '<h1>Sweeden</h1><br>'
    # plot += q.outcomes(7,"home")
    plot += q.btts(5)
    
    # plot += q.outcomes(7,"away")

    
    # plot += q.clean_sheets(5,"home")

   
    # plot += q.clean_sheets(5,"away")
   
    
    plot += '<h1>Championship</h1><br>'
    # plot += j.outcomes(7,"home")
    plot += j.btts(5)
 
    
    # plot += j.outcomes(7,"away")
  
    
    # plot += j.clean_sheets(5,"home")
  
    
    # plot += j.clean_sheets(5,"away")
    plot += '<h1>Ireland</h1><br>'
    plot += p.btts(5)
    
    plot += '<h1>Switzerland</h1><br>'
    plot += r.btts(5)

    plot += '<h1>England</h1><br>'

    # plot += o.outcomes(7,"home")
   
   
    # plot += o.outcomes(7,"away")
   
    
    # plot += o.clean_sheets(5,"home")
    

    plot += o.clean_sheets(5,"away")
    
    # plot += o.corners(7,"home")
    
    # plot += o.btts(5)
    
    # plot += o.the_best('./the-best.csv')
    

    return render_template_string(plot)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
