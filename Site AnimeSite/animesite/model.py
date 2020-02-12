from animesite import db,login_manager,app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(20),unique = True, nullable = False)
    email = db.Column(db.String(120),unique = True, nullable = False)
    foto_perfil = db.Column(db.String(40), nullable = False, default = "default.jpg")
    senha =  db.Column(db.String(40), nullable = False)
    posts = db.relationship('Postagem', backref = 'autor', lazy = True)
    comentarios = db.relationship('Comentario', backref = 'autor', lazy = True)
    administrador=db.Column(db.Boolean, nullable=False, default=False)

    def get_token_usuario(self, tempo_validade=2000):
        serial = Serializer(app.config['SECRET_KEY'],tempo_validade)
        return serial.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def validate_token_usuario(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)

    def __repr__(self):
        return f"Usuario('{self.nome}', '{self.email}','{self.foto_perfil}')"

#usuario = model.Usuario(nome="Sandy",email="manglesan98@gmail.com",senha="123",administrador=True)

class Postagem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(40), nullable = False)
    data_postada = db.Column(db.DateTime, nullable = False,default = datetime.utcnow)
    conteudo = db.Column(db.Text,nullable = False)
    imagem_postagem = db.Column(db.String(40), nullable = True)
    avaliação=db.Column(db.Integer,nullable=True)
    media=db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    comentario=db.relationship('Comentario', backref = 'Postagem', lazy = True)
    def __repr__(self):
        return f"Post('{self.titulo}','{self.conteudo}','{self.imagem_postagem}', '{self.data_postada}','{self.comentario}',{self.media})"

class Comentario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comentario_id=db.Column(db.Integer,db.ForeignKey('postagem.id'))
    conteudo_comentario=db.Column(db.String(120),nullable = False)
    autor_id=db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    def __repr__(self):
        return f"Comentario('{self.comentario_id}', '{self.conteudo_comentario}','{self.autor_id}')"

class Avaliacao(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    postagem_id=db.Column(db.Integer,db.ForeignKey('postagem.id'))
    num_recebido=db.Column(db.Integer)
    autor_id=db.Column(db.Integer,db.ForeignKey('usuario.id'))
    def __repr__(self):
        return f"Avaliacao('{self.postagem_id}', '{self.num_recebido}','{self.autor_id}')"              
db.create_all()