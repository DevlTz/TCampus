# Code Smells Identified

## Modelo

- **Arquivo**:
- **Função/Metódo**:
- **Linha**:
- **Descrição**:
- **Recomendação**:
- **Severidade**:
- **Ferramenta**:
- **Status**:

## 1. Dead Code

- **Arquivo**: src/djangoproject/posts/tests.py
- **Função/Metódo**: Classe TestCase
- **Linha**: 1:1
- **Descrição**: Módulo de testes iniciado, mas nunca utilizado. A classe nativa do django foi instanciada, mas não teve uso.
- **Recomendação**: Iniciar testes da aplicação
- **Severidade**: Baixa
- **Ferramenta**: flake8
- **Status**: Corrigido

## 2. Code Smell Estrutural ("Tratamento de Exceção Genérico").

- **Arquivo**: src/djangoproject/posts/views.py
- **Função/Metódo**: class LikePostView(APIView)
- **Linha**: 45:15
- **Descrição**: Catching too general exception Exception
- **Recomendação**: Especificar o tipo de exceção, por exemplo ValidationError do DRF ou Posts.DoesNotExist.
- **Severidade**: Alta
- **Ferramenta**: Pylint
- **Status**: Corrigido

# 3. Dead Code

- **Arquivo**: src/djangoproject/users/serializers.py
- **Função/Metódo**: from rest_framework_simplejwt.tokens import RefreshToken
- **Linha**: 6
- **Descrição**: Import "refeshToken" nunca usado
- **Recomendação**: Verificar se realmente há necessidade de
- **Severidade**: Baixa
- **Ferramenta**: vultures
- **Status**: Corrigido

# 4. Duplicate Code

- **Arquivo**: src/djangoproject/posts/views.py E src/djangoproject/users/views.py

- **Função/Método**: LikePostView.patch, UnlikePostView.patch, FollowUserView.patch, UnfollowUserView.patch

- **Linha:** Várias

- **Descrição:** Embora o pylint tenha detectado duplicação nos arquivos de migration, uma análise manual (que é parte do trabalho) revela uma duplicação de lógica muito mais grave. Os métodos para curtir/descurtir e seguir/deixar de seguir são quase idênticos em sua estrutura: obter usuário, obter objeto alvo, verificar existência, adicionar/remover de uma relação ManyToMany, incrementar/decrementar contador, salvar e responder.

- **Recomendação:** Refatorar a lógica duplicada para uma classe de serviço ou um mixin. Por exemplo, criar um PostService com um método toggle_like(user, post) e um UserService com um método toggle_follow(user, target_user). Isso adere ao princípio DRY (Don't Repeat Yourself).

- **Severidade:** Alta

- **Ferramenta:** Análise Manual (apoiada pela identificação de Pylint R0801 em outros locais, que levanta a suspeita).

- **Status:** Corrigido

# 5. Data Class / "Classe com Poucos Métodos Públicos"

- **Arquivo:** src/djangoproject/posts/models.py

- **Função/Método:** class Posts e class Event

- **Linha:** 36

- **Descrição:** O pylint aponta o erro R0903: Too few public methods (0/2) (too-few-public-methods) para a class Meta dentro dos seus models. Embora o erro seja na classe Meta, ele levanta um ponto importante sobre o Model em si: a classe Posts e a Event servem principalmente como contêineres de dados, com pouquíssimo comportamento próprio. Toda a lógica de negócio (como curtir, seguir, etc.) vive externamente, nas views. Isso é um sintoma clássico do code smell Data Class.

- **Recomendação:** Mover a lógica de negócio para dentro dos próprios models. Por exemplo, a classe Posts poderia ter um método add_like(user) e a classe User poderia ter um método follow(target_user). Isso encapsula o comportamento junto com os dados que ele manipula, seguindo melhores práticas de Orientação a Objetos.

- **Severidade:** Média

- **Ferramenta:** Pylint (R0903)

- **Status:** Este smell foi corrigido pela mesma refatoração aplicada para o Smell #4 (Criação da Camada de Serviço), que moveu a lógica de negócio das Views para os Services, aplicando o Single Responsibility Principle (SRP)

# 6. Argumento de Função Não Utilizado

- **Arquivo:** src/djangoproject/users/views.py

- **Função/Método:** ListAllUsersView.get

- **Linha: 52**

- **Descrição:** O Pylint reporta W0613: Unused argument 'request' (unused-argument). O método get na ListAllUsersView recebe o argumento request, mas nunca o utiliza em sua lógica.

- **Recomendação:** Embora em views do Django seja comum receber o request e não usá-lo, em código limpo, isso é um sinal de que o método talvez não precise de todos os parâmetros que recebe. A correção pode ser renomear o argumento para \_request para sinalizar explicitamente que ele é intencionalmente não utilizado, seguindo convenções da comunidade Python.

- **Severidade:** Baixa

- **Ferramenta:** Pylint (W0613)

- **Status:** Corrigido
