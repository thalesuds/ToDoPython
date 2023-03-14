# ToDoPython
Esta aplicação tem o objetivo de registrar tarefas para serem feitas (To Do), e ainda, descrever o progresso de cada tarefa.

Deste modo criou-se entidades, formadas por uma classe de tarefas e outra de progresso. Como o intuíto deste código é apenas
aplicar as metodologias de arquitetura de Onion Layer, príncipios Solid e Clean Code, não foi utilizado um banco de dados em SQL, 
mas sim, um em memória.

Assim, criou-se uma classe DataBase, para que fosse registradas as nossas tarefas e progressos. Para fazer a criação das entidades,
foram utilizadas factories, aqui também com o objetivo de aprendizado de Padrão de Design Factory.

Para realizar a leitura e passar as informações das tarefas e dos progressos para serem salvas no banco, foram utilizadas classes 
de Serviço, uma para tarefas, sendo outra para progresso.

Uma vez que a camada de Apresentação estava concluída, ficou completa a estruturação a arquitetura Onion, onde o fluxo de informação
dentro do software se dava pela seguinte forma:

![image](https://user-images.githubusercontent.com/103439806/225080069-05d348db-1c2e-4aaa-b63d-6214dc376782.png)

Como o objetivo aqui era o aprendizado das metodologias descritas acima, não foi dado grande ênfase no stack de back-end. 

E assim, ficou a interface para as tarefas.

![image](https://user-images.githubusercontent.com/103439806/225072273-5af1947e-5868-4cb6-9084-5963f85035bd.png)

Veja, é possível que o usário salve, delete e adicione progresso as tarefas, sendo que a janela de progressos ficou assim:
![image](https://user-images.githubusercontent.com/103439806/225072491-f885083f-a03a-4e2f-b17d-65619678734d.png)
