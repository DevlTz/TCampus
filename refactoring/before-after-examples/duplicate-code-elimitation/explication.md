Por que foi necessário a refatoração?
Antes, o metódo/lógica de curtir/descurtir estava em LikePostView e UnlikePostView, e ambas funções eram a mesma. Então, para otimizar resolvemos criar um único service para fazer o toggle
