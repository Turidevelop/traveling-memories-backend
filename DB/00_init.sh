#!/bin/bash
set -e

echo "🔐 Inicializando base de datos con roles seguros..."

# Crear roles usando SQL idempotente (funciona en Docker, Railway, Render)
PGPASSWORD="" psql -U administrador -d postgres << EOSQL
DO \$\$ BEGIN
    CREATE ROLE administrador WITH LOGIN ENCRYPTED PASSWORD '${DB_ADMIN_PASSWORD}' CREATEDB CREATEROLE;
EXCEPTION WHEN DUPLICATE_OBJECT THEN
    ALTER ROLE administrador WITH LOGIN CREATEDB CREATEROLE;
END \$\$;

DO \$\$ BEGIN
    CREATE ROLE app_user WITH LOGIN ENCRYPTED PASSWORD '${DB_APP_PASSWORD}';
EXCEPTION WHEN DUPLICATE_OBJECT THEN
    ALTER ROLE app_user WITH LOGIN;
END \$\$;
EOSQL

echo "✅ Roles creados"

echo "📊 Creando esquema y tablas..."
PGPASSWORD="" psql -U administrador -d travel_db < /docker-entrypoint-initdb.d/03_create_schema_travel_and_tables.sql

echo "🔑 Asignando permisos..."
PGPASSWORD="" psql -U administrador -d travel_db < /docker-entrypoint-initdb.d/02_grant_permissions.sql

echo "🌍 Insertando datos de ejemplo..."
PGPASSWORD="" psql -U administrador -d travel_db < /docker-entrypoint-initdb.d/04_insert_countries.sql
PGPASSWORD="" psql -U administrador -d travel_db < /docker-entrypoint-initdb.d/05_insert_into_appuser.sql

echo "✨ Base de datos inicializada correctamente"
