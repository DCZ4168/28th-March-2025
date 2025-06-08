import statistics as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#Part 1: CV of EMT and LV1



Freqs = [] #List of frequencies for EMT and 331, 332, 333, 334: manual calculation

Freqs.append([14, 15, 13, 11, 1, 1, 1, 11, 11, 8, 7, 14, 6, 11, 11])               #63E
Freqs.append([13, 2, 9, 3, 0, 9, 14, 9, 2, 2, 5, 10, 6, 6, 11, 6, 13, 11])         #63W
Freqs.append([13, 9, 26, 16, 7, 13, 14, 15, 13, 15])                               #90E
Freqs.append([8, 9, 11, 18, 15, 14, 12, 16, 17])                                   #90W
Freqs.append([15, 16, 10, 18, 24, 11, 20, 19])                                     #145E
Freqs.append([9, 12, 26, 3, 15, 5, 0, 7, 18, 14, 11, 8])                           #145W
Freqs.append([12, 7, 9, 14, 15, 16, 15, 11])                                       #331E
Freqs.append([11, 11, 14, 30, 8, 11])                                              #331W
Freqs.append([12, 15, 14, 15, 14, 15, 15, 18])                                     #332E
Freqs.append([16, 1, 5, 17, 19, 14, 12, 12, 15])                                   #332W
Freqs.append([15, 26, 16, 14, 13, 19])                                             #333E
Freqs.append([19, 18, 14, 9, 13, 0, 19, 14, 15])                                   #333W
Freqs.append([11, 3, 13, 12, 18, 16, 12, 14])                                      #334E
Freqs.append([28, 17, 21, 11, 10, 15, 13, 17])                                     #334W

CVs = []

for i in range(13): 
    mean = st.mean(Freqs[i])
    sd = st.stdev(Freqs[i])
    CV = round(sd/mean*100,2)
    CVs.append(CV)
print(CVs)



#Part 2: Study of occupation



df = pd.read_csv('resources\\280325.csv') #Load the CSV from my own folder, you edit the route to your convenience, this was my case
df = df.iloc[:, :-1] #Delete the last column, it doesn't provide any information, just NaN
df['Occupation'] = pd.to_numeric(df['Occupation'],errors='coerce') #It was loaded as a string
groups_of_lines = {'63':'EMT','90':'EMT','145':'EMT','312':'ALSA','312A':'ALSA','313':'ALSA','326':'ALSA','331':'LV1','332':'LV1',
'333':'LV1','334':'LV1','336':'LV2','337':'LV2','341':'Avanza','351':'Ruiz','352':'Ruiz','353':'Ruiz'}
remarks_to_group = {'Possible331/332/333/334': 'LV1','Possible351/352/353':'Ruiz'} #For those observations for which I couldn't identify the line
df['Group'] = df['Line'].map(groups_of_lines)
df['Group'] = df['Group'].fillna('Other')
dfnormal = df[df['TypeS'] == 'N']  #We now put the focus on occupation: TypeS == 'N'
dfnormal = dfnormal.dropna(subset=['Occupation'])
fig1, ax1 = plt.subplots()
sns.boxplot(data=dfnormal,x='Line',y='Occupation',hue='Dir',ax=ax1)
ax1.set_title("Occupation per line and direction: boxplot format")
fig1.savefig("280325_01.png",dpi=400)
fig1.show()



#Part 3: Contrast of scheduling hypothesis witn pandas



#I use the same dataframe df as in #Part 2

conditions = [  #To create a link between observations without identification of the line, but of the group, and the data frame
    df['Remarks'].str.contains('Possible331/332/333/334', na=False),  
    df['Remarks'].str.contains('Possible351/352/353', na=False)           
]
values = ['LV1', 'Ruiz']

df['TypeSGroup'] = df['TypeS'].map({            '''We divide TypeS in two groups: normal operations (with passengers, 
                                                providing actual service) and Deadheading/To Garage. We don't count other type'''
    'N': 'Normal',  
    'G': 'Deadheading/To Garage',  
    'D': 'Deadheading/To Garage'
})

df['Group'] = np.select(conditions, values, default=df['Group'])
total_per_group_line = df.groupby(['Group','Dir']).size()  #Total of observations per group line
count_per_linegroups_dg = df[df['TypeSGroup'] == 'Deadheading/To Garage'].groupby(['Group','Dir']).size()  #Total of obserrvations per group line for D/G
proportion_per_types_group = count_per_linegroups_dg/total_per_group_line  #Proportion measure
proporcion_df = proportion_per_types_group.reset_index(name='Prop')   #Convert from measure to dataframe
proporcion_df = proporcion_df[proporcion_df['Group'] != 'Other']  #Filter 
fig2, ax2 = plt.subplots()
sns.barplot(data=proporcion_df,x='Group',y='Prop',hue='Dir',ax=ax2)
ax2.set_title("Proportion of D/G services w.r.t. total services per line group and direction")
fig2.tight_layout()
fig2.savefig("280325_02.png",dpi=400)
fig2.show()      #Show the both plots: from #Part 2 and from #Part 3

dfknown = df[df['Line'].isin(['63','90','145','312','312A','313','326','331','332','333','334','336','337','341','351','352','353'])]        
#Just for observations whose line is known and those lines relevant to the study
total_per_knownline = dfknown.groupby(['Line','Dir']).size()
count_per_line_dg = dfknown[dfknown['TypeSGroup'] == 'Deadheading/To Garage'].groupby(['Line','Dir']).size()   #Same as the previous fig but for individual known lines
proportion_per_types_group_ind = count_per_line_dg/total_per_knownline  #Proportion measure
proportion_df_known = proportion_per_types_group_ind.reset_index(name='Prop')   #Convert from measure to dataframe 
fig3, ax3 = plt.subplots()
sns.barplot(data=proportion_df_known,x='Line',y='Prop',hue='Dir',ax=ax3)
ax3.set_title("Proportion of D/G services w.r.t. total services per line and direction")
fig3.tight_layout()
fig3.savefig("280325_03.png",dpi=400)
fig3.show() 