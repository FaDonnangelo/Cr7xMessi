import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

#Get league teams notes
path = "/".join(__file__.split("/")[:-1]) #Gets the file path


def Players():
    df_messi = pd.read_excel(str(path) + '/Messi.xlsx') #Get Messi's Goals sheet
    df_messi = df_messi[df_messi.Equipa!='Argentina'] #Remove Argentina games

    df_cr7 = pd.read_excel(str(path) + '/Cr7.xlsx') #Get Cristiano's Goals sheet
    df_cr7 = df_cr7[df_cr7.Equipa!='Portugal'] #Remove Portugal games

    return df_messi, df_cr7

def All_Teams():

    df_messi , df_cr7 = Players()

    df_pl = pd.read_excel(str(path) + '/PremierLeague.xlsx') 
    df_serieA = pd.read_excel(str(path) + '/SerieA.xlsx') 
    df_ligue1 = pd.read_excel(str(path) + '/Ligue1.xlsx') 
    df_bundes = pd.read_excel(str(path) + '/Bundesleague.xlsx') 
    df_laliga = pd.read_excel(str(path) + '/LaLiga.xlsx') 
    df_primliga = pd.read_excel(str(path) + '/PrimeiraLiga.xlsx')
    df_eredivisie = pd.read_excel(str(path) + '/Eredivisie.xlsx')
    
    #Join all leagues dataframes
    frame = [df_pl,df_serieA,df_ligue1,df_bundes,df_laliga,df_primliga,df_eredivisie]
    #Remove the useless columns
    for i,df in enumerate(frame):
        if len(df.columns) == 6:
            df = df.drop(df.columns[[1,2,3,4]],axis=1) #Remove the useless columns
        elif len(df.columns) == 5:
            df = df.drop(df.columns[[1,2,3]],axis=1)
        else:
            df = df.drop(df.columns[[1,2]],axis=1)
        frame.pop(i)
        frame.insert(i,df) 
    #Concatenate the dataframes      
    frame = pd.concat(frame,ignore_index=True)

    df_chleague = pd.read_excel(str(path) + '/ChampionsLeague.xlsx')
    df_chleague = df_chleague.drop(df_chleague.columns[[1,2,3,4]],axis=1).to_numpy()
    df_euleague = pd.read_excel(str(path) + '/EuropaLeague.xlsx')
    df_euleague = df_euleague.drop(df_euleague.columns[[1,2,3,4]],axis=1).to_numpy()
    frame = frame.to_numpy()

    #Add Champions League and Europa League to the Points Table
    for i in frame:
        for j in df_chleague:
            if i[0] == j[0]:
                i[1] = i[1] + j[1]
    for i in frame:
        for j in df_euleague:
            if i[0] == j[0]:
                i[1] = i[1] + j[1]

    #Create a new array for the notes and scale it 
    notes = np.zeros((len(frame),1))
    for i,element in enumerate(frame):
        notes[i,0] = element[1]
    #Scale the array with values between 1 and 2
    scaler = MinMaxScaler(feature_range=(1,2))
    scaled_data = scaler.fit_transform(notes)

    #Add the scaled notes to the teams array
    for i in range(len(scaled_data)):
        frame[i,1] = scaled_data[i,0]

    total_teams_messi = df_messi.Adversário.to_frame().drop_duplicates() #Get all teams Messi and Cristiano played against
    total_teams_messi.insert(1,"Notes",0.5) #Insert standart points for all teams Messi and Cristiano played against
    total_teams_cr7 =  df_cr7.Adversário.to_frame().drop_duplicates()
    total_teams_cr7.insert(1,"Notes",0.5)
    total_teams_messi = total_teams_messi.to_numpy()
    total_teams_cr7 = total_teams_cr7.to_numpy()


    for i,value in enumerate(total_teams_messi):    #Uptade the teams points column with the scaled points
        for j in frame:
            if value[0] == j[0]:
                total_teams_messi[i,1] = j[1]

    for i,value in enumerate(total_teams_cr7):
        for j in frame:
            if value[0] == j[0]:
                total_teams_cr7[i,1] = j[1]

    df_messi.drop(df_messi.columns[[0, 1, 2, 3, 4, 5 ,7]], axis = 1, inplace = True) #Remove useless colums in the goals table
    df_messi = df_messi.to_numpy()

    df_cr7.drop(df_cr7.columns[[0, 1, 2, 3, 4, 5 ,7]], axis = 1, inplace = True) #Remove useless colums in the goals table
    df_cr7 = df_cr7.to_numpy()

    total_points_messi = 0
    for value in df_messi:
        for value2 in total_teams_messi:
            if value[0] == value2[0]:
                total_points_messi += (value[1]*value2[1])

    total_points_cr7 = 0
    for value in df_cr7:
        for value2 in total_teams_cr7:
            if value[0] == value2[0]:
                total_points_cr7 += (value[1]*value2[1])

    return total_points_messi, total_points_cr7


messi_result , cr7_result = All_Teams()

print("Messi: " + str(messi_result) + " Cr7: " + str(cr7_result))