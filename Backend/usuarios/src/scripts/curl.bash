curl -X POST http://localhost:3000/usuarios/auth \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'