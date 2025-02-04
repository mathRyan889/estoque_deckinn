from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "estoque.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class EstoqueEVA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cor = db.Column(db.String(100), nullable=False)
    medida = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return (f'<EVA {self.id}: {str(self.cor).upper()} - {str(self.medida).upper()} - {int(self.quantidade)}un>')

def criar_banco():
    with app.app_context():
        if not os.path.exists(os.path.join(basedir, 'estoque.db')):
            db.create_all()
            print("✅ Banco criado com sucesso em:", os.path.join(basedir, 'estoque.db'))
        else:
            print("⚠️  Banco já existe em:", os.path.join(basedir, 'estoque.db'))

@app.route('/')
def index():
    itens = EstoqueEVA.query.order_by(EstoqueEVA.id).all()
    return render_template('index.html', itens=itens)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        try:
            novo_item = EstoqueEVA(
                cor=request.form['cor'].strip().upper(),
                medida=request.form['medida'].strip().upper(),
                quantidade=int(request.form['quantidade'])
            )
            db.session.add(novo_item)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Erro: {str(e)}", 500
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    item = EstoqueEVA.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            item.cor = request.form['cor'].strip().upper()
            item.medida = request.form['medida'].strip().upper()
            item.quantidade = int(request.form['quantidade'])
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Erro ao atualizar: {str(e)}", 500
    
    return render_template('editar.html', item=item)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    item = EstoqueEVA.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao excluir: {str(e)}", 500

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)