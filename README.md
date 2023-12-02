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
```
./manage.py test
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
 - [ ] display error on HTMX
 - [ ] use indicator while saving ingredient
 - [ ] clean step after form sent
 - [ ] use poetry
 - [ ] Delete Recipe/Article
 - [ ] add pagination(https://realpython.com/django-pagination/), https://htmx.org/examples/infinite-scroll/
 - [ ] add default image for article and recipe
 - [ ] rework on the slug system
 - [ ] add trigram for search
 - [ ] make author page
 - [ ] add advertising for make cash
 - [ ] add crypto reward [BAT,Polygon,NFTL]
 - [ ] Bio -> text area
 - [ ] Tests!!!!!
 - [ ] export pdf
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