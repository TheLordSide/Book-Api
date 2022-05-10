#Importation des modules

from flask import Flask, jsonify, make_response, redirect, request,session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true
BookApi = Flask(__name__)

#configuration de la connexion a la base de donnee

BookApi.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:010296@localhost:5432/bookdb'
BookApi.config['SECRET_KEY']='MaCle'
BookApi.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(BookApi)


class Categories(db.Model):
   __tablename__='Categories'
   id = db.Column(db.Integer, primary_key=True)
   libelle_categorie = db.Column(db.String(10), nullable=False)
   livres=db.relationship('Livres', backref='Categories', lazy=True)
   def __init__(self,libelle_categorie):
        self.libelle_categorie=libelle_categorie
      
class Livres(db.Model):
   __tablename__='Livres'
   id = db.Column(db.Integer, primary_key=True)
   isbn = db.Column(db.String(13), nullable=False)
   titre = db.Column(db.String(30), nullable=False)
   date_publication = db.Column(db.Date(), nullable=False)
   auteur = db.Column(db.String(30), nullable=False)
   editeur = db.Column(db.String(30), nullable=False)
   categorie_id=db.Column(db.Integer, db.ForeignKey('Categories.id'),nullable=False)
   def __init__(self,isbn,titre,date_publication,auteur,editeur,categorie_id):
        self.isbn=isbn
        self.titre=titre
        self.date_publication=date_publication
        self.auteur=auteur
        self.editeur=editeur
        self.categorie_id=categorie_id

db.create_all()
 
#Ajout des routes 

#Route par defaut 
@BookApi.route('/', methods=['POST','GET'])
def index():
    return jsonify({"Notification":"Vous etes ici"})

#Route ajout de livre(Non specifiee dans l'exo)    

    

####################################################################################################################################################################
#
#
#
######## Delete categories
#
#
#
####################################################################################################################################################################



@BookApi.route('/book/deletecategorie/<int:idcat>', methods=['DELETE'])
def deletecategory(idcat):
    if request.method=='DELETE':
        requete= Categories.query.get(idcat)
        if not requete: 
            return jsonify({
                    'Notification':'la categorie que vous entrez est indisponible',
                    'Nombre de Categorie': len(Categories.query.all()),
                    'succes': False
                    })
        else:
            db.session.delete(requete)
            db.session.commit()
            return  jsonify({
                    'Notification':'Suppression effectuée correctement',
                    'Nombre de Categorie': len(Categories.query.all()),
                    'Categorie effacée': idcat,
                    'succes': True
                    })



####################################################################################################################################################################
#
#
#
######## Update a category
#
#
#
####################################################################################################################################################################


@BookApi.route('/book/updatecategory/<int:idcat>', methods=['PATCH'])
def updatecategory(idcat):
    if request.method=='PATCH':
        requete= Categories.query.get(idcat)
        if not requete: 
            return jsonify({
                    'Notification':'id entré est inexistant',
                    'succes': False
                    })
        else:
            Libellecat=request.json.get('Libelle')
            if not Libellecat:
                return jsonify({
                    'Notification':'Aucune valeur pour le libelle entree',
                    'succes': False  
                    })
            session['Libelle']=Libellecat
            requete2=Categories.query.filter(Categories.libelle_categorie==Libellecat).all()
            if requete2:
                return jsonify({
                    'Notification':'La categorie entrée existe déjà',
                    'Nombre de Categorie':len(Categories.query.all()),
                    'succes': False  
                    })
      
        if requete:
                    db.session.commit()
                    return jsonify({
                                'Notification':'enregistrement effectué',
                                'Nombre de Categorie':len(Categories.query.all()),
                                'succes': True    
                            })
                     
                 
        
            
          

  









####################################################################################################################################################################
#
#
#
######## Add categories
#
#
#
####################################################################################################################################################################

@BookApi.route('/book/addcategories', methods=['POST'])
def addcategories():

    if request.method=='POST':
        Libellecat=request.json.get('Libelle')
        if not Libellecat:
            return jsonify({
                'Notification':'Aucune valeur pour le libelle entree',
                'succes': False  
                })
        session['Libelle']=Libellecat
        requete=Categories.query.filter(Categories.libelle_categorie==Libellecat).all()
        if requete:
            return jsonify({
                'Notification':'La categorie entrée existe déjà',
                'Nombre de Categorie':len(Categories.query.all()),
                'succes': False  
                })
        else:
            if not requete:
                cat=Categories(Libellecat)
                db.session.add(cat)
                db.session.commit()
                return jsonify({
                    'Notification':'enregistrement effectué',
                    'Nombre de Categorie':len(Categories.query.all()),
                    'succes': True    
                })
    
 
####################################################################################################################################################################
#
#
#
######## Show all Categories
#
#
#
####################################################################################################################################################################
                
@BookApi.route('/book/showallcategories', methods=['GET'])
def showallcategories():
        
        requete= Categories.query.all()
        categoriearray=[]
        for row in requete:
            requestObj={}
            requestObj['id']=row.id
            requestObj['libelle']=row.libelle_categorie
            categoriearray.append(requestObj)
        if not categoriearray:
            return jsonify({
                'Notification':'Aucune categorie disponible',
                'Nombre de categories':len(requete),
                'succes': False,
                })  
        else:
            if categoriearray:
                return jsonify({
                    'Nombre de categories':len(requete),
                    'Listecategorie' : categoriearray,
                    'succes': True
                    })
                


####################################################################################################################################################################
#
#
#
######## Show categories by ID
#
#
#
####################################################################################################################################################################                
            
            
@BookApi.route('/book/showallcategories/<int:idcat>', methods=['GET']) 
def showonecat(idcat):
        requete= Categories.query.filter(Categories.id==idcat).all()
        if not requete:
           return jsonify({
               'Notification' : 'Aucune categorie ne correspond au id entree',
               'succes': False
               }) 
        categoriearray=[]
        for row in requete:
            requestObj={}
            requestObj['id']=row.id
            requestObj['libelle']=row.libelle_categorie
            categoriearray.append(requestObj)
        if not categoriearray:
              return jsonify({
               'Notification' : 'Aucune categorie ne correspond au id entree',
               'succes': False
               })  
        else:
            if categoriearray:
                return jsonify({'Listecategorie' : categoriearray})          

                    
####################################################################################################################################################################
#
#
#
######## Show all books
#
#
#
####################################################################################################################################################################   
@BookApi.route('/book/showbooklist', methods=['GET'])
def showbooklist():
     requete= Livres.query.all()
     Livrearray=[]
     for row in requete:
            requestObj={}
            requestObj['id']=row.id
            requestObj['isbn']=row.isbn
            requestObj['titre']=row.titre
            requestObj['date_publication']=row.date_publication
            requestObj['auteur']=row.auteur
            requestObj['editeur']=row.editeur
            requestObj['categorie_id']=row.categorie_id
            Livrearray.append(requestObj)
     if not Livrearray:
            return jsonify({
                'Notification':'Aucun livre enregistré',
                'Nombre de livres':len(requete),
                'succes': False
                })  
     else:
            if Livrearray:
                return jsonify({
                    'Nombre de livres':len(requete),
                    'Listecategorie' : Livrearray,
                    'succes': True
                    })



####################################################################################################################################################################
#
#
#
######## Show all books
#
#
#
####################################################################################################################################################################   

@BookApi.route('/book/addbooks', methods=['POST'])
def addbooks():
    if request.method=='POST':
        isbn=request.json.get('isbn')
        titre=request.json.get('titre')
        date_publication=request.json.get('date_publication')
        auteur=request.json.get('auteur')
        editeur=request.json.get('editeur')
        categorieid=request.json.get('idcategorie')
        requete=Categories.query.filter(Categories.id==categorieid).all()
        if not requete:
             return jsonify({
                 'Notification':'la categorie que vous entrez est indisponible',
                 'succes': False
                 })
        else:
            session['isbn']=isbn
            session['titre']=titre
            session['date_publication']=date_publication
            session['auteur']=auteur
            session['editeur']=editeur
            session['idcategorie']=categorieid
            livre=Livres(isbn,titre,date_publication,auteur,editeur,categorieid)
            db.session.add(livre)
            db.session.commit()
            return jsonify({
                'Notification':'enregistrement effectué',
                'Nombre de Livres':len(Livres.query.all()),
                'succes': True
                })

#Ajout de l'option debug
if __name__=="__name__":
    BookApi.run(debug=True)
   
   
      