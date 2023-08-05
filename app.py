# streamlit app for IPL analysis

import streamlit as st
import pandas as pd
import plotly.express as px
import helper

st.sidebar.image("image.png",width = 230)
st.sidebar.title('IPL analysis 2008-2020')
user_menu = st.sidebar.radio("select an option",('Season Summary',"Overall Analysis",
                                     'Team wise analysis', 'Player wise analysis'))

df1,df2 = helper.clean_data()

season_data = df1[['id','season']].merge(df2,on = 'id')
finals = df1.drop_duplicates(subset = ['season'],keep = 'last')


if user_menu == 'Season Summary':
    
    st.markdown("<h1 style='text-align: center; font-family:georgia,garamond,serif;font-size:40px;'>Season Summary</h1>", unsafe_allow_html=True)
    
    match_per_season = df1.season.value_counts().reset_index().rename(columns={'index':'season','season':
                                                                           'matches'})
    matches_per_season = match_per_season.sort_values(by = 'season')
    season_score = season_data.groupby('season')['total_runs'].sum().reset_index()

    runs_per_season = pd.concat([match_per_season, season_score.iloc[:,1]], axis = 1)

    season_summary = runs_per_season.merge(finals,on = 'season').rename({"team1":'finalist 1','team2':'finalist 2'},axis =1)
    
    temp_df= season_data.groupby(['batsman','season'])['batsman_runs'].sum().reset_index()
    temp_df = temp_df.groupby(['season','batsman'])['batsman_runs'].max().sort_values(ascending=False).reset_index().drop_duplicates(subset = 'season', keep = 'first')
    
    def runner_ups(season_summary,col1,col2,col3):
        list1 = []
        for a,b,c in zip(season_summary[col1],season_summary[col2], season_summary[col3]):
            if a == b:
                list1.append(c)
            else:
                list1.append(a)
        return list1 
    
    season_summary['runner up'] = runner_ups(season_summary,'finalist 1','winner','finalist 2')   
    player_of_seasons = ['Shane Watson','Adam Gilchrist','Sachin Tendulkar','Chris Gayle','Sunil Narine','Shane Watson',"Glenn Maxwell",'Andre Russell','Virat Kohli','Ben Stokes','Sunil Narine','Andre Russell','Jofra Archer']
    season_summary['player of the season'] = player_of_seasons
    
    st.table(season_summary[['season','matches','total_runs','finalist 1','finalist 2','winner','runner up','player of the season']])


elif user_menu == 'Overall Analysis':
    st.markdown("<h1 style='text-align: center; font-family:georgia,garamond,serif;font-size:40px;'>Overall Analysis</h1>", unsafe_allow_html=True)
    matches = df1.shape[0]
    host_cities = df1.venue.nunique()
    players = pd.concat([df2.bowler, df2.batsman],axis = 0).nunique()
    seasons = df1.season.nunique()
    teams = df1.team1.nunique()
    
    col1,col2,col3 = st.columns(3)
    
        
    with col2:
        st.subheader('Host Cities')
        st.title(host_cities)
        
    with col3:
        st.subheader('players')
        st.title(players)
        
    with col1:
        st.subheader('Seasons')
        st.title(seasons)
        
    col4,col5 = st.columns(2) 
     
    with col4:
        st.subheader('Matches')
        st.title(matches)
        
    with col5:
        st.subheader('Teams played')
        st.title(teams)
        
    st.subheader('Matches over the years')
    fig1 = helper.matches_over_years(df1)
    st.plotly_chart(fig1)
    
    st.subheader('Teams playes over the years')
    fig2 = helper.team_over_years(df1)
    st.plotly_chart(fig2)
    
    st.subheader('Runs scored over the years')
    fig3 = helper.score_over_seasons(df1,df2)
    st.plotly_chart(fig3)
    
    years = df1.season.unique().tolist()
    years.insert(0,'Overall') 
    selected_year  = st.sidebar.selectbox('Select Year ',years)
    if selected_year == 'Overall':
        st.subheader('Toss winning percentage of teams')
    else:
        st.subheader(f'Toss winning percentage of teams in {selected_year}')
        
    fig3 = helper.toss_winners(df1,selected_year)
    st.plotly_chart(fig3)
    
    if selected_year == 'Overall':
        st.subheader('Match winning percentage of teams')
    else:
        st.subheader(f'Match winning percentage of teams in {selected_year}')
    fig4 = helper.win_percentage(df1,selected_year)
    st.plotly_chart(fig4)
    
    if selected_year == 'Overall':
        st.subheader('Top 10 batsmen in IPL')
    else:
        st.subheader(f'Top 10 batsmen in {selected_year}')
    top_batsmen = helper.top_bats(df1,df2,selected_year)
    fig5 = px.bar(x = top_batsmen.index, y = top_batsmen.values,labels = dict(x = 'Top 10 Batsmen',y = "Runs Scores"),text_auto = True)
    fig5.update_layout(xaxis = dict(
        tickmode = 'linear'
        
    ))
    fig5.update_traces(
                  marker=dict(line=dict(color='#000000', width=2))
                  )
    st.plotly_chart(fig5)
    
    if selected_year == 'Overall':
        st.subheader('Top 10 bowlers in IPL')
    else:
        st.subheader(f'Top 10 bowlers in {selected_year}')
    fig6 = helper.top_bowls(df1,df2,selected_year)
    st.plotly_chart(fig6)
    
    st.subheader("Highest runs scored in an innings")
    fig7 = helper.highest_innings_score(df1,df2)
    st.plotly_chart(fig7)
    
    if selected_year == 'Overall':
        st.subheader('Most player of Matches')
    else:
        st.subheader(f'Most player of Matches in {selected_year}')
    fig8 = helper.most_player_of_matches(df1,selected_year)
    st.plotly_chart(fig8)
    
elif user_menu == 'Player wise analysis':
    
    batsmans_df = df2[['id','over','ball','batsman','non_striker','batsman_runs','non_boundary','batting_team','extras_type','dismissal_kind','bowler','player_dismissed']]
    bowling_df = df2[['id','over','ball','bowler','total_runs','is_wicket','bowling_team','extras_type','dismissal_kind','batsman']]
    
    #st.title('Palyer Wise Analysis')
    st.markdown("<h1 style='text-align: center; font-family:georgia,garamond,serif;font-size:40px;'>Player Wise Analysis</h1>", unsafe_allow_html=True)
    batsmen = df2.batsman.unique().tolist()
    batsmen.sort()
    selected_batsman = st.sidebar.selectbox('Select a Batsman', batsmen)
    st.header(f'{selected_batsman}')
    runs = helper.total_runs(batsmans_df, selected_batsman)
    sixes = helper.sixes(batsmans_df, selected_batsman)
    fours = helper.fours(batsmans_df, selected_batsman)
    matches = helper.matches_of_player(batsmans_df,selected_batsman)
    average = helper.average_of_player(batsmans_df,selected_batsman)
    strikerate = helper.strike_rate(batsmans_df,selected_batsman)
    highscore = helper.high_score(batsmans_df, selected_batsman)
    type_of_dismissal = helper.dismissals(batsmans_df, selected_batsman)
    
    col1, col2 , col3  = st.columns(3)
    col4, col5,col6 = st.columns(3)
    col7, col8 = st.columns(2)
    
    with col1:
        st.subheader(f'Total Runs')
        st.title(runs)
        
    with col2:
        st.subheader(f'Sixes')
        st.title(sixes)
        
    with col3:
        st.subheader(f'Fours')
        st.title(fours)
        
    with col4:
        st.subheader('Mathes')
        st.title(matches)
        
    with col5:
        st.subheader('Average')
        st.title(round(average,2))
        
    with col6:
        st.subheader('Strike Rate')
        st.title(round(strikerate,2))
        
    with col7:
        st.subheader('High Score')
        st.title(highscore)
            
    fig10 = helper.runs_classification(batsmans_df,selected_batsman)
    
    st.subheader(f"Runs Classification")
    st.plotly_chart(fig10)
    
    st.subheader('Types of Dismissals')
    fig11 = helper.dismissals(batsmans_df,selected_batsman)
    st.plotly_chart(fig11)
    
    st.subheader('Strike rate over the years')
    fig12 = helper.str_rate_through_over(batsmans_df,selected_batsman)
    st.plotly_chart(fig12)
    
    st.subheader('Milestones')
    fig13 = helper.scores(batsmans_df,selected_batsman)
    st.plotly_chart(fig13)
    
    selected_bowler = st.sidebar.selectbox('Select a Bowler',batsmen)
    st.header(selected_bowler)
    bowlermatches = helper.bowler_matches(bowling_df,selected_bowler)
    overs = helper.overs_delivered(bowling_df,selected_bowler)
    wicket = helper.wickets(bowling_df,selected_bowler)
    average = helper.average_of_bowler(bowling_df,selected_bowler) 
    economy_of_bowler = helper.economy(bowling_df,selected_bowler)
    bestfigures = helper.best_figures(bowling_df,selected_bowler)
    
    col9, col10, col11 = st.columns(3)
    with col9:
        st.subheader('Mathces Played')
        st.title(bowlermatches) 
        
    with col10:
        st.subheader('Overs Delivered')
        st.title(round(overs,0))
    
    with col11:
        st.subheader('Wickets')
        st.title(wicket)
    
    col12,col13,col14 = st.columns(3)
    
    with col12:
        st.subheader('Average')
        st.title(average) 
        
    with col13:
        st.subheader('Economy')
        st.title(round(economy_of_bowler,1))
    
    with col14:
        st.subheader('Best Figures')
        st.title(bestfigures)
    
    st.subheader('Wicket Hauls')
    fig14 = helper.wickets_haul(bowling_df,selected_bowler)
    st.plotly_chart(fig14)
    
elif user_menu == 'Team wise analysis':
    
    st.markdown("<h1 style='text-align: center; font-family:georgia,garamond,serif;font-size:40px;'>Team Wise Analysis</h1>", unsafe_allow_html=True)        
    teams = df1.team1.unique()
    years = list(range(2008,2021))
    years.insert(0,'Overall')
    selected_team = st.sidebar.selectbox('Select an IPL team',teams)
    selected_year = st.sidebar.selectbox('Select Year',years)
    st.header(selected_team)
    
    col15 = st.columns(1)
    col16,col17 = st.columns(2)
    
    with col16:
        st.subheader('Season winners')
        st.header(helper.season_wins(df1,selected_team))
        
    with col17:
        st.subheader('Season runner ups')
        st.header(helper.runner_up_times(df1,selected_team))
    
    st.subheader('Highest Totals in First innings')    
    fig15 = helper.highest_totals_defending(season_data,selected_team,1)
    st.plotly_chart(fig15)
    
    st.subheader('Highest Totals in Second innings') 
    fig16 = helper.highest_totals_chasing(season_data,selected_team,2) 
    st.plotly_chart(fig16)
    
    st.subheader('Top 5 bowlers')
    fig19 = helper.top_bowlers(season_data,selected_team,selected_year)
    st.plotly_chart(fig19)

    st.subheader('Top 5 batsmen')
    fig20 = helper.top_batsmen(season_data,selected_team,selected_year)
    st.plotly_chart(fig20)
