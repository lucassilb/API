from flask import Flask
from flask_restx import Api, Resource, fields
 
app = Flask(__name__)
 
api = Api(
    app,
    version="1.0",
    title="Minha API",
    description="API REST feita com Flask",
    doc="/swagger"
)
 
ns = api.namespace("usuarios", description="Operações relacionadas a usuários")
 
usuario_model = api.model("Usuario", {
    "id": fields.Integer(readonly=True, description="ID do usuário"),
    "nome": fields.String(required=True, description="Nome do usuário"),
    "email": fields.String(required=True, description="Email do usuário"),
    "Telefone": fields.String(required=False, description="Telefone do usuário"),
})
 
usuarios = [
    {"id": 1, "nome": "João", "email": "joao@example.com", "Telefone": "123456789"},
    {"id": 2, "nome": "Maria", "email": "maria@example.com", "Telefone": "987654321"}
]
 
@ns.route("/")
class UsuarioList(Resource):
    @ns.doc('Listar todos os usuários')
    def get(self):
        """Listar todos os usuários"""
        return usuarios, 200
   
    @ns.expect(usuario_model)
    @ns.doc('Criar um novo usuário')
    def post(self):
        """Criar um novo usuário"""
        novo_usuario = api.payload
        novo_usuario["id"] = len(usuarios) + 1
        usuarios.append(novo_usuario)
        return novo_usuario, 201
 
@ns.route("/<int:id>")
@ns.param("id", "ID do usuário")
class Usuario(Resource):
    @ns.doc('Obter um usuário pelo ID')
    def get(self, id):
        '''Obter um usuário pelo ID'''
        for usuario in usuarios:
            if usuario["id"] == id:
                return usuario, 200
        return {"message": "Usuário não encontrado"}, 404
 
    @ns.expect(usuario_model)
    @ns.doc('Atualizar um usuário pelo ID')
    def put(self, id):
        """Atualizar um usuário pelo ID"""
        for usuario in usuarios:
            if usuario["id"] == id:
                usuario.update(api.payload)
                return usuario, 200
        return {"message": "Usuário não encontrado"}, 404
 
    @ns.doc('Deletar um usuário pelo ID')
    def delete(self, id):
        """Deletar um usuário pelo ID"""
        for usuario in usuarios:
            if usuario["id"] == id:
                usuarios.remove(usuario)
                return {"message": "Usuário deletado com sucesso"}, 200
        return {"message": "Usuário não encontrado"}, 404
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)