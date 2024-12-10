# installer dans powershell : pip install streamlit-authenticator
# installer dans powershell : pip install streamlit-option-menu

import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

# Nos données utilisateurs doivent respecter ce format

lesDonneesDesComptes = {'usernames': {'utilisateur': {'name': 'utilisateur',
   'password': 'utilisateurMDP',
   'email': 'utilisateur@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'utilisateur'},
  'root': {'name': 'root',
   'password': 'rootMDP',
   'email': 'admin@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'administrateur'}}}

authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)

authenticator.login()
#créer le bouton deconnexion dans la barre latérale
with st.sidebar :
    if st.session_state["authentication_status"]:
    # Le bouton de déconnexion
     authenticator.logout("Déconnexion")
     st.write('Bienvenue: Melanie')

# Créer le menu dans la barre latérale
if st.session_state["authentication_status"]:
    with st.sidebar:
        selection = option_menu(
            menu_title=None,  # Pas de titre de menu
            options=["Accueil", "Presentation Client" , "Etude de marché" , "Equipe", "Recommandations films", "KPI", "Problèmes rencontrés","Recommandations/ suggestions client"]
    )


if st.session_state["authentication_status"]:
    # On indique au programme quoi faire en fonction du choix
    if selection == "Accueil":
                st.title("Wild code school : Projet 2 ")
                st.image("https://th.bing.com/th/id/R.7e9183f95a1237eed74b6e911f4aa030?rik=6FRjaPSeXY2pUw&riu=http%3a%2f%2fmariepierrem.m.a.pic.centerblog.net%2ffv5s7fd8s6.png&ehk=LJjgr%2bndWf9891%2bDJgWc5f5Gm9ckXgW4Q6RAZC%2b0c%2fA%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1")
                col1, col2 ,col3, col4 = st.columns(4)
                with col1:
                    st.image("https://image.tmdb.org/t/p/original/v0dj9NVPFTX0bv5NtqxK99i1Ae3.jpg") #Mission: Impossible - Rogue Nation 
                    st.image("https://image.tmdb.org/t/p/original/sNL1aPGCMFmcnNDFWVUKehO3Vjr.jpg") #OSS 117 : Rio ne répond plus
                    #st.image("https://image.tmdb.org/t/p/original/vlLW4BPPS6XL8mxAvoJSppJV3Sv.jpg")      #101 dalmatiens
                    st.image("https://image.tmdb.org/t/p/original/dfht1lGq2ALbrRkMj35dUrj5kHG.jpg")  #Bienvenue chez les Ch'tis
                with col2:
                    st.image("https://image.tmdb.org/t/p/original/smFyhZHuOCZEmH0kfXOrJLC3Acx.jpg") #Toy Story 4 
                    st.image("https://image.tmdb.org/t/p/original/yJm61MmTMjOmNXxPxdoaIkdqnOm.jpg") # Harry Potter and the Deathly Hallows
                    #st.image("https://image.tmdb.org/t/p/original/rNr3W7GuSpIRjuSr0TM6vSTrIdx.jpg") #west side story
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
                st.title("Presentation client")
                st.write("Un cinéma situé dans la Creuse constate une baisse de fréquentation et souhaite moderniser son approche pour attirer et fidéliser une clientèle locale. Le projet consiste à développer un site Internet dédié aux habitants de la région et à mettre en place un moteur de recommandations de films, capable de communiquer avec les clients.")
                st.video("https://www.youtube.com/watch?v=6ocJK8jQ6sI")
    
    elif selection == "Etude de marché":
                st.title("Etude de marché")
                st.write("Description :")
                st.write("La Creuse est un département français situé dans la région Nouvelle-Aquitaine et ayant appartenu, avant 2016, à la région Limousin avant la disparition de cette dernière. Il succède à la province de la Marche dont il reprend une grande partie du territoire.")
                st.write("Population : 115 702 hab. (2021)")
                st.write("Capitale : Guéret")
                st.write("Superficie : 5 565 km²")
                st.write("Cantons : 15")
        
                col1, col2 = st.columns(2)
                with col1:
                        st.image("https://www.actualitix.com/wp-content/uploads/2017/05/ou-se-trouve-creuse.jpg")
                        st.write("Localisation de la creuse")
                with col2:
                        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Carte_r%C3%A9sultats_cantons_2015_Creuse.svg")
                        st.write("Cantons de la creuse")
                st.write ("VISUALISATION MARCHE DE LA CREUSE (page 4): https://www.cnc.fr/cinema/etudes-et-rapports/statistiques/datavisualisation-la-geographie-du-cinema")

    elif selection == "Equipe":
                st.title("Bienvenue sur ma page")
                col1, col2 = st.columns(2)
                with col1:
                        st.image("https://attic.sh/n7dvxa4xl5bi9pwtg9ntmqhq101b")
                        st.write("Yasmina : Scrum Master")
                        st.image("https://static.tiktokemoji.com/202411/15/x20t8eUr.webp")
                        st.write("Mariétou : Team Member")
                       
                with col2:
                        st.image("https://attic.sh/471qrlom5chx5d65jzw748f3ucf4")
                        st.write("Alexandre : Team Member")
                        st.image("https://attic.sh/78097cw049dbfkjq74trr3gafah0")
                        st.write("Mélanie : Product Owner")#st.image("https://attic.sh/99t8n9w34y6ekmwewzxwk3lx4jbk" )
                
                                   
    elif selection == "Recommandations films":
                st.title("Bienvenue sur ma page")
                st.image("https://th.bing.com/th/id/OIP.eUjoOLdCIHEWmWMpAh2gtwHaEK?rs=1&pid=ImgDetMain")
    
    elif selection == "KPI":
                st.title("Bienvenue sur ma page")
                st.image("https://th.bing.com/th/id/OIP.eUjoOLdCIHEWmWMpAh2gtwHaEK?rs=1&pid=ImgDetMain")
                col1, col2, col3 = st.columns(3)
                with col1:
                        st.image("https://www.starnimo.com/wp-content/uploads/2020/12/chaton-mignon-roux-821x1536.jpg")
                    
                        st.write("Mon chat bébé")
                with col2:
                        st.image("https://th.bing.com/th/id/OIP.t7n2xUAuM3dLpAlvM2rH3wHaEv?rs=1&pid=ImgDetMain")
                        st.write("Le chat en mode détente")
                with col3:
                        st.image("https://th.bing.com/th/id/OIP.eUjoOLdCIHEWmWMpAh2gtwHaEK?rs=1&pid=ImgDetMain")
                        st.write("Mon chat entrain de reviser les cours de machine learning")

    elif selection == "Recommandations/ suggestions client":
                st.title("Conseils")
                st.image("https://th.bing.com/th/id/OIP.eUjoOLdCIHEWmWMpAh2gtwHaEK?rs=1&pid=ImgDetMain")
                st.write("- Analyse des besoins et des attentes des clients locaux.")
                st.write("- Faciliter l'accès aux horaires des séances et à la réservation de billets en ligne.")
                st.write("- Promouvoir les événements spéciaux et les avant-premières.")

                                                                                                            

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')


