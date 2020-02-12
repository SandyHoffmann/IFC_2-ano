from flask import render_template, url_for, flash, redirect,request
from animesite import app,db,bcrypt,mail
from animesite.formulario import RegistroForm, LoginForm, EditarPerfilForm,PostagemForm,EditarPostagemForm,ComentarioForm,AvaliacaoForm,EmailResetarSenhaForm,ResetarSenhaForm
from animesite.model import Usuario, Postagem, Comentario, Avaliacao
from flask_login import current_user,logout_user,login_required,login_user
from wtforms.validators import ValidationError
import secrets
import os
from PIL import Image
from flask_mail import Message

@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home_anime.html', titulo='AnimeWebSite')

@app.route('/top_postagens',methods=['GET','POST'])
def top_postagens():
    post=Postagem()
    estrelas=Avaliacao()
    posts_bem_avaliados=Postagem.query.order_by(Postagem.media.desc()).all()
    numero_posts=len(posts_bem_avaliados)
    lista_top_posts=[]
    posts_existentes=0
    mensagem = ""
    if numero_posts==0:
        mensagem = "Essa página ainda não possui postagens, seja o primeiro a postar! "
    else:
        if numero_posts<=5 and numero_posts>0:
            posts_existentes=numero_posts
            mensagem = "A página possui o total de "+str(numero_posts)+" postagens no momento, entre para fazer parte da comunidade! "
        if numero_posts>5:
            posts_existentes=5
            mensagem = "A página possui o total de "+str(numero_posts)+" postagens no momento, entre para fazer parte da comunidade! "
        for x in range(posts_existentes):
            lista_top_posts.append(posts_bem_avaliados[x])
    return render_template('top_postagens.html', titulo='Top Postagens',lista=lista_top_posts,mensagem=mensagem)

@app.route('/registro' ,methods=['GET','POST'])
def registro():
    formulario = RegistroForm()
    if formulario.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(formulario.senha.data).decode('utf-8')
        usuario=Usuario(nome=formulario.nome.data,email=formulario.email.data,senha=senha_criptografada)
        db.session.add(usuario)
        db.session.commit()
        return redirect('login')
    return render_template('registro.html', titulo='Registro', form=formulario)
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        formulario = LoginForm()
        if formulario.validate_on_submit():
            usuario=Usuario.query.filter_by(nome=formulario.nome.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha,formulario.senha.data):
                login_user(usuario,remember=formulario.lembrar.data)
                return redirect(url_for('home'))
            else:
                flash('Login não foi possivel, por favor verifique seus dados novamente!')
    return render_template('login.html', titulo='login', form=formulario)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def salvarfoto(foto_nova,diretorio):
    numero_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(foto_nova.filename)
    foto_arquivo=numero_hex+f_ext
    diretorio=os.path.join(app.root_path,'static/'+diretorio,foto_arquivo )
    tamanhoimg=(250,250)
    imagem=Image.open(foto_nova)
    imagem.thumbnail(tamanhoimg)
    imagem.save(diretorio)
    return(foto_arquivo)

@app.route('/perfil'+'<user_id>',methods=['GET','POST'])
@login_required
def perfil(user_id):
    posts=Postagem.query.filter(Postagem.usuario_id==user_id).all()
    formulario=EditarPerfilForm()
    usuario=Usuario.query.filter_by(id=user_id).first()
    if formulario.validate_on_submit():
        if formulario.nome.data!=usuario.nome or formulario.email.data!= usuario.email or formulario.foto_nova.data:
            if formulario.nome.data!=usuario.nome:
                usuario.nome = formulario.nome.data
            if formulario.email.data!= usuario.email:
                usuario.email = formulario.email.data
            if formulario.foto_nova.data:
                img_antiga=usuario.foto_perfil
                if img_antiga!='default.jpg':
                    os.remove('animesite/static/imagens_perfil/'+img_antiga)
                else:
                    pass
                foto_arquivo=salvarfoto(formulario.foto_nova.data,diretorio='imagens_perfil')
                usuario.foto_perfil=foto_arquivo
            db.session.commit()
            redirect(url_for('perfil',user_id=user_id))
    elif request.method == 'GET':
        formulario.nome.data=usuario.nome
        formulario.email.data=usuario.email
    foto_nova=url_for('static',filename='imagens_perfil/'+ current_user.foto_perfil)
    return render_template('perfil.html', titulo='Perfil',foto_perfil=foto_nova,form=formulario,posts=posts,len_post=len(posts),usuario=usuario)


@app.route('/postagens',methods=['GET','POST'])
@login_required
def postar():
    formulario=PostagemForm()
    if formulario.validate_on_submit():
        if formulario.imagem_postagem.data:
            imagem=salvarfoto(formulario.imagem_postagem.data,diretorio='imagens_postagem')
            post=Postagem(titulo=formulario.titulo.data,conteudo=formulario.conteudo.data,autor=current_user,imagem_postagem=imagem)
        else:
            post=Postagem(titulo=formulario.titulo.data,conteudo=formulario.conteudo.data,autor=current_user)
        db.session.add(post)
        db.session.commit()
        return(redirect(url_for('postar')))
    postagenspg=Postagem.query.all()
    return render_template('postagens.html', titulo='Postagens',posts=postagenspg,form=formulario)

@login_required
@app.route('/post_esp_edicao'+'<post_id>',methods=['GET','POST'])
def editar_postagem(post_id):
    postagem=Postagem.query.get_or_404(post_id)
    formulario=EditarPostagemForm()
    if current_user.nome==postagem.autor.nome or current_user.administrador == True:
        post=Postagem.query.get(post_id)
        if formulario.validate_on_submit():
            post.titulo=formulario.titulo.data
            post.conteudo=formulario.conteudo.data
            if formulario.titulo.data!=post.titulo or formulario.conteudo.data!=post.conteudo:
                if formulario.titulo.data!=post.titulo:
                    post.titulo = formulario.titulo.data
                if formulario.conteudo.data!=post.conteudo:
                    post.conteudo = formulario.conteudo.data
            db.session.commit()
        elif request.method == 'GET':
            formulario.titulo.data=post.titulo
            formulario.conteudo.data=post.conteudo
        return(render_template('post_especifico_edicao.html',titulo='postagem.titulo',post=postagem,form=formulario))

@app.route('/post_esp'+'<post_id>',methods=['GET','POST'])
def ver_postagem(post_id):
    postagem=Postagem.query.get_or_404(post_id)
    comentario=ComentarioForm()
    estrela_form= AvaliacaoForm()
    post=Postagem.query.get(post_id)
    estrela_user=Avaliacao.query.filter_by(postagem_id=post_id,autor_id=current_user.id).first()
    media=post.media
    if estrela_form.validate_on_submit():
        if estrela_user:
            estrela_user.num_recebido=estrela_form.estrela.data
            db.session.commit()
        else:
            avaliacaofinal=Avaliacao(postagem_id=post_id,num_recebido=estrela_form.estrela.data,autor_id=current_user.id)
            db.session.add(avaliacaofinal)
            db.session.commit()
        media_post = calculo_media(0,post.id)
        post.media = media_post
        db.session.commit()
        return(redirect(url_for('ver_postagem',post_id=post_id)))
    elif comentario.validate_on_submit():
        comentario=Comentario(comentario_id=post_id,conteudo_comentario=comentario.comentarios.data,autor_id=(current_user.id))
        db.session.add(comentario)
        db.session.commit()
        return(redirect(url_for('ver_postagem',post_id=post_id)))
    elif request.method == 'GET':
        comentario.comentarios.data=postagem.titulo
    return(render_template('post_especifico.html',titulo='postagem.titulo',post=postagem,coment=comentario,comentariobd=Comentario.query.filter_by(comentario_id=post.id),estrela_form= AvaliacaoForm(),media=media))

def calculo_media(nova_nota=0,post_id=0):
    estrela_list=Avaliacao.query.all()
    estrela_temp=0
    total_notas=0
    cont=0
    for estrela in estrela_list:
        if estrela.postagem_id == post_id:    
            estrela_temp=estrela.num_recebido
            cont+=1
            total_notas=int(estrela_temp)+total_notas
    if cont==0:
            cont=1
    media=total_notas//cont
    return(media)

@app.route('/excluir_post'+'<post_id>',methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    postagem=Postagem.query.get_or_404(post_id)
    if postagem.autor.nome != current_user.nome and current_user.administrador == False:
        flash('Não é possivel exluir post pois ele n é seu')
        return(redirect(url_for('postar')))
    else:
        if postagem.imagem_postagem:
            os.remove('animesite/static/imagens_postagem/'+postagem.imagem_postagem)
        else:
            pass
        db.session.delete(postagem)
        db.session.commit()
        flash('Deletado com sucesso')
        return(redirect(url_for('postar')))

@login_required
@app.route('/redefinir_senha',methods=['GET','POST'])
def requisitar_nova_senha():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form=EmailResetarSenhaForm()
        if form.validate_on_submit():
            usuario=Usuario.query.filter_by(email=form.email.data).first()
            enviar_email_senha(usuario)
            flash('Mandamos um email para confirmar sua alteração de senha.','info')
            return redirect(url_for('login'))
        return render_template('redefinir_senha.html', titulo='Redefinição De Senha',form=form)

@app.route('/resetarsenha'+'<token>',methods=['GET','POST'])
def resetarsenha(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    usuario=Usuario.validate_token_usuario(token)
    if usuario == None:
        flash('Esse código não é mais valido','warning')
        return redirect(url_for('requisitar_nova_senha'))
    form = ResetarSenhaForm()
    if form.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario.senha=senha_criptografada
        db.session.commit()
        return redirect('login')
    return(render_template('resetarsenha.html', titulo='Mudando Senha',form=form))

def enviar_email_senha(usuario):
    codigo= usuario.get_token_usuario()
    mensagem=Message('Pedido para Mudança de Senha', sender='animekawaaiwebsite@gmail.com',recipients=[usuario.email])
    mensagem.body=f"""
    Para resetar a sua senha é só clicar no link abaixo:

    {url_for("resetarsenha", token=codigo,_external=True)}

    Se esse email não foi requisitado por você, pedimos que o ignore!
    """ 

    mail.send(mensagem)

