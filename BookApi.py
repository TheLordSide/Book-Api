#Importation des modules

from ast import Try
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
     try:
        if request.method=='DELETE':
                requete= Categories.query.get(idcat)
        if not requete: 
            return jsonify({
                    'Error':'la categorie que vous entrez est indisponible',
                    'Nombre de Categorie': len(Categories.query.all()),
                    'success': False
                    })
        else:
            db.session.delete(requete)
            db.session.commit()
            return  jsonify({
                    'Response':'Suppression effectuée correctement',
                    'Nombre de Categories': len(Categories.query.all()),
                    'Categorie effacée': idcat,
                    'success': True
                    })
        
     except:  
            abort(405)
    



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
   try:
        if request.method=='PATCH':
            requete= Categories.query.get(idcat)
        if not requete: 
            return jsonify({
                    'Error':'id entré est inexistant',
                    'success': False
                    })
        else:
            requete.libelle_categorie = request.json.get('libelle_categorie')
            if requete.libelle_categorie == "":
                  return jsonify({
                                'Error':'Aucune categorie entree',
                                'success': False
                                })
            else:
                db.session.commit()
                return jsonify({
                                'Response':'Modifie avec succes',
                                'id categorie moodifiee':idcat,
                                'Nombre de Categories': len(Categories.query.all()),
                                'success': True
                                })
   except:
             abort(405)


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
    try:
        if request.method=='POST':
            Libellecat=request.json.get('libelle_categorie')
        if not Libellecat:
            return jsonify({
                'Error':'Aucune valeur entree',
                'success': False  
                })
        session['Libelle']=Libellecat
        requete=Categories.query.filter(Categories.libelle_categorie==Libellecat).all()
        if requete:
            return jsonify({
                'Erreur':'La categorie entrée existe déjà',
                'success': False  
                })
        else:
            if not requete:
                cat=Categories(Libellecat)
                db.session.add(cat)
                db.session.commit()
                return jsonify({
                    'Response':'enregistrement effectué',
                    'Nombre de Categorie':len(Categories.query.all()),
                    'success': True    
                })
    except:
        abort(405)
    
 
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
                requestObj['libelle_categorie']=row.libelle_categorie
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
      try:
        requete= Categories.query.filter(Categories.id==idcat).all()
        if not requete:
           return jsonify({
               'Error' : 'Aucune categorie ne correspond au id entree',
               'success': False
               }) 
        categoriearray=[]
        for row in requete:
            requestObj={}
            requestObj['id']=row.id
            requestObj['libelle']=row.libelle_categorie
            categoriearray.append(requestObj)
        if not categoriearray:
              return jsonify({
               'Error' : 'Aucune categorie ne correspond au id entree',
               'success': False
               })  
        else:
            if categoriearray:
                return jsonify({
                    'Listecategorie' : categoriearray,
                    'Nombre de categories':len(Categories.query.all()),
                    'Id recherche': idcat,
                    'success': True
                    })         
      except: 
                abort(405)
                    
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
    try:
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
                'Erreur':'Aucun livre enregistré',
                'Nombre de livres':len(requete),
                'success': False
                })  
     else:
            if Livrearray:
                return jsonify({
                    'Nombre de livres':len(requete),
                    'Liste de livres' : Livrearray,
                    'success': True
                    })
    except:
            abort(405)

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
    try:
     requete= Livres.query.filter(Livres.id==idlivre).all()
     if not requete:
           return jsonify({
               'Erreur' : 'Aucun Livre ne correspond au id entré',
               'success': False
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
                'Erreur':'Aucun livre enregistré',
                'Nombre de livres':len(requete),
                'success': False
                })  
     else:
            if Livrearray:
                return jsonify({
                    'Id recherché' : idlivre,
                    'Liste de Livres' : Livrearray,
                    'success': True
                    })
    except:
             abort(405)



####################################################################################################################################################################
#
#
#
######## Show books by id cat
#
#
####################################################################################################################################################################

@BookApi.route('/book/showbooklist/<int:idcat>', methods=['GET'])
def showbookbyidcat(idcat):
    try:
     requete= Livres.query.filter(Categories.id==idcat).all()
     if not requete:
           return jsonify({
               'Erreur' : 'Aucun Livre ne correspond au id entré',
               'success': False
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
                'Erreur':'Aucun livre enregistré',
                'Nombre de livres':len(requete),
                'success': False
                })  
     else:
            if Livrearray:
                return jsonify({
                    'Id recherché' : idcat,
                    'Liste de LIvres' : Livrearray,
                    'success': True
                    })
    except:
             abort(405)







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
        try:
            if request.method=='POST':
                isbn=request.json.get('isbn')
                titre=request.json.get('titre')
                date_publication=request.json.get('date_publication')
                auteur=request.json.get('auteur')
                editeur=request.json.get('editeur')
                categorieid=request.json.get('idcategorie')
                requete=Categories.query.filter(Categories.id==categorieid).all()
                if isbn == "" and date_publication == "" and auteur == "" and titre == "" and editeur == "" and categorieid == "" :
                            return jsonify({
                                "Success": False,
                                "Error": "Vos champs sont vides !"
                            })
                if not requete:
                    return jsonify({
                        'Error':'la categorie que vous entrez est indisponible',
                        'succes': False
                        })
                else:    
                    rqt = Livres.query.filter(
                            Livres.isbn == isbn, Livres.date_publication == date_publication).all()
                    if rqt:
                            return jsonify({
                                "Success": False,
                                "Error": "Le code isbn existe déjà !"
                            })
                            
                    elif not rqt:
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
                            'Response':'enregistrement effectué',
                            'Nombre de Livres':len(Livres.query.all()),
                            'success': True
                            })

        except:
                 abort(405)
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
    try:
        if request.method=='DELETE':
            requete= Livres.query.get(idlivre)
        if not requete: 
            return jsonify({
                    'Error':'le livre que vous entrez est indisponible',
                    'success': False
                    })
        else:
            db.session.delete(requete)
            db.session.commit()
            return  jsonify({
                    'Response':'Suppression effectuée correctement',
                    'Nombre de Livres': len(Livres.query.all()),
                    'Livre effacé': idlivre,
                    'success': True
                    })
    except:
            abort(405)




####################################################################################################################################################################
#
#
#
######## Update a book by ID
#
#
#
#################################################################################################################################################################### 

@BookApi.route('/book/updatebook/<int:id>', methods=['PATCH'])
def updatebook(id):
    try:
        if request.method=='PATCH':
            requete= Livres.query.get(id)
        if not requete: 
            return jsonify({
                    'Error':'id entré est inexistant',
                    'success': False
                    })
               
        else:
            requete.isbn = request.json.get('isbn')
            requete.titre= request.json.get('titre')
            requete.date_publication= request.json.get('date_publication')
            requete.auteur= request.json.get('auteur')
            requete.editeur= request.json.get('editeur')
            requete.categorie_id= request.json.get('categorie_id')
            
            if requete.isbn == "" and requete.date_publication == "" and requete.titre == "" and requete.auteur == "" and requete.editeur == "" and requete.categorie_id == "" :
                            return jsonify({
                                "Success": False,
                                "Error": "Vos champs sont vides !"
                            })
            db.session.commit()
            return jsonify({
                                'Response':'Modifie avec succes',
                                'id categorie moodifiee':id,
                                'Nombre de Livres': len(Livres.query.all()),
                                'success': True
                                })
    except:
             abort(405)
        




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
    
         

@BookApi.errorhandler(405)
def page_not_found(e):
    return jsonify({
        "succes":False,
        "response":"Method not allowed",
    })
    

if __name__=="__name__":
    BookApi.run(debug=True)
   
   
      