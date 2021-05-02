# -*- coding: utf-8 -*-
"""Covid_Dashboard_Deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TnTFn5WvKFj9ITsw097bjob3xdinnp6Q
"""

# Import librairies
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

import pickle
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
matplotlib.use('Agg')
st.set_option('deprecation.showPyplotGlobalUse', False)


# Load data
#loaded_data = pickle.load(open('/content/gdrive/My Drive/Colab Notebooks/data_covid.dat', 'rb'))
loaded_data = pickle.load(open('data_covid.dat', 'rb'))



#"""Create a dashboard"""


def main():
    st.title('Centralisation des échanges de flacons de vaccins')
    #st.subheader('Projet proposé par:')
    

    @st.cache()  #hash_funcs={data.dict: my_hash_func}
    def load_data():
        data = loaded_data.copy()
        return data
    
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Les données chargent...')
    # Load the data into the dataframe.
    data = load_data()
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Les données sont chargées!')

    st.title('Création d\'un dataframe à partir des données originales')
    
    @st.cache()  #hash_funcs={data.dict: my_hash_func}
    def load_dataframe():
        Df = pd.DataFrame(data['data'], columns=data['feature_names'])
        #Df['score_de_priorite'] = data['score_de_priorite']
        return Df

    # Create a text element and let the reader know the dataframe has been created.
    #dataframe_load_state = st.text('Le dataframe est créé!')
    # Load the data into the dataframe.
    Df = load_dataframe()
    # Notify the reader that the data was successfully loaded.
    #dataframe_load_state.text('Les données sont chargées dans le dataframe!')

    # Make the centre_id the index ### centre_id
    #Df.set_index('centre_id', inplace=True)
    Df_regions = Df.copy()
    #Df_regions.drop(['centre_id'], axis=1, inplace=True)
    ##Df_regions.set_index('centre_id', inplace=True)

    Df_regions.semaine.unique()

    # Change fortmat 
    # Department
    Df_regions['code_departement'] = Df_regions['code_departement'].astype('int32')

    # Print the top 5 of the created Dataframe
    st.write('Ci-dessous sont affichées les 5 premières lignes du tableau de données pour une région'
              ' l\'index correspond aux départements')
    st.write(Df_regions.head(5))
    

    # BY CENTER (FROM A DEPARTMENT)

    Df_dep_total = Df_regions.copy()

    
##
    DEP = Df_regions['code_departement']
    Df_regions.set_index('code_departement', inplace=True)
    Df_regions['code_departement'] = Df_regions.index

    # Use the index to define an centre_id to look for the data of a centre individualy 
    ID_Dep = st.number_input('Entrer l\'identifiant du département, code_departement:',
                                min_value=int(DEP.index.min()), #int(Df_centres['centre_id'].min()), #
                                max_value=int(DEP.index.max()), #int(Df_centres['centre_id'].max()), #
                                format="%i",
                                )
    #Df_regions.reset_index(inplace=True)
    Df_dep = Df_regions[Df_regions.code_departement==ID_Dep]  #Df_regions.loc[ID_Dep]

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations par semaine')

    #Df_dep = Df_regions[Df_regions.code_departement==ID_Dep]


    #st.title('Nombres de flacons alloués par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_dep['semaine'] # à voir
    nombre_ucd = Df_dep['nb_ucd'] # dans df initial allocations
    ax.plot(semaines, nombre_ucd) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Nombre d\'udc')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe allocations evolution
    #st.title('Observation de l\'évolution des allocations par jour')


    st.write('******************************************************')

    # Observe stocks evolution
    st.title('Observation de l\'évolution des stocks par semaine') # ca a du sens? 

    #st.title('Nombres de flacons en stock par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_dep['semaine'] # à voir
    nombre_ucd = Df_dep['nb_ucd'] # dans df initial stock
    ax.plot(semaines, nombre_ucd) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Nombre d\'udc')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe stocks evolution
    #st.title('Observation de l\'évolution des stocks par jour')


    st.write('******************************************************')

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations et des stocks par semaine')
    ### FAIRE UN GRAPH qui regroupe les 2 du haut

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations et des stocks par jour')


    st.write('******************************************************')

    # Observe missed appointment ratio evolution
    st.title('Observation de l\'évolution du ratio de RDV manqués/RDV prévus par semaine')
    #st.title('Nombres de flacons en stock par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_dep['semaine'] # à voir
    ratio = Df_dep['ratio_efficacite'] # dans df merge tot
    ax.plot(semaines, ratio) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Ratio RDV manqués/prévus')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe missed appointment ratio evolution
    st.title('Observation de l\'évolution du ratio de RDV manqués/RDV prévus par jour')




###


##
    #Tester les 2
    #CENTRE = Df_regions['centre_id']
    CENTRE = Df_dep_total['centre_id']
    Df_dep_total['centre_id'] = Df_dep_total.index

    # Use the index to define an centre_id to look for the data of a centre individualy 
    ID_Centre = st.number_input('Entrer l\'identifiant du centre, centre_id:',
                                min_value=int(CENTRE.index.min()), #int(Df_centres['centre_id'].min()), #
                                max_value=int(CENTRE.index.max()), #int(Df_centres['centre_id'].max()), #
                                format="%i",
                                )

    # Create a dataframe with shap_values and feature_names
    #Df_centres = pd.DataFrame(shap_values,
    #                        columns=data['feature_names'][1:]) 

    Df_centres = Df_dep_total[Df_dep_total.code_departement==ID_Dep] 

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations par semaine')

    #st.title('Nombres de flacons alloués par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_centres['semaine'] # à voir
    nombre_ucd = Df_centres['nb_ucd'] # dans df initial allocations
    ax.plot(semaines, nombre_ucd) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Nombre d\'udc')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe allocations evolution
    #st.title('Observation de l\'évolution des allocations par jour')


    st.write('******************************************************')

    # Observe stocks evolution
    st.title('Observation de l\'évolution des stocks par semaine') # ca a du sens? 

    #st.title('Nombres de flacons en stock par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_centres['semaine'] # à voir
    nombre_ucd = Df_centres['nb_ucd'] # dans df initial stock
    ax.plot(semaines, nombre_ucd) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Nombre d\'udc')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe stocks evolution
    #st.title('Observation de l\'évolution des stocks par jour')


    st.write('******************************************************')

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations et des stocks par semaine')
    ### FAIRE UN GRAPH qui regroupe les 2 du haut

    # Observe allocations evolution
    st.title('Observation de l\'évolution des allocations et des stocks par jour')


    st.write('******************************************************')

    # Observe missed appointment ratio evolution
    st.title('Observation de l\'évolution du ratio de RDV manqués/RDV prévus par semaine')
    #st.title('Nombres de flacons en stock par semaine')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    semaines = Df_centres['semaine'] # à voir
    ratio = Df_centres['ratio_efficacite'] # dans df merge tot
    ax.plot(semaines, ratio) 
    ax.set_xlabel('Semaines')
    ax.set_ylabel('Ratio RDV manqués/prévus')
    #st.write(fig)
    st.pyplot(bbox_inches='tight')
    plt.clf()

    # Observe missed appointment ratio evolution
    st.title('Observation de l\'évolution du ratio de RDV manqués/RDV prévus par jour')



  

if __name__== '__main__':
    main()