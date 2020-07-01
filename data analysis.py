from tkinter import *
import pandas as pd
import matplotlib.pyplot as graph
import seaborn as born
import warnings
warnings.filterwarnings('ignore')


BowlerData = pd.read_csv('G:/cricket/Bowler_Data.csv')
Batsman_Data = pd.read_csv('G:/cricket/Batsman_Data.csv')
Ground_Averages = pd.read_csv('G:/cricket/Ground_Averages.csv')
odimatches = pd.read_csv( 'G:/cricket/ODI_Match_Totals.csv')
ODI_Match_Results = pd.read_csv('G:/cricket/ODI_Match_Results.csv')
WC_players = pd.read_csv('G:/cricket/WC_players.csv')

# print(Ground_Averages.head(80))
# print(odimatches)
# print(ODI_Match_Results)
odimatches["scores"] = odimatches["Unnamed: 0"]
odimatches.drop(columns = "Unnamed: 0", inplace = True)

wcpitches = [ "Eden Gardens, Kolkata",
                        "Saurashtra Rajkot ",
                        "Nehru Stadium, Kochi",
                        "JSCA Stadium , Ranchi ",
                        "Punjab Cricket Stadium, Mohali",
                        "Himachal Pradesh Stadium, Dharamsala",
                        "Maharashtra  Stadium, Pune ",
                        "Sawai Mansingh Stadium, Jaipur" ,
                        "Vidarbha  Stadium, Nagpur ",
                        "M.Chinnaswamy Stadium, Bengaluru ",
                        "Green Park, Kanpur",
                        "Barabati Stadium, Cuttack ",
                        "Sardar Patel (Gujarat) Stadium, Ahmedabad ",
                        "Rajiv Gandhi  Uppal",
                        "Holkar Cricket Stadium, Indore",
                        "MA Chidambaram Stadium, Chepauk",
                        "Wankhede Stadium, Mumbai ",
                        "Barsapara Cricket Stadium, Guwahati ",
                        "Brabourne Stadium, Mumbai",
                        "Greenfield , Thiruvananthapuram",
                        "Rajiv Gandhi  Dehradun ",
                     ]

groundstats = []
odigrounds = odimatches.Ground
for i in odigrounds:
    for j in wcpitches:
        if i in j:

            groundstats.append((i, j))



gnames = dict( set( groundstats ) )


def fullgnames(value):
    return gnames[ value ]


def ghist():
    ghistory = odimatches[ odimatches.Ground.isin( [ Ground[ 0 ] for Ground in groundstats ] ) ]
    ghistory[ "Ground" ] = ghistory.Ground.apply( fullgnames )
    teammatches = ghistory.Country.value_counts().reset_index()
    graph.figure( figsize = (7, 8) )
    born.barplot( x = "index", y = "Country", data = teammatches ).set_title( "Total Matches Played by each Country" )
    graph.xlabel( "Country" )
    graph.ylabel( "Matches Played" )
    graph.xticks( rotation = 60 )
    graph.show()
    print(ghistory.head(5))

ghistory = odimatches[ odimatches.Ground.isin( [ Ground[ 0 ] for Ground in groundstats ] ) ]
ghistory[ "Ground" ] = ghistory.Ground.apply( fullgnames )
ghistory = ghistory[~ghistory.Result.isin(["-"])]
#print(ghistory.Result.value_counts())

def gwinning():
    winnings = ghistory[["Country", "Result"]]
    winnings["count"] = 1
    gresults = winnings.groupby(["Country", "Result"]).aggregate(["sum"])
    gresults = gresults.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).reset_index ()
    gresults.columns = ["Country", "Result", "Count"]
    print(gresults)
    graph.figure(figsize=(7, 8))
    born.barplot(x = "Country", y = "Count", hue = "Result", data = gresults)
    graph.ylabel("Percentage")
    graph.title("Country - Results")
    graph.xticks(rotation = 60)
    graph.show()


def gwinningone():
    Inning_Wins = ghistory[ghistory.Result == "won"].Inns.value_counts(normalize = True).reset_index()
    born.barplot(x = "index", y = "Inns", data = Inning_Wins).set_title("winnings by Innigs")
    graph.xlabel("innings")
    graph.ylabel("Winning Percentage")
    graph.figure(figsize=(7, 8))
    graph.show()


    innings = ghistory[ghistory.Result == "won"][["Inns","Ground"]]
    innings["Count"] = 1
    innings = innings.groupby(["Ground","Inns"]).sum()
    innings = innings.groupby(level=0).apply(lambda x:100 * x / float(x.sum())).reset_index()
    innings.columns = ["Ground", "Inns","Wins"]

    #print(innings.head(5))


    graph.figure(figsize=(15,8))
    born.barplot(x = "Ground", y = "Wins", hue = "Inns", data = innings).set_title("innings vs winnings")
    graph.xticks(rotation = 60)
    #graph.show()


def gscorewkt():
    scores = ghistory[ [ "Score_without_wickets", "Ground" ] ]
    scores = scores[ scores.Score_without_wickets > 50 ]
    scores = scores[scores.Score_without_wickets > 50]
    scores = scores.groupby("Ground").mean().reset_index()
    graph.figure(figsize=(7, 8))
    born.barplot(x = "Ground", y = "Score_without_wickets", data = scores).set_title("Average scores of Pitches")
    graph.xticks(rotation = 60)
    graph.ylabel("scores")
#    graph.show()

def no_of_wickets(value):
    if "/" not in value:
        return 10
    elif "D" in value:
        return 0
    else:
        return int( value.split( "/" )[ 1 ] )

ghistory[ "Total_wickets" ] = ghistory.Score.apply( no_of_wickets )

wickets = ghistory[ [ "Total_wickets", "Ground" ] ]
wickets = wickets.groupby( "Ground" ).mean().reset_index()

def gAveragewicketsinnings():
    graph.figure(figsize=(7, 8))
    born.barplot(x = "Ground", y = "Total_wickets", data = wickets).set_title("Average No.of wickets Per innings")
    graph.show()


Grounds = ghistory.Ground.unique()
WC_Teams = ghistory.Country.unique()
winnings = {}
for Ground in Grounds:
    winnings.update({Ground : {}})
    for Team in WC_Teams:
        Country_Ground_Record = ghistory[(ghistory.Country == Team) & \
                                                   (ghistory.Ground == Ground)]
        print("Ground : ", Ground, "Team : ", Team)
        matches_played = len(Country_Ground_Record)
        if matches_played== 0:
            continue
        matches_won = len(Country_Ground_Record[Country_Ground_Record.Result == "won"])
        winperc = matches_won / matches_played *100
        winnings[Ground].update({Team : {"matches_played-" : matches_played,\
                                       "matches_won": matches_won,\
                                       "winperc" : winperc}})
#print(winnings['Eden Gardens,Kolkata-India'])

team_wise_data = [ ]
for Pitch, P_Data in winnings.items():

    for Team, Team_Data in P_Data.items():
        inside = [ ]
        inside.extend( [ Pitch, Team, Team_Data[ "matches_played-" ], \
                         Team_Data[ "matches_won" ], Team_Data[ "winperc" ] ] )
        team_wise_data.append( inside )
Cols = [ "Ground", "Country", "Played", "Won", "winperc" ]

teamwins = pd.DataFrame( team_wise_data, columns = Cols )

def gcoun():
    graph.figure(figsize=(7, 8))
    born.barplot( x = "Ground", y = "winperc", hue = "Country", data = teamwins, \
                 hue_order = [ "India", "England", "Pakistan", "Australia" ] )
    graph.xticks( rotation = 60 )
    graph.show()

def gcounoe():
    graph.figure(figsize=(7, 8))
    born.barplot(x = "Ground", y = "winperc",hue = "Country", data = teamwins,\
                hue_order = ["SouthAfrica","Newzealand","WestIndies","Sri Lanka"])
    graph.xticks(rotation = 60)
    graph.plot()
    graph.show()

Ground_Averages = pd.read_csv('G:/cricket/Book1.csv')

X=Ground_Averages.iloc[:,:-1].values
Y=Ground_Averages.iloc[:,:-1].values


born.barplot( x = "Ave", y = "RPO", data = Ground_Averages )
graph.xlabel("Average")
graph.ylabel("Runs per over")
graph.xticks( rotation = 60 )
# graph.show()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size = 1/3)

from sklearn.linear_model import LinearRegression
ir=LinearRegression()
ir.fit(X_train,y_train)
def lr():
    yyy=ir.predict(X_test)
    print(yyy)
    graph.scatter(X_test,y_test,color='blue')
    graph.plot(X_train,ir.predict(X_train),color='red')
    graph.title("graph")
    graph.show()




#BATSMAN
Batsman_Data.drop( columns = Batsman_Data.columns[ 0 ], inplace = True )
Batsman_Data = Batsman_Data[ ~Batsman_Data.Bat1.isin( [ "DNB", "TDNB" ] ) ]
Batsman_Data = Batsman_Data[ Batsman_Data.Player_ID.isin(WC_players.ID ) ]
Stadiums = [ item[ 0 ] for item in set( groundstats ) ]
BatinIndia = Batsman_Data[ Batsman_Data.Ground.isin( Stadiums ) ]


def outornot(value):
    if "*" in value:
        return 0
    else:
        return 1


BatinIndia[ "outornot" ] = BatinIndia.Bat1.apply( outornot )
change_type = [ "Runs", "BF", "4s", "6s" ]
for i in change_type:
    BatinIndia[ i ] = BatinIndia[ i ].astype( "int" )

BatsmanInfo = BatinIndia
BatinIndia = BatinIndia.groupby( [ "Ground", "Batsman" ] ).sum().reset_index()

BatScore = BatinIndia.groupby( [ "Batsman" ] ).sum().reset_index()
BatScore[ "Average" ] = BatScore[ "Runs" ]  / BatScore[ "outornot" ]


BestBatAvg = BatScore[ (BatScore.outornot > 10) & (BatScore.Average > 40) ] \
.sort_values( by = "Average", ascending = False )
# def BestBatAvg():
#     print(BestBatAvg.head( 5 ))

Player_WC_ID = Batsman_Data[ [ "Player_ID", "Batsman" ] ].drop_duplicates()

Player_ID = list(
BestBatAvg.merge( Player_WC_ID, how = "left", on = "Batsman" )[ "Player_ID_y" ].astype( "int" ) )
BestBatAvg[ "Player_ID" ] = Player_ID
WC_players.columns = [ "Player", "Player_ID", "Country" ]
CountryWisePlayer = list( BestBatAvg.merge( WC_players, how = "left", on = "Player_ID" )[ "Country" ] )
BestBatAvg[ "Country" ] = CountryWisePlayer
#print( BestBatAvg )


def Bestavg():
    #print(BestBatAvg)
    BestBatAvg[ "Strike_Rate" ] = BestBatAvg[ "Runs" ] / BestBatAvg[ "BF" ] * 100
    print(BestBatAvg.head(5))
def BestBatstr( ):
    BestBatAvg[ "4s_avg" ] = BestBatAvg[ "4s" ] / BestBatAvg[ "outornot" ]
    BestBatAvg[ "6s_avg" ] = BestBatAvg[ "6s" ] / BestBatAvg[ "outornot" ]
    print(BestBatAvg.sort_values(by = ["4s_avg"],ascending=False).head())
    #print(BestBatAvg.sort_values(by = ["6s_avg"],ascending=False).head())

def bestonboundry():
        print(BestBatAvg.sort_values(["Strike_Rate"],ascending = False))
        born.countplot( BestBatAvg[ "Country" ] ).set_title( "No.of Best Batsman per Team" )
        graph.xticks( rotation = 60 )
        graph.figure( figsize = (7, 8) )
        graph.show()

def BestBatcountry():
    print( BestBatAvg[["Country", "Batsman"]].sort_values("Country"))



#BOWLER
#print("Bowler Data")
BowlerData = BowlerData[ BowlerData.Ground.isin( Stadiums ) ]
BowlerData = BowlerData[ ~BowlerData.Overs.str.contains( '-' ) ]
#print( BowlerData.sample( 5 ) )


def overs_to_ball(value):
    if "." in value:
        over = value.split( "." )
        return int( over[ 0 ] ) * 6 + int( over[ 1 ] )
    else:
        return int( value ) * 6

#BOWLERS


BowlerData[ "Balls" ] = BowlerData.Overs.apply( overs_to_ball )
for j in [ 'Runs', 'Madeins', 'Wickets', 'Balls' ]:
    BowlerData[ j ] = BowlerData[ j ].astype( "float" )
BowlerData.Ground = BowlerData.Ground.apply( fullgnames )
BowlerInIndia = BowlerData.groupby( [ "Bowler" ] ).sum()[ [ "Runs", "Madeins", "Wickets", "Balls" ] ].reset_index()
BowlerInIndia[ "Economy" ] = BowlerInIndia.Runs * 6 / BowlerInIndia.Balls
BowlerInIndia[ "Average" ] = BowlerInIndia.Runs / BowlerInIndia.Wickets
BowlerInIndia[ "Strike_Rate" ] = BowlerInIndia.Balls / BowlerInIndia.Wickets
def bowler():
    print( BowlerInIndia.sample( 5 ) )

BowlerInIndia = BowlerInIndia[ (BowlerInIndia.Balls > 36) & (BowlerInIndia.Wickets > 5) ]
#print( BowlerInIndia )

Player_WC_ID = BowlerData[ [ "Player_ID", "Bowler" ] ].drop_duplicates()

BowlerInIndia = BowlerInIndia.merge( Player_WC_ID, how = "left", on = "Bowler" )

CountryWisePlayer = list( BowlerInIndia.merge( WC_players, how = "left", on = "Player_ID" )[ "Country" ] )
BowlerInIndia[ "Country" ] = CountryWisePlayer


#print( BowlerInIndia.head(5) )

# highest_no_madians
def BowlerIndia():
    print( BowlerInIndia.sort_values( by = [ "Madeins" ], ascending = False )[ :5 ] )

BowlerInIndia[ "Maidens_per_Overs_Percentage" ] = \
    ((BowlerInIndia.Madeins * 6) / (BowlerInIndia.Balls)) * 100
def bowlerfullstat():
    print( BowlerInIndia.sample( 5 ) )

( BowlerInIndia.sort_values( by = [ "Maidens_per_Overs_Percentage" ], ascending = False )[ :10 ] )

( BowlerInIndia.sort_values( by = [ "Average" ] )[ :10 ] )

( BowlerInIndia.sort_values( by = [ "Wickets" ], ascending = False )[ :10 ] )

# bower teamwise
aggregations = {
    'Runs': 'sum',
    'Madeins': 'sum',
    'Wickets': 'sum',
    'Balls': 'sum',
    'Economy': 'mean',
    'Average': 'mean',
    'Strike_Rate': 'mean',
    'Maidens_per_Overs_Percentage': 'mean'
}

TeamwiseBowler = BowlerInIndia.groupby( 'Country' ).agg( aggregations ).reset_index()
def bowlerbyteams():
    print( BowlerInIndia )

def ghaphofteams():
    graph.figure( figsize = (7, 8) )
    g = born.lineplot( data = TeamwiseBowler[ TeamwiseBowler.columns[ 6:8 ] ] )
    g.set_xticklabels( [ "India" ] + [ item for item in TeamwiseBowler.Country ] )
    graph.xticks( rotation = 60 )
    graph.show()
    graph.figure(figsize=(7, 8))
    g = born.lineplot( data = TeamwiseBowler[ [ "Economy", "Maidens_per_Overs_Percentage" ] ] )
    g.set_xticklabels( [ "India" ] + [ item for item in TeamwiseBowler.Country ] )
    graph.xticks( rotation = 60 )
    graph.show()

BestBowler = BowlerInIndia[ (BowlerInIndia.Balls > 150) & \
                                          (BowlerInIndia.Average < 40) & \
                                          (BowlerInIndia.Strike_Rate < 40) & \
                                          (BowlerInIndia.Economy < 7.5)]

def bestbowler():
   print( BestBowler )
def BestBowlersTeam():
    born.countplot( BowlerInIndia[ (BowlerInIndia.Balls > 150) & \
                                         (BowlerInIndia.Average < 40) & \
                                         (BowlerInIndia.Strike_Rate < 40) & \
                                         (BowlerInIndia.Economy < 7.5) ].Country ). \
        set_title( "No.of Best Bowlers per Team" )
    graph.xticks( rotation = 60 )
    graph.show()

# # AllRonder

#print("All rounder Data")


BowlerData = BowlerData[ BowlerData.columns[ 1: ] ]
BowlerData.columns = [ 'Overs', 'Maidens', 'Runs_Given', 'wickets', 'Economy', 'Bowling_Average', 'Bowling_StrikeRate',
                        'Opposition', \
                        'Ground', 'Start_Date', 'Match_ID', 'Player', 'Player_ID', 'Balls_Bowled' ]
#print( BowlerData.sample( 5 ) )
BatsmanInfo.sample( 5 )
BatsmanInfo.Ground = BatsmanInfo.Ground.apply( fullgnames )
BatsmanInfo = BatsmanInfo[ [ "Runs", "BF", "SR", "4s", "6s", "Match_ID", \
                                                       "Player_ID", "outornot"]]
BatsmanInfo.columns = [ "Runs_Scored", "Balls_Faced", "Batting_StrikeRate", "4s", "6s",\
                                     "Match_ID", "Player_ID", "outornot" ]
def Batinfo():
    print( BatsmanInfo.sample( 5 ) )

AllRounder = BowlerData.merge( BatsmanInfo, on = [ "Match_ID", "Player_ID" ] )
def Allrounder():
    print( AllRounder.head( 5 ) )
AllRounder = AllRounder.groupby( [ "Player_ID", "Player" ] ).sum().reset_index()
#print( AllRounder.sample( 5 ) )
AllRounder[ "Economy" ] = AllRounder.Runs_Given*6/AllRounder.Balls_Bowled
AllRounder[ "Bowling_StrikeRate" ] = AllRounder.Runs_Given / AllRounder.wickets
AllRounder[ "Bowling_Average" ] = AllRounder.Balls_Bowled / AllRounder.wickets
# Batting Stats
AllRounder[ "Batting_Average" ] = AllRounder.Runs_Scored / AllRounder.outornot
AllRounder[ "Batting_StrikeRate" ] = AllRounder.Runs_Scored * 100 / AllRounder.Balls_Faced
def allr():
    print( AllRounder.head( 5 ) )
AllRounder[ (AllRounder.Balls_Bowled > 120) & \
                 (AllRounder.Economy < 7) & \
                   (AllRounder.Batting_StrikeRate > 70) & \
                   (AllRounder.Batting_Average > 35) ]
def allroun():
    print( AllRounder.head(5))




root = Tk()
root.geometry("400x400")
#for jpg

def openbat():
    top = Toplevel()
    top.geometry("400x400")


    b9= Button( top, fg = "red", text = "best batsman on strike rate&avg", command = Bestavg)
    b9.pack( fill = "x")

    #b9.bind('<Double-1>',openbat)

    b9= Button( top, fg = "red", text = "batsman on most 4's&6's  ", command = BestBatstr)
    b9.pack( fill = "x")

    b9 = Button( top, fg = "red", text = "which country have highest no of best batsman(graph)", command = bestonboundry)
    b9.pack( fill = "x" )

    b9= Button( top, fg = "red", text = "Best Batsman in India  ", command = BestBatcountry)
    b9.pack( fill = "x")


def openball( ):

    top = Toplevel()
    top.geometry( "400x400" )
    b8 = Button( top, fg = "red", text = "Best Bowler list teamwise", command = bowlerbyteams )
    b8.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "Bowler  graph economy vs maidens ", command = ghaphofteams )
    b9.pack( fill = "x" )



    b9 = Button( top, fg = "red", text = "Best Bowler Teamwise graph", command = BestBowlersTeam )
    b9.pack( fill = "x" )



    b9 = Button( top, fg = "red", text = "Best Bowlers in India ", command = BowlerIndia )
    b9.pack( fill = "x" )



def openallrounder( ):
    top = Toplevel()
    top.geometry( "400x400")


    b9 = Button( top, fg = "red", text = "best allrounder av", command = allr  )
    b9.pack( fill = "x" )


def openground( ):
    top = Toplevel()
    top.geometry( "400x400")
    b8 = Button( top, fg = "red", text =" winnings" , command = gwinning )
    b8.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "Ground history", command = ghist )
    b9.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "Innings vs winnings ", command =ghaphofteams )
    b9.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "Avg wicket  ", command = gAveragewicketsinnings)
    b9.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "gcoun ", command = gcoun )
    b9.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "gcounone ", command = gcounoe )
    b9.pack( fill = "x" )

    b9 = Button( top, fg = "red", text = "Linear reg ", command = lr )
    b9.pack( fill = "x" )
#Frames

f1=Frame(root, bg="grey", borderwidth=6, relief=SUNKEN)
f1.pack(side=TOP, fill="x",anchor="nw")

f2=Frame(root, bg="blue", borderwidth=6, relief=SUNKEN)
f2.pack(side=TOP, fill="x")

f3=Frame(root, bg="orange", borderwidth=6, relief=SUNKEN)
f3.pack(side=TOP, fill="x")

f4=Frame(root, bg="black", borderwidth=6, relief=SUNKEN)
f4.pack(side=TOP, fill="x")

f5=Frame(root, bg="white", borderwidth=6, relief=SUNKEN)
f5.pack(side=TOP, fill="x")




#button


b1=Button(f1,fg="red",text="Batsman Data", command=openbat).pack(fill="x")

b2=Button(f2,fg="black",text="Bowler Data",command=openball).pack(fill="x")



b3=Button(f4,fg="red",text="All rounder Data",command=openallrounder).pack(fill="x")

b4=Button(f3,fg="orange",text="Ground Data",command=openground).pack(fill="x")
root.mainloop()