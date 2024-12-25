#version melanie
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

#pour la visualisation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import ast

#pour le ML 
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer

#creer template de fond 
st.markdown("""
    <style>
    /* Fond global pour l'application */
    .stApp {
        background-image: url('https://usbeketrica.com/media/69246/download/3872959826_57043705df_k.jpg?v=1&inline=1');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ciblage des widgets (conteneur principal) */
    div.block-container {
        background: rgba(255, 255, 255, 0.85); /* Transparence blanche */
        border-radius: 15px; /* Coins arrondis */
        padding: 20px; /* Espacement interne */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# Créer le menu dans la barre latérale
# Menu de navigation
with st.sidebar:
    selection = option_menu(
        menu_title="Menu",  # Titre du menu dans la sidebar
        options=["Accueil",'Presentation Client','Etude de marché','Recherche précise', "Recommandations","Films vus ♥️","Films à voir 👍","KPI","Propositions client"],
        icons=["house-door","person-video","film", "search","camera-reels","clipboard2-check","clipboard2-check","bar-chart","easel2"],
        default_index=0,
        orientation="horizontale",  # Menu horizontale 
        styles={
            "container": {"padding": "5px"},
            "icon": {"font-size": "20px", "color": "#000000"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "10px", 
                "--hover-color": "#f08080"
            },
            "nav-link-selected": {"background-color": "#f08080"}
        }
    )


if 'viewed_movies' not in st.session_state:
    st.session_state['viewed_movies'] = []
#fonction pour mon onglet "j'ai vu"
def film_vu(movie):
    movie_title = movie['title_y']  # On accède directement à la clé 'Titre'

    # Vérification si la liste viewed_movies existe dans st.session_state
    if 'viewed_movies' not in st.session_state:
        st.session_state.viewed_movies = []

    # Vérification si le film est déjà marqué comme vu
    if movie_title in st.session_state.viewed_movies:
        st.session_state.viewed_movies.remove(movie_title)  # Retirer le titre de la liste des films vus
        st.success(f"Le film **{movie_title}** a été retiré de la liste des films vus.")
    else:
        st.session_state.viewed_movies.append(movie_title)  # Ajouter le titre à la liste des films vus
        st.success(f"Vous avez marqué le film **{movie_title}** comme vu !")


if 'list_movies' not in st.session_state:
    st.session_state['list_movies'] = []
#fonction pour mon onglet "Ma liste de films à voir"
def film_a_voir(movie):
    movie_title = movie['title_y']  # On accède directement à la clé 'Titre'

    # Vérification si la liste viewed_movies existe dans st.session_state
    if 'list_movies' not in st.session_state:
        st.session_state.list_movies = []

    # Vérification si le film est déjà marqué comme vu
    if movie_title in st.session_state.list_movies:
        st.session_state.list_movies.remove(movie_title)  # Retirer le titre de la liste des films vus
        st.success(f"Le film **{movie_title}** a été retiré de la liste des films à voir.")
    else:
        st.session_state.list_movies.append(movie_title)  # Ajouter le titre à la liste des films à voir
        st.success(f"Vous avez marqué le film **{movie_title}** comme à voir !")


# On indique au programme quoi faire en fonction du choix
if selection == "Accueil":
                st.title("Bienvenue sur MatchMyMovie")
                st.subheader("Retrouvez des films qui matchent avec vos envies !")
                col1, col2 ,col3, col4 = st.columns(4)
                with col1:
                    st.image("https://image.tmdb.org/t/p/original/v0dj9NVPFTX0bv5NtqxK99i1Ae3.jpg") #Mission: Impossible - Rogue Nation 
                    st.image("https://image.tmdb.org/t/p/original/sNL1aPGCMFmcnNDFWVUKehO3Vjr.jpg") #OSS 117 : Rio ne répond plus
                    st.image("https://image.tmdb.org/t/p/original/dfht1lGq2ALbrRkMj35dUrj5kHG.jpg")  #Bienvenue chez les Ch'tis
                with col2:
                    st.image("https://image.tmdb.org/t/p/original/smFyhZHuOCZEmH0kfXOrJLC3Acx.jpg") #Toy Story 4 
                    st.image("https://image.tmdb.org/t/p/original/yJm61MmTMjOmNXxPxdoaIkdqnOm.jpg") # Harry Potter and the Deathly Hallows
                    st.image("https://image.tmdb.org/t/p/original/A0Th0x8QIzP0njrFAJnYQ5ouIoB.jpg") #Forrest Gump
                with col3:
                    st.image("https://image.tmdb.org/t/p/original/tz4DUBcxU7UowOIJwqvQfdWkU2U.jpg") #The Polar Express
                    st.image("https://image.tmdb.org/t/p/original/gdUJ6ECIHNE5M2HImGaBOfb8jR2.jpg")  #Intouchables
                    st.image("https://image.tmdb.org/t/p/original/ybjooZMNlRBaFNfs52XqONc4Xyw.jpg")#Deadpool 2"
                with col4:
                    st.image("https://image.tmdb.org/t/p/original/obsGPyNOAwkQbLRQOHR6a21VT23.jpg")#Rogue One: A Star Wars Story
                    st.image("https://image.tmdb.org/t/p/original/aZ7JWKenzR28H4bCgFJwdCuHovW.jpg")#Babysitting 
                    st.image("https://image.tmdb.org/t/p/original/2k0mHrCtIydYR0RA4RyjhRc2hNN.jpg") #Scream

elif selection == "Presentation Client":
                #st.title("")
                #st.subheader("**Un cinéma situé dans la Creuse constate une baisse de fréquentation et souhaite moderniser son approche pour attirer et fidéliser une clientèle locale. Le projet consiste à développer un site Internet dédié aux habitants de la région et à mettre en place un moteur de recommandations de films, capable de communiquer avec les clients.**")
                #st.subheader("Voici la salle de projection de notre client")
                #st.video("https://www.youtube.com/watch?v=6ocJK8jQ6sI")
                
                # CSS pour le style
                st.markdown(
                    """
                    <style>
                    .cinema-desc {
                        font-size: 1.2em;
                        color: #444;
                        background-color: #f9f9f9;
                        padding: 10px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }
                    .video-container {
                        text-align: center;
                        margin-top: 30px;
                    }
                    .header-title {
                        color: #2c3e50;
                        font-family: 'Arial', sans-serif;
                        margin-bottom: 20px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Contenu stylisé
                st.markdown('<h2 class="header-title">Présentation client</h2>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="cinema-desc">
                        <strong>Un cinéma situé dans la Creuse constate une baisse de fréquentation et souhaite moderniser son approche 
                        pour attirer et fidéliser une clientèle locale. 
                        Le projet consiste à développer un site Internet dédié aux habitants 
                        de la région et à mettre en place un moteur de recommandations de films, capable de communiquer avec les clients.</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown('<h4 class="header-title">Voici la salle de projection de notre client</h4>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="video-container">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/6ocJK8jQ6sI" frameborder="0" allowfullscreen></iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                

elif selection == "Etude de marché":
                #st.title("")
                #st.write("Description :")
                #st.write("La Creuse est un département français situé dans la région Nouvelle-Aquitaine et ayant appartenu, avant 2016, à la région Limousin avant la disparition de cette dernière. Il succède à la province de la Marche dont il reprend une grande partie du territoire.")
                #st.write("Population : 115 702 hab. (2021)")
                #st.write("Capitale : Guéret")
                #st.write("Superficie : 5 565 km²")
                #st.write("Cantons : 15")

                #col1, col2 = st.columns(2)
                                #with col1:
                                #        st.image("https://www.actualitix.com/wp-content/uploads/2017/05/ou-se-trouve-creuse.jpg")
                                #        st.write("Localisation de la creuse")
                                #with col2:
                                #        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Carte_r%C3%A9sultats_cantons_2015_Creuse.svg")
                                #        st.write("Cantons de la creuse")
                                #st.write ("VISUALISATION MARCHE DE LA CREUSE (page 4): https://www.cnc.fr/cinema/etudes-et-rapports/statistiques/datavisualisation-la-geographie-du-cinema")'''

                # CSS pour le style
                st.markdown(
                    """
                    <style>
                    .title {
                        font-size: 2em;
                        color: #2c3e50;
                        font-family: 'Arial', sans-serif;
                        margin-bottom: 20px;
                    }
                    .description {
                        font-size: 1.2em;
                        color: #444;
                        background-color: #f9f9f9;
                        padding: 15px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .details {
                        font-size: 1.1em;
                        color: #333;
                        margin-top: 10px;
                    }
                    .details strong {
                        color: #2c3e50;
                    }
                    .col-container {
                        display: flex;
                        justify-content: space-around;
                        margin-top: 20px;
                    }
                    .col {
                        flex: 1;
                        margin: 0 10px;
                    }
                    .image-container {
                        text-align: center;
                    }
                    .image-container img {
                        width: 100%;
                        border-radius: 10px;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .image-caption {
                        text-align: center;
                        font-size: 1em;
                        color: #666;
                        margin-top: 10px;
                    }
                    .link {
                        text-align: center;
                        margin-top: 30px;
                    }
                    .link a {
                        font-size: 1.1em;
                        color: #2c3e50;
                        text-decoration: none;
                    }
                    .link a:hover {
                        text-decoration: underline;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Contenu stylisé
                st.markdown('<h1 class="title">Bienvenue en Creuse</h1>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="description">
                        <strong>Description :</strong> 
                        La Creuse est un département français situé dans la région Nouvelle-Aquitaine et ayant appartenu, avant 2016, à la région Limousin avant la disparition de cette dernière. 
                        Il succède à la province de la Marche dont il reprend une grande partie du territoire.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="details">
                        <p><strong>Population :</strong> 115 702 hab. (2021)</p>
                        <p><strong>Capitale :</strong> Guéret</p>
                        <p><strong>Superficie :</strong> 5 565 km²</p>
                        <p><strong>Cantons :</strong> 15</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="col-container">
                        <div class="col">
                            <div class="image-container">
                                <img src="https://www.actualitix.com/wp-content/uploads/2017/05/ou-se-trouve-creuse.jpg" alt="Localisation de la Creuse">
                                <p class="image-caption">Localisation de la Creuse</p>
                            </div>
                        </div>
                        <div class="col">
                            <div class="image-container">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e4/Carte_r%C3%A9sultats_cantons_2015_Creuse.svg" alt="Cantons de la Creuse">
                                <p class="image-caption">Cantons de la Creuse</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="link">
                        <p>VISUALISATION MARCHE DE LA CREUSE (page 4): 
                        <a href="https://www.cnc.fr/cinema/etudes-et-rapports/statistiques/datavisualisation-la-geographie-du-cinema" target="_blank">https://www.cnc.fr/cinema/etudes-et-rapports/statistiques/datavisualisation-la-geographie-du-cinema</a>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
                
elif selection == "Recherche précise":
                st.image("https://img.freepik.com/photos-premium/clap-cinema-loupe-tableau-noir-craie-industrie-du-cinema-divertissement_175682-23332.jpg?w=740")

                st.write("**🎥 Bienvenue sur notre fabuleux moteur de recherche de films ! 🎥**")

                st.write("✨ Trouvez le Film de vos Rêves : Plongez dans le monde magique du cinéma avec notre moteur de recherche ! Vous pouvez utiliser un ou plusieurs filtres pour affiner votre quête cinématographique")
                
                st.write("Que vous souhaitiez utiliser ces filtres de manière indépendante, tel un ninja solitaire, ou les combiner pour une recherche encore plus précise, comme un maître Jedi du cinéma, tout est possible ! Vous cherchez une comédie romantique avec Ryan Gosling réalisée par Damien Chazelle ? Ou peut-être un film d'aventure dirigé par Peter Jackson ? Aucun problème, notre moteur est là pour vous.")
                
                st.write("Entrez vos préférences et laissez la magie opérer. Notre moteur de recherche est conçu pour vous guider vers le film parfait, que ce soit pour une soirée entre amis, un dimanche en famille, ou une session de cinéma en solo.")
                
                # Fonction pour charger les données
                @st.cache_data
                def load_data(file_path):
                    return pd.read_csv(file_path)

                # Chemin du fichier CSV
                csv_tmdb = 'https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv'
                df_ml_final= load_data(csv_tmdb)

                # Sélection du genre
                genre = st.selectbox("Sélectionner un genre", ["","Action", 'Adventure','Animation', 'Fantasy',"Drama", "Comedy","Crime","Thriller","Romance", "Music", "Science Fiction","War",'Western'])

                # Entrée utilisateur pour acteur/actrice et réalisateur/réalisatrice 
                acteur = st.text_input("Optionnel : Saisir un acteur/actrice de votre choix") 
                real = st.text_input("Optionnel : Saisir un réalisateur/réalisatrice de votre choix")
                film = st.text_input("Optionnel : Saisir un nom de film de votre choix")
               
                # Filtrer les films en fonction des inputs utilisateur 
                filtered_films = df_ml_final[df_ml_final['genres_x'].str.contains(genre, case=False, na=False)] 
                if acteur: 
                    filtered_films = filtered_films[filtered_films['cast'].str.contains(acteur, case=False, na=False)] 
                if real: 
                        filtered_films = filtered_films[filtered_films['director'].str.contains(real, case=False, na=False)]
                if film: 
                        filtered_films = filtered_films[filtered_films['title_y'].str.contains(film, case=False, na=False)]

                # Sélectionner les 3 films les mieux notés 
                top_10_films = filtered_films.sort_values(by='averageRating', ascending=False).head(10)
                
                # Afficher les suggestions de films
                st.subheader(" Suggestions de films")
                for index, row in top_10_films.iterrows() :

                    # Créer deux colonnes pour les boutons
                    col1, col2 = st.columns([1, 1]) 
                    with col1: 
                        if st.button(f"Déjà vu ♥️ ", key=f"vu_{index}"): 
                            film_vu(row) 
                    with col2: 
                        if st.button(f"À voir 👍", key=f"voir_{index}"): 
                            film_a_voir(row) 

                    col1, col2= st.columns([1, 2]) 
                    with col1:
                        st.image(row['poster_path']) 

                    with col2:
                        #affichage des vidéos 
                        try:  
                            st.video(row['key']) 
                             
                        except Exception as e: 
                            st.write("Video Indisponible")   #f"Erreur lors de la conversion et de l'affichage de la vidéo : {e}"

                    st.write(f"**{row['title_y']}** ({row['startYear']})")
                    st.write(f"**Synopsis** : {row['overview']}")
                    st.write(f"**Casting** : {row['cast']}")
                    st.write(f"**Réalisateur** : {row['director']}")
                    st.write(f":star: Note moyenne : {row['averageRating']}")
                    st.write(f":fire: Popularité : {row['popularity']}")

                    # Ajouter une barre horizontale  
                    st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)

elif selection == "Recommandations":
                ################################################################
                # RECOMMANDATION Mot cle
                st.image("https://www.ac-reunion.fr/sites/ac_reunion/files/styles/banner_1340x730/public/2022-01/daac-visuel-cin-ma-17078.jpg?itok=deYU8R3Z")
                st.write("**🔍 Rechercher par Mot-Clé** : Vous avez un mot en tête et vous espérez qu'il vous conduira à une perle cinématographique cachée ? Entrez votre mot-clé magique et regardez notre moteur travailler. C'est comme lancer une incantation, mais pour les films ! Par exemple, tapez 'super-héros' et attendez-vous à une avalanche de capes, de collants et de sauvetages de dernière minute. Et si vous tapez 'romance', préparez-vous à sortir vos mouchoirs. Bref, c'est votre baguette magique du cinéma !")

                # Liste de stopwords en français (vous pouvez personnaliser cette liste)
                stopwords_fr = ['le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'd\'', 'en', 'que', 'qui', 'à', 'dans', 'sur',
                                'pour', 'avec', 'sans', 'est', 'et', 'il', 'elle', 'ils', 'elles', 'nous', 'vous', 'ça', 'ce', 'ces']

                # Fonction pour charger les données
                @st.cache_data
                def load_data(file_path):
                    return pd.read_csv(file_path)

                # Chemin du fichier CSV
                csv_tmdb = 'https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv'
                df_ml_final= load_data(csv_tmdb)

                # Fonction pour trouver des films similaires
                def find_similar_movies(df, query, n_neighbors=10, threshold_distance=0.9):
                    # Utilisation de TfidfVectorizer avec les stopwords en français
                    vectorizer = TfidfVectorizer(stop_words=stopwords_fr)

                    # Transformation des résumés de films en vecteurs
                    X_tfidf = vectorizer.fit_transform(df['overview'])

                    # Entraînement du modèle NearestNeighbors pour trouver des films similaires
                    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
                    knn.fit(X_tfidf)

                    # Transformation du texte de la requête
                    query_tfidf = vectorizer.transform([query])

                    # Trouver les voisins les plus proches
                    distances, indices = knn.kneighbors(query_tfidf)

                    results = []
                    # Ajouter les films similaires trouvés à la liste des résultats
                    for idx, dist in zip(indices[0], distances[0]):
                        if dist < threshold_distance:
                            results.append({
                                'title_y': df.iloc[idx]['title_y'],  # Assurez-vous que cette clé est correcte
                                'Synopsis': df.iloc[idx]['overview'],
                                'Distance': dist,
                                'Affiche': df.iloc[idx]['poster_path'],
                                'Video': df.iloc[idx]['key'] # Ajoutez la clé des vidéos
                            })
                    
                    return results
                
                

                # Fonction principale de l'application Streamlit
                def main():
                    # Fonction pour charger les données
                    @st.cache_data
                    def load_data(file_path):
                        return pd.read_csv(file_path)

                    # Chemin du fichier CSV
                    csv_tmdb = 'https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv'
                    df_ml_final= load_data(csv_tmdb)

                    # Saisie du mot-clé par l'utilisateur 
                    mot_cle = st.text_input("**Saisir un mot-clé**") 
                    
                    # Exécuter la recherche si un mot-clé est saisi 
                    if mot_cle: 
                        resultats = find_similar_movies(df_ml_final, mot_cle) 
                        if resultats: 
                            st.write(f"Films correspondants au mot-clé '{mot_cle}':") 
                            for resultat in resultats: 
                                 
                                 # Créer deux colonnes pour les boutons
                                col1, col2 = st.columns([1, 1]) 
                                with col1: 
                                    if st.button(f"Déjà vu ♥️ ", key=f"vu_{resultat}"):  
                                        film_vu(resultat) 
                                with col2: 
                                    if st.button(f"À voir 👍", key=f"voir_{resultat}"): 
                                        film_a_voir(resultat) 
                                 # Diviser l'affichage en deux colonnes 
                                col1, col2 = st.columns([1, 2]) 
                                 
                                with col1: 
                                    st.image(resultat['Affiche']) 
                                     
                                with col2: 
                                        try:
                                            # Afficher directement la vidéo YouTube (sans transformation)
                                            if resultat['Video']:
                                                st.video(resultat['Video'])
                                            else:
                                                st.write("Vidéo Indisponible")
                                        except Exception as e:
                                            st.write("Vidéo Indisponible")
                                        
                                 #titre film
                                st.write(f"**Titre :** {resultat['title_y']}")

                                 #synopsis
                                st.write(f"**Synopsis :** {resultat['Synopsis']}") 
                                 
                                 # Ajouter une barre horizontale 
                                st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True) 
                        else: 
                             st.write(f"Aucun film similaire trouvé pour le mot-clé '{mot_cle}'.")

                if __name__ == "__main__":
                    main()

            ######################################################
            #RECOMMANDATION films
                st.write("**🍿 Rechercher par votre film préféré** : Vous avez un film fétiche que vous regardez en boucle, au point de connaître toutes les répliques par cœur ? Pas de souci, nous sommes là pour vous aider à découvrir d'autres trésors ! Indiquez-nous votre film préféré et nous trouverons des œuvres qui titilleront vos mêmes zones de plaisir cinématographique. Si vous aimez 'Inception', nous vous proposerons des films qui vous feront douter de la réalité. Et si 'La La Land' est votre truc, attendez-vous à chanter et danser dans votre salon. C'est comme si votre film préféré avait plein de petits cousins talentueux !")
                def recommend_movies_by_model(selected_title, df, feature_columns, top_n=10):
                        selected_title_lower = selected_title.lower()
                        similar_titles = df[df['title_y'].str.lower().str.contains(selected_title_lower)]
                        
                        if similar_titles.empty: 
                            return []
                        
                        selected_title = similar_titles.iloc[0]['title_y']
                        selected_genres = df[df['title_y'] == selected_title][[
                            'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
                            'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
                            'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']].iloc[0]
                        
                        # Créer une colonne binaire 'similar_to_selected' pour indiquer si un film est similaire au film sélectionné
                        df['similar_to_selected'] = df.apply(
                            lambda row: int(all(row[genre] == selected_genres[genre] for genre in selected_genres.index)),
                            axis=1
                        )

                        if df['similar_to_selected'].nunique() <= 1: 
                            return []


                        # Supprimer le film sélectionné du DataFrame
                        df_filtered = df[df['title_y'] != selected_title]
                        X = df_filtered[feature_columns]
                        y = df_filtered['similar_to_selected']
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                        
                        model = RandomForestClassifier(random_state=42)
                        

                        results = []
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        accuracy = accuracy_score(y_test, y_pred)
                        results.append({'Accuracy': accuracy, 'ModelObject': model})
                        results_df = pd.DataFrame(results).sort_values(by='Accuracy', ascending=False) 

                        df['predicted_similarity'] = model.predict(df[feature_columns])

                        # Trouver les films recommandés similaires au film sélectionné
                        recommended_movies = df[df['predicted_similarity'] == 1]['title_y'].tolist()
                        return recommended_movies[:top_n]
                        #'model_performance': results_df[['Model', 'Accuracy']]

                        
                # Fonction principale de l'application Streamlit
                def main1():
                            # Fonction pour charger les données
                            @st.cache_data
                            def load_data(file_path):
                                return pd.read_csv(file_path)

                            # Chemin du fichier CSV
                            csv_tmdb = 'https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv'
                            df_ml_final= load_data(csv_tmdb)
                            mlb = MultiLabelBinarizer()

                            #get dummies pour encoder le language
                            df_ml_final = pd.get_dummies(df_ml_final, columns=['original_language'])
                            df_ml_final[['original_language_en','original_language_fr']] = df_ml_final[['original_language_en','original_language_fr']].astype(int)
                            
                            #mlb pour encoder les genres
                            df_ml_final['genres_x'] = df_ml_final['genres_x'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                            genre_features = mlb.fit_transform(df_ml_final['genres_x'])
                            genre_feature_names = mlb.classes_
                            df_ml_final_genres_x = pd.DataFrame(genre_features, columns=genre_feature_names)
                            df_ml_final = pd.concat([df_ml_final, df_ml_final_genres_x], axis=1)

                            feature_columns = [
                        'startYear', 'runtimeMinutes', 'averageRating', 'numVotes',
                        'average_popularity_cast', 'average_popularity_director', 'popularity',
                        'original_language_en', 'original_language_fr', 'Action', 'Adventure',
                        'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                        'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
                        'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
                    ]
                            # Normalisation des colonnes numériques
                            scaler = StandardScaler()
                            df_ml_final[['runtimeMinutes', 'averageRating', 'numVotes', 'average_popularity_cast', 'average_popularity_director', 'popularity']] = scaler.fit_transform(df_ml_final[['runtimeMinutes', 'averageRating', 'numVotes', 'average_popularity_cast', 'average_popularity_director', 'popularity']])
                            
                            # Saisie du mot-clé par l'utilisateur
                            film = st.text_input("**Saisir le film de votre choix :** ")

                            # Exécuter la recherche si un mot-clé est saisi
                            if film:
                                resultats = recommend_movies_by_model(film, df_ml_final, feature_columns, top_n=5)
                                if resultats:
                                    st.write(f"Films similaires au film '{film}':")
                                    for titre in resultats:
                                        film_data = df_ml_final[df_ml_final['title_y'].str.lower() == titre.lower()].iloc[0]
                                        
                                        # Créer deux colonnes pour les boutons
                                        col1, col2 = st.columns([1, 1]) 
                                        with col1: 
                                            if st.button(f"Déjà vu ♥️ ", key=f"vu_{titre}"): 
                                                film_vu(film_data) 
                                        with col2: 
                                            if st.button(f"À voir 👍 ", key=f"voir_{titre}"): 
                                                film_a_voir(film_data) 
                                        # Diviser l'affichage en deux colonnes
                                        col1, col2 = st.columns([1, 2])
                                        with col1:
                                            st.image(film_data['poster_path'])
                                        with col2: 
                                            try:
                                                # Afficher directement la vidéo YouTube (sans transformation)
                                                if film_data['key']:
                                                    st.video(film_data['key'])
                                                else:
                                                    st.write("Vidéo Indisponible")
                                            except Exception as e:
                                                st.write("Vidéo Indisponible")
                                                
                                        #titre film
                                        st.write(f"**Titre :** {film_data['title_y']}")
                                        #synopsis
                                        st.write(f"**Synopsis :** {film_data['overview']}")
                                        # Ajouter une barre horizontale
                                        st.markdown("<hr style='border: 2px solid #F08080;'>", unsafe_allow_html=True)
                                else:
                                    st.write(f"Aucun film similaire trouvé pour le mot-clé '{film}'.")

                if __name__ == "__main__":
                    main1()


                # Fin de page sur le thème du cinéma
                footer_html = """
                <div style="background-color:#f8f9fa; padding:10px; border-top:2px solid #f08080;">
                    <center>
                        <img src="https://img.icons8.com/emoji/48/000000/popcorn-emoji.png" alt="Popcorn" style="margin-right: 10px;">
                        <img src="https://img.icons8.com/color/48/000000/clapperboard.png" alt="Clapperboard" style="margin-right: 10px;">
                        <img src="https://img.icons8.com/emoji/48/000000/film-frames-emoji.png" alt="Film Reels">
                        <h4 style="color:#343a40; margin-top:20px;">Merci d'avoir utiliser notre site de recommandations de films !</h4>
                        <h5 style="color:#343a40;">A bientôt dans nos salles </h5>
                        <p style="color:#6c757d;">Suivez-nous sur les réseaux sociaux pour plus de contenu cinématographique et informations de votre cinéma.</p>
                        <div>
                            <a href="https://www.facebook.com" style="margin-right:10px;"><img src="https://img.icons8.com/color/48/000000/facebook.png" alt="Facebook"></a>
                            <a href="https://www.twitter.com" style="margin-right:10px;"><img src="https://img.icons8.com/color/48/000000/twitter.png" alt="Twitter"></a>
                            <a href="https://www.instagram.com" style="margin-right:10px;"><img src="https://img.icons8.com/color/48/000000/instagram-new.png" alt="Instagram"></a>
                            <a href="https://www.youtube.com"><img src="https://img.icons8.com/color/48/000000/youtube.png" alt="YouTube"></a>
                        </div>
                    </center>
                </div>
                """
                st.markdown(footer_html, unsafe_allow_html=True)

elif selection == "Films vus ♥️":
    # Affichage des films vus
    st.title("Films déjà vus")
    df_ml_final= pd.read_csv('https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv')

    # Si la liste des films vus contient des films
    if st.session_state.viewed_movies:
        st.write("Voici les films que vous avez vus :")
        
        # Parcours de chaque titre de film dans la liste des films vus
        for movie_title in st.session_state.viewed_movies:
            # Recherche dans le DataFrame pour obtenir les détails du film
            movie = df_ml_final[df_ml_final['title_y'] == movie_title].iloc[0]  # Assurez-vous qu'il y a au moins un film trouvé
            
            # Utilisation de la mise en page avec 2 colonnes pour plus de clarté
            col1, col2= st.columns([1, 2]) 
            with col1:
                st.image(movie['poster_path']) 

            with col2:
                #affichage des vidéos 
                try:  
                    st.video(movie['key']) 
                             
                except Exception as e: 
                    st.write("Video Indisponible")   #f"Erreur lors de la conversion et de l'affichage de la vidéo : {e}"

            st.write(f"**{movie['title_y']}** ({movie['startYear']})")
            st.write(f"**Synopsis** : {movie['overview']}")
            st.write(f"**Casting** : {movie['cast']}")
            st.write(f"**Réalisateur** : {movie['director']}")
            st.write(f":star: Note moyenne : {movie['averageRating']}")
            st.write(f":fire: Popularité : {movie['popularity']}")
            
            st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)  # Séparation visuelle entre les films
    else:
        st.write("Vous n'avez pas encore marqué de films comme vus.")

elif selection == "Films à voir 👍":
    # Affichage des films à regarder
    st.title("Films à voir")
    df_ml_final= pd.read_csv('https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv')

    # Si la liste des films vus contient des films
    if st.session_state.list_movies:
        st.write("Voici les films que vous avez à voir :")
        
        # Parcours de chaque titre de film dans la liste des films vus
        for movie_title in st.session_state.list_movies:
            # Recherche dans le DataFrame pour obtenir les détails du film
            movie = df_ml_final[df_ml_final['title_y'] == movie_title].iloc[0]  # Assurez-vous qu'il y a au moins un film trouvé
            
            # Utilisation de la mise en page avec 2 colonnes pour plus de clarté
            col1, col2= st.columns([1, 2]) 
            with col1:
                st.image(movie['poster_path']) 

            with col2:
                #affichage des vidéos 
                try:  
                    st.video(movie['key']) 
                             
                except Exception as e: 
                    st.write("Video Indisponible")   #f"Erreur lors de la conversion et de l'affichage de la vidéo : {e}"

            st.write(f"**{movie['title_y']}** ({movie['startYear']})")
            st.write(f"**Synopsis** : {movie['overview']}")
            st.write(f"**Casting** : {movie['cast']}")
            st.write(f"**Réalisateur** : {movie['director']}")
            st.write(f":star: Note moyenne : {movie['averageRating']}")
            st.write(f":fire: Popularité : {movie['popularity']}")
            
            st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)  # Séparation visuelle entre les films
    else:
        st.write("Vous n'avez pas encore marqué de films dans votre liste à voir.")


elif selection == "KPI":
    # Chemin du fichier CSV
    df_ml_final= pd.read_csv('https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv')
    df_actor_pop = pd.read_csv('https://raw.githubusercontent.com/Gustaviche/MatchMyMovie/refs/heads/main/df_actor_actress_updated.csv')
    df_director_pop = pd.read_csv('https://raw.githubusercontent.com/Gustaviche/MatchMyMovie/refs/heads/main/director_popularities.csv')

        # Fonction générique pour afficher les entités (réalisateurs/acteurs) en lignes
    def display_entities_in_rows(top_entities, entity_key, photo_column):
        # Définir la répartition des entités par ligne
        entity_rows = [
            [top_entities.iloc[0]],  # Ligne 1 : Top 1
            [top_entities.iloc[1], top_entities.iloc[2]],  # Ligne 2 : Top 2 et 3
            [top_entities.iloc[3], top_entities.iloc[4], top_entities.iloc[5]],  # Ligne 3 : Top 4, 5, 6
            [top_entities.iloc[6], top_entities.iloc[7], top_entities.iloc[8], top_entities.iloc[9]],  # Ligne 4 : Top 7, 8, 9, 10
        ]

        for row in entity_rows:
            cols = st.columns(len(row))  # Créer une colonne par entité dans la ligne
            for i, entity in enumerate(row):
                with cols[i]:
                    # Vérifier si l'image existe
                    if pd.notna(entity[photo_column]):
                        st.markdown(
                            f"""
                            <div style="text-align: center;">
                                <img src="{entity[photo_column]}" alt="{entity[entity_key]}" width="150">
                                <p><strong>{entity[entity_key]}</strong></p>
                                <p>Nombre de films : {entity['number_of_movies']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="text-align: center;">
                                <p><strong>{entity[entity_key]}</strong></p>
                                <p>Image non disponible</p>
                                <p>Popularité totale : {entity['popularity']}</p>
                                <p>Nombre de films : {entity['number_of_movies']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    # Fonction pour calculer les Top 10 des réalisateurs/acteurs par popularité
    def get_top_10_entities_by_popularity(df, entity_key, photo_dict):
        # Grouper par l'entité (réalisateur ou acteur) et compter le nombre de films (lignes) et sommer la popularité
        grouped_entities = df.groupby(entity_key).agg({
            'popularity': 'sum',  # Somme de la popularité pour chaque entité
        }).reset_index()

        # Compter le nombre de films par entité (cela correspond au nombre de lignes par entité)
        grouped_entities['number_of_movies'] = df.groupby(entity_key).size().values
        
        # Trier par popularité décroissante
        top_entities = grouped_entities.sort_values(by='popularity', ascending=False).head(10)
        
        # Ajouter les URLs des photos
        top_entities['photo_url'] = top_entities[entity_key].map(photo_dict)
        
        return top_entities

    director_photos = {
                    "Steven Spielberg": "https://image.tmdb.org/t/p/w500/tZxcg19YQ3e8fJ0pOs7hjlnmmr6.jpg",
                    "Clint Eastwood": "https://image.tmdb.org/t/p/w500/dU35NnjZ4aGw5abIJe3WXVf3Eey.jpg",
                    "Quentin Tarantino": "https://image.tmdb.org/t/p/w500/1gjcpAa99FAOWGnrUvHEXXsRs7o.jpg",
                    "Ridley Scott": "https://image.tmdb.org/t/p/w500/zABJmN9opmqD4orWl3KSdCaSo7Q.jpg",
                    "Martin Scorsese": "https://image.tmdb.org/t/p/w500/mN49M9y74NZgMVKN35Qan5cfxrP.jpg",
                    "Christopher Nolan": "https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg",
                    "Tim Burton": "https://image.tmdb.org/t/p/w500/wcjuY5vD1nlfwWNbvvTGg5dGoRR.jpg",
                    "Sylvester Stallone": "https://image.tmdb.org/t/p/w500/gn3pDWthJqR0VDYGViGD3048og7.jpg",
                    "Ron Howard": "https://image.tmdb.org/t/p/w500/tDKn6gAgvARdQRfuem2JwyNcP3B.jpg",
                    "Robert Zemeckis": "https://image.tmdb.org/t/p/w500/lPYDQ5LYNJ12rJZENtyASmVZ1Ql.jpg",
                     }

    actor_photos = {
                    "Tom Hanks": "https://image.tmdb.org/t/p/w500/eKF1sGJRrZJbfBG1KirPt1cfNd3.jpg",
                    "Robert De Niro": "https://image.tmdb.org/t/p/w500/cT8htcckIuyI1Lqwt1CvD02ynTh.jpg",
                    "Chris Evans": "https://image.tmdb.org/t/p/w500/3bOGNsHlrswhyW79uvIHH1V43JI.jpg",
                    "Tom Cruise": "https://image.tmdb.org/t/p/w500/8qBylBsQf4llkGrWR3qAsOtOU8O.jpg",
                    "Hugh Jackman": "https://image.tmdb.org/t/p/w500/4Xujtewxqt6aU0Y81tsS9gkjizk.jpg",
                    "Robert Downey Jr.": "https://image.tmdb.org/t/p/w500/5qHNjhtjMD4YWH3UP0rm4tKwxCL.jpg",
                    "Matt Damon": "https://image.tmdb.org/t/p/w500/vgqgSZvrIrhY5yngVIg1R1KZQWQ.jpg",
                    "Samuel L. Jackson": "https://image.tmdb.org/t/p/w500/AiAYAqwpM5xmiFrAIeQvUXDCVvo.jpg",
                    "Mark Ruffalo": "https://image.tmdb.org/t/p/w500/5GilHMOt5PAQh6rlUKZzGmaKEI7.jpg",
                    "Chris Hemsworth": "https://image.tmdb.org/t/p/w500/u9Ovh0g3b9kqYjcydqW11PCv5DZ.jpg"
                     }

    # Streamlit - Interface
    st.title("Visualisation des KPI")

    option = st.selectbox("Sélectionnez la Visualisation", ("Top 10 Réalisateurs", "Top 10 Acteurs/Actrices","Nombre de Films par Année","Films les plus populaires par Année","Films les plus populaires par Genre"))

    if option == "Top 10 Réalisateurs":
        top_directors = get_top_10_entities_by_popularity(df_director_pop, 'director', director_photos)
        st.subheader("Top 10 Réalisateurs par Popularité")
        display_entities_in_rows(top_directors, 'director', 'photo_url')


        grouped_directors = df_director_pop.groupby('director').agg({ 
            'tconst': 'count',# Compter le nombre de films  
            'popularity': 'sum' # Calculer la popularité moyenne 
            }).reset_index() 
        grouped_directors.columns = ['director', 'number_of_movies', 'average_popularity'] 
        top_directors_by_popularity = grouped_directors.sort_values(by='average_popularity', ascending=False).head(10) 
        

    elif option == "Top 10 Acteurs/Actrices":
        top_actors = get_top_10_entities_by_popularity(df_actor_pop, 'actor_actress', actor_photos)
        st.subheader("Top 10 Acteurs/Actrices par Popularité")
        display_entities_in_rows(top_actors, 'actor_actress', 'photo_url')

        grouped_actors = df_actor_pop.groupby('actor_actress').agg({ 
            'tconst': 'count',# Compter le nombre de films  
            'popularity': 'sum' # Calculer la popularité moyenne 
            }).reset_index() 
        grouped_actors.columns = ['director', 'number_of_movies', 'average_popularity'] 
        top_actors_by_popularity = grouped_actors.sort_values(by='average_popularity', ascending=False).head(10) 
        

    elif option == 'Nombre de Films par Année':
                        df_ml_final= pd.read_csv('https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv')

                        # Sélection des critères par l'utilisateur
                        threshold = st.slider("Seuil de Note Moyenne (averageRating)", 0.0, 10.0, 7.5)
                        year_range = st.slider("Années", min_value=int(df_ml_final['startYear'].min()), max_value=int(df_ml_final['startYear'].max()), value=(2010, 2024))

                        # Filtrer les films selon le seuil et la plage d'années
                        filtered_films = df_ml_final[(df_ml_final['averageRating'] > threshold) & (df_ml_final['startYear'].between(year_range[0], year_range[1]))]

                        # Compter le nombre de films par année
                        films_per_year = filtered_films.groupby('startYear').size()

                        # Afficher les résultats
                        #st.write(f"Nombre de films par année avec une note supérieure à {threshold} entre {year_range[0]} et {year_range[1]}")
                        #st.write(films_per_year)

                        # Visualiser les résultats
                        fig, ax = plt.subplots(figsize=(12, 6))
                        sns.barplot(x=films_per_year.index, y=films_per_year.values, palette='viridis', ax=ax)
                        ax.set_title(f'Nombre de Films par Année à {threshold}')
                        ax.set_xlabel('Année')
                        ax.set_ylabel('Nombre de Films')
                        plt.xticks(rotation=45)

                        # Afficher le graphique dans Streamlit
                        st.pyplot(fig)

                        # Afficher la liste des films correspondant aux critères 
                        st.write(f"Liste des films avec une note supérieure à {threshold} entre {year_range[0]} et {year_range[1]}:") 

                        # Itérer sur les années et afficher les films correspondants 
                        for year in range(year_range[0], year_range[1] + 1): 
                            st.write(f"**Année {year}**:") 
                            films_of_year = filtered_films[filtered_films['startYear'] == year] 
                            for index, row in films_of_year.iterrows(): 
                                  st.write(f"- {row['title_y']} (Note: {row['averageRating']})")

    elif option == "Films les plus populaires par Année": 
                    
                    st.title("Top 10 Films les Plus Populaires")

                    # Laisser l'utilisateur choisir l'année
                    year_choice = st.slider("Choisissez une année", min_value=1960, max_value=2024, step=1)

                    # Filtrer les films de l'année choisie
                    df_filtered = df_ml_final[df_ml_final['startYear'] == year_choice]

                    # Trier les films par nombre de votes et sélectionner les 10 meilleurs
                    df_top10 = df_filtered.sort_values(by='averageRating', ascending=False).head(10)

                    # Afficher les posters des 10 films les plus populaires en 5 colonnes
                    st.write(f"Top 10 des films avec le plus de votes en {year_choice}")
                    cols = st.columns(5)

                    for i, row in enumerate(df_top10.iterrows()): 
                           with cols[i % 5]: st.image(row[1]['poster_path'], caption=row[1]['title_y']) 
                           # Séparer les lignes 
                           if i == 4: 
                                 cols = st.columns(5)
    elif option == "Films les plus populaires par Genre":  
        st.title("Top 10 par genre")
        # Chemin du fichier CSV
        csv_tmdb ='https://raw.githubusercontent.com/Melanie94480/Projet-2/refs/heads/Melanie/df_ml_final_v2_1812.csv'
        df_ml_final= pd.read_csv(csv_tmdb)
        genres =  ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "War", "Western"]
        genre = st.segmented_control("Choisissez un genre pour decouvrir les meilleurs films", genres)
        # Filtrer le DataFrame pour le genre sélectionné
        if genre:
            filtered_df = df_ml_final[df_ml_final['genres_x'].str.contains(genre, case=False, na=False)]
            # Trier les films par note moyenne et popularité
            sorted_df = filtered_df.sort_values(by=['averageRating', 'popularity'], ascending=[False, False])
            # Sélectionner les 10 meilleurs films
            top_10_films = sorted_df.head(10)
            # Vérifier si des films sont disponibles pour le genre sélectionné
            if top_10_films.empty:
                st.write(f"Aucun film trouvé pour le genre : **{genre}**.")
            else:
                st.write(f"### Top 10 des films : **{genre}**")
                for index, row in top_10_films.iterrows():
                # Afficher l'image et les informations sur le film
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        # Affichage de l'image du film
                        st.image(row['poster_path'], width=150)  # Lien de l'image
                    with col2:
                        # Informations sur le film
                        st.write(f"**{row['title_y']}** ({row['startYear']})")
                        st.write(f":star: Note moyenne : {row['averageRating']}")
                        st.write(f":fire: Popularité : {row['popularity']}")
                    st.markdown("---")

elif selection == "Propositions client":
        st.title("Conseils")
        # Mise en forme avec Markdown pour plus de clarté
        st.markdown("""
                ### 📝 Analyser des besoins et attentes des clients locaux
                - **Mettre en place un système pour recueillir les avis et suggestions des clients** afin d'améliorer constamment l'expérience.

                ### 🎬 Faciliter l'accès aux horaires des séances et à la réservation de billets en ligne
                - **Simplifier l'accès à la billetterie en ligne** et aux horaires des films, avec une interface fluide et accessible.

                ### 🎉 Promouvoir les événements spéciaux et les avant-premières
                - **Organiser des événements thématiques** autour de films populaires ou anniversaires de films cultes. Par exemple:
                - Soirées à thème telles que 'Classiques du cinéma' ou 'Marathons de films'.

                ### 🎁 Proposer un programme de fidélité
                - Offrir des **réductions pour les billets et collations**, en récompensant les visites régulières avec un système de points ou de réductions.

                ### 🤝 Collaborer avec des entreprises locales
                - **Offrir des réductions ou des offres combinées** avec des entreprises locales, comme une réduction pour un dîner dans un restaurant avant ou après la séance de cinéma.
                """)












