Tenha python 3.6, docker e minikube.

Inicie o minikube com:<br/>
`minikube start`

Com o terminal na pasta base do projeto execute:<br/>`python deploy.py --namespace apiexample`

Siga as instrucoes geradas pelo script anterior. 

Para testar utilize os endpoints:<br/>
`localhost:5000/healthCheck`
`localhost:5000/add/car`
`localhost:5000/get/car/<placa>`

Exemplo de POST json para o `localhost:5000/add/car`:<br/>
`{
"Cor": "XXX",
"Placa": "XXXX-XXXX",
"Ano": "3245",
"Modelo": "XXXX"
}`

