#Importation des modules

from os import abort
from flask import Flask, jsonify, make_response, redirect, request,session, url_for,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
BookApi = Flask(__name__)


BookApi.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:010296@localhost:5432/bookdb'
BookApi.config['SECRET_KEY']='MaCle'
BookApi.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(BookApi)


class Categories(db.Model):
   __tablename__='Categories'
   id = db.Column(db.Integer, primary_key=True)
   libelle_categorie = db.Column(db.String(50), nullable=False)
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
            requete.libelle_categorie = request.json.get('libelle_categorie')
            if requete.libelle_categorie == "":
                  return jsonify({
                                'Notification':'Aucune categorie entree',
                                'succes': False
                                })
            else:
                db.session.commit()
                return jsonify({
                                'Notification':'Modifie avec succes',
                                'id categorie moodifiee':idcat,
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
        Libellecat=request.json.get('libelle_categorie')
        if not Libellecat:
            return jsonify({
                'Error':'Aucune valeur entree',
                'succes': False  
                })
        session['Libelle']=Libellecat
        requete=Categories.query.filter(Categories.libelle_categorie==Libellecat).all()
        if requete:
            return jsonify({
                'Erreur':'La categorie entrée existe déjà',
                'succes': False  
                })
        else:
            if not requete:
                cat=Categories(Libellecat)
                db.session.add(cat)
                db.session.commit()
                return jsonify({
                    'Response':'enregistrement effectué',
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
    try:
        if request.method=='GET':   
            requete= Categories.query.all()
            categoriearray=[]
            for row in requete:
                requestObj={}
                requestObj['id']=row.id
                requestObj['libelle']=row.libelle_categorie
                categoriearray.append(requestObj)
            if not categoriearray:
                return jsonify({
                    'Error':'Aucune categorie disponible',
                    'Nombre de categories':len(requete),
                    'success': False,
                    })  
            else:
                if categoriearray:
                    return jsonify({
                        'Nombre de categories':len(requete),
                        'Liste de categories' : categoriearray,
                        'success': True
                        })
    except:
        abort(405)
                


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
               'Error' : 'Aucune categorie ne correspond au id entree',
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
######## Show books by id
#
#
#
####################################################################################################################################################################   


@BookApi.route('/book/showbooklist/<int:idlivre>', methods=['GET'])
def showbookbyid(idlivre):
     requete= Livres.query.filter(Livres.id==idlivre).all()
     if not requete:
           return jsonify({
               'Notification' : 'Aucun Livre ne correspond au id entré',
               'succes': False
               }) 
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
                    'Id recherché' : idlivre,
                    'Listecategorie' : Livrearray,
                    'succes': True
                    })


####################################################################################################################################################################
#
#
#
######## Add books
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

 
####################################################################################################################################################################
#
#
#
######## Delete book by ID
#
#
#
####################################################################################################################################################################    
    
@BookApi.route('/book/deletebook/<int:idlivre>', methods=['DELETE'])
def deletebook(idlivre):
    if request.method=='DELETE':
        requete= Livres.query.get(idlivre)
        if not requete: 
            return jsonify({
                    'Notification':'le livre que vous entrez est indisponible',
                    'succes': False
                    })
        else:
            db.session.delete(requete)
            db.session.commit()
            return  jsonify({
                    'Notification':'Suppression effectuée correctement',
                    'Nombre de Livres': len(Livres.query.all()),
                    'Livre effacé': idlivre,
                    'succes': True
                    })





####################################################################################################################################################################
#
#
#
######## Update a book by ID
#
#
#
#################################################################################################################################################################### 

@BookApi.route('/book/updatebook/<int:idbook>', methods=['PATCH'])
def updatebook(idbook):
    if request.method=='PATCH':
        requete= Livres.query.get(idbook)
        if not requete: 
            return jsonify({
                    'Notification':'id entré est inexistant',
                    'succes': False
                    })
        else:
            requete.isbn = request.json.get('isbn')
            requete.titre = request.json.get('titre')
            requete.date_publication = request.json.get('date_publication')
            requete.auteur = request.json.get('auteur')
            requete.editeur = request.json.get('editeur')
            requete.categorie_id = request.json.get('categorie_id')
            db.session.commit()
            return jsonify({
                                'Notification':'Modifie avec succes',
                                'id categorie moodifiee':idbook,
                                'succes': True
                                })
      











####################################################################################################################################################################
#
#
#
#Error handling
#
#
#
####################################################################################################################################################################


@BookApi.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "succes":False,
        "response":"Ressource not found",
    })
    
    
@BookApi.errorhandler(400)
def page_not_found(e):
    return jsonify({
        "succes":False,
        "response":"Bad request",
    })
        

@BookApi.errorhandler(405)
def page_not_found(e):
    return jsonify({
        "succes":False,
        "response":"Method not allowed",
    })
    

if __name__=="__name__":
    BookApi.run(debug=True)
   
   
      