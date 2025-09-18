Refact número 1) Por que foi necessário a refatoração de curtir e descurtir?

Antes, o metódo/lógica de curtir/descurtir estava em LikePostView e UnlikePostView, e ambas funções tinha a mesma lógica.

Para otimizar, eliminamos a duplicação (DRY) e centralizamos a lógica, no método de service (toggle_user_like), que faz a alternância do estado de following do user.
Enquanto a View ficou responsável apenas por lidar com a requisição HTTP e chamar o service.

Refact numéro 2) Por que foi necessário a refatoração de unfollow e follow?

Antes, a lógica para "seguir" e "deixar de seguir" estava duplicada em duas classes de View separadas (FollowUserView e UnfollowUserView). Ambas faziam quase a mesma coisa: validavam o usuário, checavam se a relação existia, adicionavam ou removiam de dois campos ManyToMany (following e followers) e atualizavam os contadores total_following e total_followers.

Para otimizar, eliminamos a duplicação (DRY) e centralizamos a lógica, no método de service (toggle_user_follow), que faz a alternância do estado de following do user.
Enquanto a View ficou responsável apenas por lidar com a requisição HTTP e chamar o service.
