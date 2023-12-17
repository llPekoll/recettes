# Recette


## traductions
```
./manage.py makemessages --all
./manage.py compilemessages
```
## Run tailwind
```
./manage.py tailwind start
```
## Run test
code gen
```
playwright codegen localhost:8000
```
run test
```
pytest -s
```


## Lint
```
isort app/
black app/
bandit app/
flake8 app/
# cli version
isort app/;black app/;bandit app/;flake8 app/
```


## Cool Stuff
https://codepen.io/nailaahmad/pen/MyZXVE

autocomplete
https://codepen.io/mrcodebox33/pen/OJaGrra



## TODO 
 - [~] indicator for create Recipe Article
 - [ ] test on edit article
 - [ ] test on comment
 - [ ] test on edit bio
 - [ ] test on search
 - [ ] display error on HTMX
 - [ ] use poetry
 - [ ] add trigram for search
 - [ ] make author page
 - [ ] add advertising for make cash
 - [ ] add crypto reward [BAT,Polygon,NFTL]
 - [ ] Bio -> Quill
 - [ ] export pdf
 
 - [x] install versatile image
 - [x] faire le footer RGPD etc.... 
 - [x] make a component from comment
 - [x] test on edit recipe
 - [x] add pagination(https://realpython.com/django-pagination/), https://htmx.org/examples/infinite-scroll/
 - [x] add default image for article and recipe
 - [x] rework on the slug system
 - [x] use indicator also on regular form
 - [x] use indicator on HTMX
 - [x] clean step after form sent
 - [x] clear step after submit and display if no title
 - [x] component star system
 - [x] Delete Recipe/Article
 - [x] Tests!!!!!
 - [x] faire un model link pour rajouter a instruction
 - [x] faire des instructions step!
 - [x] Ajouter un quill pour les comment
 - [x] Reduce Search bar
 - [x] mettre les fichier static pour quill plutot que des CDN


# ChangeLog
### V 0.01
  
 - install minio, 
 - Edit profile pricture, 
 - Add recipie picture
 - Blog
 - move article to an serparated app
 - clean template mess -> use componenent directory
 - add tags
 - Edit Articles
 - add publish for articles too
 - Report Report
 - add auto suggestion for tag
 - Edit Recipes
 - make search better
 - Django pictures

## Recipe 

 we can create recipe from ingredient or from the form


 ## Misc link
 https://codepen.io/KaioRocha/pen/YoEVvZ
 https://codepen.io/alvarotrigo/pen/PoKMyWE
 https://www.fontpair.co/all