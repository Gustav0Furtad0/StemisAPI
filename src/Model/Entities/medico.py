from src.Model.database import db
from werkzeug.security import check_password_hash, generate_password_hash

class Medico(db.Model):
    ##* Atributos da tabela "medicos"
    __tablename__ = 'medicos'
    __cpf = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    __nome_completo = db.Column(db.String(255), nullable=False)
    __crm = db.Column(db.Integer, nullable=False, unique=True)
    __data_inscricao_crm = db.Column(db.Date, nullable=False)
    __senha = db.Column(db.String(50), nullable=False)
    __consultas = db.relationship('Consulta', backref='medico')
    
    def __init__(self, nome_completo, crm, cpf, data_inscricao_crm, senha):
    ## Metodo de inicialização da classe
        self.__nome_completo = nome_completo
        self.__crm = crm
        self.__cpf = cpf
        self.__data_inscricao_crm = data_inscricao_crm
        self.__senha = generate_password_hash(senha)
    
    def to_dict(self):
    ## Metodo para retornar os dados do medico em um dicionario
        '''
        Retorna um dicionário com os dados do médico
        Returns:
            dict -- Dicionário com os dados do médico
            {
                'cpf': int,
                'nome_completo': str,
                'crm': int,
                'data_inscricao_crm': date
            }
        '''
        return {
            'cpf': self.__cpf,
            'nome_completo': self.__nome_completo,
            'crm': self.__crm,
            'data_inscricao_crm': self.__data_inscricao_crm,
        }
    def buscar_consultas(self):
    ## Metodo para retornar consultas do medico
        '''
        Retorna as consultas do médico
        Returns:
            list -- Lista com as consultas do médico
        '''
        return self.__consultas
    
    def atualizar_medico(self, cpf=False, nome_completo=False, crm=False, data_inscricao_crm=False, senha=False):
    ## Metodo para atualizar medico
        '''
        Atualiza os dados do médico
        Keyword Arguments:
            cpf {int} -- CPF do médico (default: {False})
            nome_completo {str} -- Nome completo do médico (default: {False})
            crm {int} -- CRM do médico (default: {False})
            data_inscricao_crm {date} -- Data de inscrição no CRM do médico (default: {False})
            senha {str} -- Senha do médico (default: {False})
        '''
        try:
            if cpf:
                self.__cpf = cpf
            
            if nome_completo:
                self.__nome_completo = nome_completo
            
            if crm:
                self.__crm = crm
                
            if data_inscricao_crm:
                self.__data_inscricao_crm = data_inscricao_crm
            
            if senha:
                self.__senha = senha
            
            db.session.commit()
            return True, 'Médico atualizado com sucesso!'
        
        except:
            return False, 'Erro ao atualizar médico!'
    
    def verificar_senha(self, senha):
    ## Metodo para verificar senha
        '''
        Verifica se a senha informada é a senha do médico
        Arguments:
            senha {str} -- Senha a ser verificada
        Returns:
            bool -- True se a senha informada for a senha do médico
            bool -- False se a senha informada não for a senha do médico
        '''
        return check_password_hash(self.__senha, senha)
    
    def deletar_medico(self):
        ## Metodo para deletar medico
        '''
        Deleta o médico do banco de dados
        '''
        try:
            db.session.delete(self)
            db.session.commit()
            return True, 'Médico deletado com sucesso!'
        
        except:
            return False, 'Erro ao deletar médico!'
    
    ##* Metodos estaticos
    @staticmethod
    def adicionar_medico(cpf, nome_completo, crm, data_inscricao_crm, senha):
        ## Metodo para cadastrar novo medico
        '''
        Adiciona um médico ao banco de dados
        Arguments:
            cpf {int} -- CPF do médico
            nome_completo {str} -- Nome completo do médico
            crm {int} -- CRM do médico
            data_inscricao_crm {date} -- Data de inscrição no CRM do médico
            senha {str} -- Senha do médico
            
        Returns:
            bool -- True se o médico for adicionado com sucesso
            bool -- False se o médico não for adicionado com sucesso
            str -- Mensagem de erro
        '''
        try:
            medico = Medico.query.filter_by(crm=crm).first()
            if medico:
                raise Exception('CRM já cadastrado!')
            medico = Medico(nome_completo, crm, cpf, data_inscricao_crm, senha)
            db.session.add(medico)
            db.session.commit()
            return True, 'Médico adicionado com sucesso!'
        except:
            return False, 'Erro ao adicionar médico!'
    
    @staticmethod
    def buscar_medico_crm(crm):
        ## Metodo para buscar medico pelo CRM
        '''
        Busca um médico pelo CRM
        Arguments:
            crm {int} -- CRM do médico
        Returns:
            Medico -- Objeto do médico encontrado
            bool -- False se o médico não for encontrado
        '''
        medico = Medico.query.filter_by(crm=crm).first()
        if medico:
            return medico
        return False
