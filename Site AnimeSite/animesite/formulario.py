from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,RadioField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from animesite.model import Usuario
from flask_login import current_user
from animesite.model import Postagem


class MensagemErroForm(object):
    def __init__(self,min=1,max=120):
        self.min=min
        self.max=max
    def mensagem_tamanho(self,min,max):
        mensagem = "O campo deve ter de "+str(min)+" até "+str(max)+" caracteres."
        return mensagem
    def mensagem_email_invalido(self):
        mensagem = "O Email digitado não é válido, por favor tente novamente!"
        return mensagem
    def mensagem_confirmacao_senha(self):
        mensagem = "As senhas não batem."
        return mensagem
    def mensagem_formatoimg(self):
        mensagem = "O formato da imagem mandada não é compatível."
        return mensagem

funcao_validacao=MensagemErroForm()

class RegistroForm(FlaskForm):
    def validate_nome_usuario(self,nome):
        nome = Usuario.query.filter_by(nome=nome.data).first()
        if nome:
            raise ValidationError('O nome citado já foi utilizado. Por favor escolha outro!')
            user=None

    def validate_email_usuario(self,email):
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('O email citado já foi utilizado. Por favor escolha outro!')
            user=None
    nome = StringField('Nome_do_Usuario',validators=[DataRequired(),Length(2,15,message=funcao_validacao.mensagem_tamanho(2,15)),validate_nome_usuario])
    email = StringField('Email',validators =[DataRequired(), Email(message=funcao_validacao.mensagem_email_invalido()),validate_email_usuario])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(2,15,message=funcao_validacao.mensagem_tamanho(2,15))])
    confirmacao_senha = PasswordField('Confirme a Senha', validators=[DataRequired(),EqualTo('senha',message=funcao_validacao.mensagem_confirmacao_senha())])
    mandar_registro = SubmitField('Submeter Cadastro')
   

class ComentarioForm(FlaskForm):
    comentarios=TextAreaField('Comentario',validators=[DataRequired(),Length(1,120,message=funcao_validacao.mensagem_tamanho(1,120))])
    mandar_comentario = SubmitField('Submeter Comentario',validators=[])

class LoginForm(FlaskForm):
    nome = StringField('Nome_do_Usuario',validators=[DataRequired(),Length(2,15,message=funcao_validacao.mensagem_tamanho(2,15))])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Mantenha-me conectado')
    mandar_login = SubmitField('Logar')


class EditarPerfilForm(FlaskForm):
    def validate_nome_usuario(self,nome):
        if nome.data != current_user.nome:
            usuario = Usuario.query.filter_by(nome=nome.data).first()          
            if usuario:
                raise ValidationError('O nome citado já foi utilizado. Por favor escolha outro!')

    def validate_email_usuario(self,email):
        if email.data != current_user.email:
            email = Usuario.query.filter_by(email=email.data).first()           
            if email:
                raise ValidationError('O email citado já foi utilizado. Por favor escolha outro!')

    nome = StringField('Nome_do_Usuario',validators=[DataRequired(),Length(2,15,message=funcao_validacao.mensagem_tamanho(2,15)),validate_nome_usuario])
    email = StringField('Email',validators =[DataRequired(), Email(funcao_validacao.mensagem_email_invalido()),validate_email_usuario])
    foto_nova=FileField('Trocar a foto de perfil :3', validators=[FileAllowed(['jpg','png','jpeg'],message=funcao_validacao.mensagem_formatoimg())])
    mandar_editacao_perfil = SubmitField('Mudar dados')

class PostagemForm(FlaskForm):
    titulo = StringField('Titulo postagem',validators=[DataRequired(),Length(2,20,message=funcao_validacao.mensagem_tamanho(2,20))])
    conteudo = TextAreaField('Conteudo', validators=[DataRequired(),Length(2,200,message=funcao_validacao.mensagem_tamanho(2,100))])
    imagem_postagem = FileField('imagem pra postagem :D', validators=[FileAllowed(['jpg','png','jpeg'],message=funcao_validacao.mensagem_formatoimg())])
    mandar_postagem = SubmitField('Submeter Postagem')


class EditarPostagemForm(FlaskForm):
    titulo = StringField('Titulo postagem',validators=[DataRequired(),Length(2,20,message=funcao_validacao.mensagem_tamanho(2,20))])
    conteudo = TextAreaField('Conteudo', validators=[DataRequired(),Length(2,100,message=funcao_validacao.mensagem_tamanho(2,100))])
    mandar_edicao_postagem = SubmitField('Submeter Edições')

class AvaliacaoForm(FlaskForm):
    estrela = RadioField('Estrela1',choices=[('1',''),('2',''),('3',''),('4',''),('5','')],validators=[DataRequired()])
    mandar_avaliacao = SubmitField('Submeter Avaliação')

class EmailResetarSenhaForm(FlaskForm):
    def validate_email_usuario(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is None:
            raise ValidationError('Não se tem registros de contas com esse email, por favor, tente novamente!')
            user=None
    email = StringField('Email',validators =[DataRequired(funcao_validacao.mensagem_email_invalido()), Email(),validate_email_usuario])
    mandar_email_reset = SubmitField('Requisitar outra senha')

class ResetarSenhaForm(FlaskForm):
    senha = PasswordField('Senha', validators=[DataRequired(),Length(2,15,message=funcao_validacao.mensagem_tamanho(2,15))])
    confirmacao_senha = PasswordField('Confirme a Senha', validators=[DataRequired(),EqualTo('senha',message=funcao_validacao.mensagem_confirmacao_senha())])
    mandar_nova_senha = SubmitField('Confirmar Nova Senha')
