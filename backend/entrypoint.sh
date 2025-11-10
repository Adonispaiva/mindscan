# D:\projetos-inovexa\mindscan\backend\entrypoint.sh
#!/bin/bash

# Aguarda o banco de dados ficar disponível
until pg_isready -h db -p 5432 -U $POSTGRES_USER; do
  echo "Aguardando o banco de dados..."
  sleep 2
done

# Aplica migrações e executa a aplicação
alembic upgrade head
exec flask run --host=0.0.0.0 --port=$BACKEND_PORT
