import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt

df1 = pd.read_csv("IPL Matches 2008-2020.csv")
df2 = pd.read_csv('IPL Ball-by-Ball 2008-2020.csv')



def clean_data():
    
    df1.team1.replace("Rising Pune Supergiants", "Rising Pune Supergiant",inplace = True)
    df1.team2.replace("Rising Pune Supergiants", "Rising Pune Supergiant",inplace = True)
    df1.toss_winner.replace("Rising Pune Supergiants", "Rising Pune Supergiant",inplace = True)
    df1.winner.replace("Rising Pune Supergiants", "Rising Pune Supergiant",inplace = True)
    df1['date'] = pd.to_datetime(df1.date,infer_datetime_format=True)
    df1['season'] = df1.date.dt.year
    
    return df1,df2


def matches_over_years(df):
    temp_df  = df.season.value_counts().sort_index()
    fig = px.line(x = temp_df.index , y = temp_df.values,markers=  True, labels=dict(x = 'Years', y = 'Matches'))
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    return fig

def team_over_years(df):
    temp_df = df.groupby('season')['team1'].nunique()
    fig = px.bar(x = temp_df.index , y = temp_df.values, labels=dict(x = 'Years', y = 'Teams'),text_auto=True)
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )

def score_over_seasons(df1,df2):
    temp_df = df1[['id','season']].merge(df2,on = 'id', how = 'left')
    temp_df = temp_df.groupby('season')['total_runs'].sum()
    fig = px.bar(x = temp_df.index, y = temp_df.values,labels=dict(x = 'season', y = 'Score'),text_auto=True)
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )

def selected_year(df,year):
    temp_df = df[df.season == year].team1.append(df[df.season==year].team2).reset_index()
    temp_df.drop(['index'] , axis = 1, inplace = True
                )
    temp_df.rename(columns = {0:'team'},inplace = True)

    matches_of_team_for_specific_year = temp_df.team.value_counts()
    return matches_of_team_for_specific_year

def toss_winners(df,year):
    matches_per_team = (df.team2.value_counts() + df.team1.value_counts()).sort_values(ascending=False)
    if year == 'Overall':
      temp_df = round(((df.toss_winner.value_counts() / matches_per_team) * 100).sort_values(ascending = True),2)
    elif year != "Overall":
      temp_df = round(((df[df.season == year].toss_winner.value_counts() / selected_year(df,year))*100).sort_values(ascending = True),2)
      
    fig = px.bar(x = temp_df.values, y = temp_df.index, labels=dict(x = "Toss winning %",y = "Team"),text_auto = True)

    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )

def win_percentage(df,year):
    if year == "Overall":
      matches_per_team = (df.team2.value_counts() + df.team1.value_counts()).sort_values(ascending=False)
      team_wins = df.winner.value_counts()
      matches_per_team = matches_per_team.sort_index()
      team_wins = team_wins.sort_index()
      winning_percentage = round(team_wins / matches_per_team * 100,2)
      winning_percentage = winning_percentage.sort_values(ascending=True)
    elif year != 'Overall':
        matches_per_team = (df[df.season == year].team2.value_counts() + df[df.season == year].team1.value_counts()).sort_values(ascending=True)
        team_wins = df[df.season == year].winner.value_counts()
        matches_per_team = matches_per_team.sort_index()
        team_wins = team_wins.sort_index()
        winning_percentage = round(team_wins / selected_year(df1,year) * 100,2)
        winning_percentage = winning_percentage.sort_values(ascending=True)
    fig = px.bar(x = winning_percentage.values, y = winning_percentage.index, labels=dict(x = "Match Winning %",y = "Teams"),text_auto = True)

    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )


def top_bats(df1,df2,year):
    
    season_data = df1[['id','season']].merge(df2, left_on='id', right_on='id', how = 'left').drop(columns='id',axis = 1)
    if year == 'Overall':
        temp_df = season_data.groupby('batsman')['batsman_runs'].sum().sort_values(ascending = False).head(10)
    elif year != "Overall":
        temp_df = season_data[season_data.season == year].groupby('batsman')['batsman_runs'].sum().sort_values(ascending = False).head(10)
    return temp_df


def top_bowls(df1,df2,year):
    season_data = df1[['id','season']].merge(df2, left_on='id', right_on='id', how = 'left').drop(columns='id',axis = 1)
    temp_df = season_data[(season_data.dismissal_kind == 'caught') | (season_data.dismissal_kind == 'bowled') | (season_data.dismissal_kind == 'lbw') | (season_data.dismissal_kind == 'stumped') | (season_data.dismissal_kind == 'hit wicket') | (season_data.dismissal_kind.isnull() == True)]
    if year == 'Overall':
        temp_df = temp_df.groupby("bowler")['is_wicket'].sum().sort_values(ascending = False).head(10)
    elif year != 'Overall':
        temp_df = temp_df[temp_df.season == year].groupby("bowler")['is_wicket'].sum().sort_values(ascending = False).head(10)
        
    fig = px.bar(x = temp_df.index, y = temp_df.values,labels=dict(x = 'Top 10 Bowler', y = 'Wickets taken'),text_auto = True)
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )


def highest_innings_score(df1,df2):
    season_data = df1[['id','season']].merge(df2, left_on='id', right_on='id')
    high_scores =season_data.groupby(['id','batting_team','season'])['total_runs'].sum().reset_index().sort_values(by = 'total_runs',ascending = False).head(10)[['batting_team','total_runs','season']].sort_values(by = 'total_runs',ascending=True)
    fig = px.imshow(high_scores.pivot_table(index = 'season', columns='batting_team',values='total_runs'),text_auto = True,labels = dict(color = 'Score'), width = 700)
    fig.update_coloraxes(showscale=False)

    return fig

def most_player_of_matches(df, year):
    if year == 'Overall':
        temp_df = df.player_of_match.value_counts().head(5)
    if year != 'Overall':
        temp_df = df[df.season == year].player_of_match.value_counts().head(5)
        
    fig = go.Figure(data = go.Pie(labels = temp_df.index, values = temp_df.values,pull=[0, 0, 0,0, 0] ))
    fig.update_traces(hoverinfo='percent', textinfo='value+label', textfont_size=10,
                  marker=dict(colors =  ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
, line=dict(color='#000000', width=2
            )))
    
    return fig
        

def total_runs(df, batsman):
    temp_df = df[df.batsman == batsman].batsman_runs.sum()
    return temp_df

def fours(df, batsman):
    temp_df = df[(df.batsman == batsman) & (df.batsman_runs == 4)].shape[0]
    return temp_df


def sixes(df, batsman):
    temp_df = df[(df.batsman == batsman) & (df.batsman_runs == 6)].shape[0]
    return temp_df

def matches_of_player(df,player):
    temp_df = df[df.batsman == player].id.nunique()
    return temp_df

def average_of_player(df,player):
    dismissal = df[(df.batsman == player) & (df.player_dismissed.isnull() == False)].player_dismissed.count()
    score = df[df.batsman == player].batsman_runs.sum()
    temp_df = score / dismissal
    return temp_df

def strike_rate(df,player):
  return (df[(df.batsman == player)].batsman_runs.sum() / df[(df.batsman == player) & (df.extras_type != 'wides')].ball.count()) * 100

def high_score(df,player):
    return df[df.batsman == player].groupby('id')['batsman_runs'].sum().max()    

def runs_classification(df,batsman):
  temp_df=  df[(df.batsman == batsman)  & (df.batsman_runs != 0)].batsman_runs.value_counts().sort_index()
  fig = go.Figure(data = go.Pie(labels = temp_df.index, values = temp_df.values))
  fig.update_traces(hoverinfo='percent+label', textinfo='value', textfont_size=10,
                  marker=dict(colors =  ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
                , line=dict(color='#000000', width=2)))
  fig.update_layout(
    title="Runs Classification",
    legend_title="Categories",
    font=dict(
    size = 13)
  )
  
  return fig

def str_rate_through_over(df,player):
    runs = df[df.batsman == player].groupby('over')['batsman_runs'].sum()
    balls = df[(df.batsman == player) & (df.extras_type != 'wides')].groupby('over').ball.count()
    str_rate = round((runs / balls) * 100,1) 
    fig = px.bar(data_frame= str_rate, x= str_rate.index, y = str_rate.values, text_auto=True, labels= dict(y = 'Strike Rate'))
    fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )
    return fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1 
    )
)
    
def scores(df,player):
    temp_df = df[df.batsman == player].groupby('id')['batsman_runs'].sum().reset_index()
    temp_df['scores'] = temp_df['batsman_runs'].apply(lambda x: ('30+' if (50 > x >= 30) else('50+' if (100 > x >= 50) else ('100+' if (x >= 100) else 0))))
    temp_df = temp_df[(temp_df.scores == '30+') | (temp_df.scores == '50+') | (temp_df.scores == '100+')]
    temp_df = temp_df.scores.value_counts()
    fig = go.Figure(data = go.Pie(labels = temp_df.index , values = temp_df.values))
    fig.update_traces(hoverinfo='percent', textinfo='label+value', textfont_size=10,
                  marker=dict(colors =  ['gold', 'mediumturquoise', 'darkorange']
                , line=dict(color='#000000', width=2)))

    fig.update_layout(
    title="30s - 50s - 100s runs",
    font=dict(
    size = 13)
    )
    return fig


def bowler_matches(df,bowler):
    return df[df.bowler == bowler].id.nunique() 

def overs_delivered(df,bowler):
    temp_df = df[(df.extras_type != 'wides') & (df.extras_type != 'noballs') & (df.extras_type != 'penalty')]
    return (temp_df[temp_df.bowler == bowler].ball.count()) / 6

def dismissals(df,batsman):
  temp_df = df[df.batsman == batsman].dismissal_kind.value_counts()
  fig = go.Figure(data = go.Pie(labels=temp_df.index, values=temp_df.values))
  fig.update_traces(hoverinfo='percent', textinfo='label+value', textfont_size=10,
                  marker=dict(colors =  ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
                , line=dict(color='#000000', width=2)), name = 'Wickets')

  fig.update_layout(
    title="Dismissals",
    legend_title="Categories",
    font=dict(
    size = 13)
  )
  return fig


def wickets(df,batsman):
  temp_df = df[(df.dismissal_kind == 'caught') | (df.dismissal_kind == 'bowled') | (df.dismissal_kind == 'lbw') | (df.dismissal_kind == 'stumped') | (df.dismissal_kind == 'hit wicket') | (df.dismissal_kind.isnull() == True)]
  return temp_df[temp_df.bowler == batsman].is_wicket.sum()


def average_of_bowler(df,bowler):
  return round(df[(df.bowler == bowler)  & (df.extras_type != 'byes') & (df.extras_type != 'legbyes')].total_runs.sum() / df[(df.bowler == bowler) | (df.batsman == bowler)].id.nunique(),1)

def economy(df,bowler):
  return (df[(df.bowler == bowler) & (df.extras_type != 'byes') & (df.extras_type != 'legbyes')].total_runs.sum() / df[(df.bowler == bowler) & (df.extras_type != 'wides') & (df.extras_type != 'noballs') & (df.extras_type != 'penalty')].ball.count()) * 6

def best_figures(df,player):
  temp_df = df[df.bowler == player].groupby('id')[['is_wicket','total_runs']].sum()
  n = temp_df.is_wicket.max()
  runs = temp_df[temp_df.is_wicket == n].total_runs.min()
  return (f"{runs}-{n}")


def wickets_haul(df,player):

  temp = df[(df.dismissal_kind == 'caught') | (df.dismissal_kind == 'bowled') | (df.dismissal_kind == 'lbw') | (df.dismissal_kind == 'stumped') | (df.dismissal_kind == 'hit wicket') & (df.dismissal_kind.isnull() == False)]
  temp = temp[temp.bowler == player].groupby('id')['is_wicket'].sum().reset_index()
  temp = temp[(temp.is_wicket == 3)|(temp.is_wicket == 4) | (temp.is_wicket == 5) | (temp.is_wicket == 6)]
  n = temp.is_wicket
  l = []
  for a in n:
     a = str(a) + 's'
     l.append(a) 
  temp['is_wicket'] = l
  temp = temp.value_counts().reset_index().rename({"count":'times'},axis = 1)
  return temp
  """fig = go.Figure(data = go.Pie(labels = temp.is_wicket , values = temp.times))
  fig.update_traces(hoverinfo='percent', textinfo='label+value', textfont_size=15,
                  marker=dict(colors =  ['mediumturquoise', 'darkorange']
                , line=dict(color='#000000', width=2)))

  fig.update_layout(
    title="3 - 4 - 5 -6 wickets-haul",
    font=dict(
    size = 13)
    )
  return fig"""

def season_wins(df,team):
    temp_df = df.drop_duplicates(subset = ['season'],keep = 'last')
    return f"{temp_df[temp_df.winner == team].shape[0]} times"

def runner_up_times(df,team):
    list1 = []
    temp = df.drop_duplicates(subset = ["season"],keep = 'last')
    for a,b,c in zip(temp['team1'],temp['team2'],temp['winner']):
        if a == c:
            list1.append(b)
        else:
            list1.append(a)
    temp['runner_ups'] = list1
    temp = temp[temp.runner_ups == team].shape[0]
    return f"{temp} times"

def highest_totals_defending(df,team,inning):
    temp = df[(df.batting_team == team) & (df.inning == inning)]
    temp = temp.groupby(['id','season','bowling_team']).total_runs.sum().reset_index().sort_values(by = 'total_runs' ,ascending = False).head(10)
    fig = px.bar(x = temp['season'], y = temp['total_runs'],height=500,color = temp['bowling_team'],text_auto=True,title = 'Top 10 Highest Totals in 1st Innings', labels = dict(x = 'Season', y = 'Innings Total', color = 'Bowling Team'))
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )
    
def highest_totals_chasing(df,team,inning):
    temp = df[(df.batting_team == team) & (df.inning == inning)]
    temp = temp.groupby(['id','season','bowling_team']).total_runs.sum().sort_values(ascending = False).reset_index().head(10)
    fig = px.bar(x = temp['season'], y = temp['total_runs'],height=500,color = temp['bowling_team'],text_auto=True,title = 'Top 10 highest totals of 2nd Innings', labels = dict(x = 'Season', y = 'Innings Total', color = 'Bowling Team'))
    fig.update_layout(xaxis = dict(
        tickmode = 'linear'
    ))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2)))
    
    
def toss_percentage(df,team,year):
    if year == 'Overall':
        matches_per_team = (df[df.team2 == team].groupby('season')['team2'].count() + df[df.team1 == team].groupby('season')['team2'].count()).sort_values(ascending=False)
        temp_df = ((df[df.toss_winner == team].groupby('season').toss_winner.count() / matches_per_team) * 100)
        fig = px.bar(x = temp_df.index, y = temp_df.values, labels=dict(x = "Season",y = "Toss Winning percentage %"))
    elif year != 'Overall':
        matches_per_team = (df[(df.season == year) & (df.team2 == team)].groupby('season')['team2'].count() + df[(df.season == year) & (df.team1 == team)].groupby('season')['team2'].count())
        temp_df = ((df[(df.season == year) & (df.toss_winner == team)].toss_winner.count() / matches_per_team) * 100)
        fig = px.bar(x = temp_df.index, y = temp_df.values, labels=dict(x = "Season",y = "Toss Winning percentage %"))
    fig.update_traces(
    marker=dict(line=dict(color='#000000', width=2)))
    
    return fig


def win_percentage_of_team(df,year,team):
    if year == "Overall":
      matches_per_team = (df[df.team2 == team].groupby('season').team2.count() + df[df.team1 == team].groupby('season').team1.count()).sort_values(ascending=False)
      team_wins = df[df.winner == team].groupby('season').winner.count()
      matches_per_team = matches_per_team.sort_index()
      team_wins = team_wins.sort_index()
      winning_percentage = team_wins / matches_per_team * 100
      winning_percentage = round(winning_percentage.sort_values(ascending=True),1)
      fig = px.bar(x = winning_percentage.index, y = winning_percentage.values, labels=dict(x = "Season",y = "Match Winning %"),text_auto=True)
    elif year != 'Overall':
        matches_per_team = (df[(df.season == year) & (df.team2 == team)].groupby('season').team2.count() + df[(df.season == year) & (df.team1 == team)].groupby('season').team1.count()).sort_values(ascending=True)
        team_wins = df[(df.season == year) * (df.winner == team)].groupby('season').winner.count()
        matches_per_team = matches_per_team.sort_index()
        team_wins = team_wins.sort_index()
        winning_percentage = team_wins / matches_per_team * 100
        winning_percentage = round(winning_percentage.sort_values(ascending=True),1)
        fig = px.bar(x = winning_percentage.index, y = winning_percentage.values, labels=dict(x = "Season",y = "Match Winning %"),text_auto=True)
        fig.update_layout(xaxis = dict(
        tickmode = 'array',
        tickvals = [year]))
    return fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2)))
    
def top_batsmen(df,team,year):
    if year == 'Overall':
        temp_df = df[df.batting_team == team]
    elif year != "Overall":
        temp_df = df[(df.batting_team == team) & (df.season == year)]
    
    temp_df = temp_df.groupby(['batsman'])['batsman_runs'].sum().sort_values(ascending = False).head(5)
    fig = px.bar(x = temp_df.index , y = temp_df.values , text_auto=True, labels = dict(x = 'Batsman', y = 'Runs Scored'))
    fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2)))
    return fig

def top_bowlers(df,team,year):
    if year == 'Overall':
        temp_df = df[df.bowling_team == team]
    elif year != "Overall":
        temp_df = df[(df.bowling_team == team) & (df.season == year)]
    
    temp_df = temp_df[(temp_df.dismissal_kind != 'run out')  & (temp_df.dismissal_kind != 'obstructing the field')].groupby(['bowler'])['is_wicket'].sum().sort_values(ascending = False).head(5)
    fig = px.bar(x = temp_df.index , y = temp_df.values , text_auto=True, labels = dict(x = 'Bowlers', y = 'Wickets taken'))
    fig.update_traces(
                  marker=dict(line=dict(color='#000000', width=2)))
    return fig

