-- ============================================
-- GRANT PERMISSIONS TO APPLICATION USERS
-- ============================================
-- Este script asigna permisos específicos a:
-- - app_user: usuario principal de la aplicación
-- - alexst, turidev: usuarios específicos para casos concretos
-- Se ejecuta DESPUÉS de crear el esquema y las tablas

-- ============================================
-- PERMISOS EN EL ESQUEMA
-- ============================================
-- Permitir que app_user, alexst y turidev usen el esquema
GRANT USAGE ON SCHEMA travel TO app_user, alexst, turidev;

-- ============================================
-- PERMISOS DE LECTURA EN TABLAS
-- ============================================
-- SELECT en todas las tablas (para lectura de datos)
GRANT SELECT ON ALL TABLES IN SCHEMA travel TO app_user, alexst, turidev;

-- ============================================
-- PERMISOS DE ESCRITURA EN TABLAS
-- ============================================
-- INSERT, UPDATE, DELETE en tablas de datos
GRANT INSERT, UPDATE, DELETE ON travel.appuser TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.trip TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.trip_entry TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.photo TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.place_visited TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.country TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.city TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.whislist TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.tag TO app_user, alexst, turidev;
GRANT INSERT, UPDATE, DELETE ON travel.trip_tag TO app_user, alexst, turidev;

-- ============================================
-- PERMISOS EN SECUENCIAS (para SERIAL/AUTO INCREMENT)
-- ============================================
-- Necesario para que puedan insertar datos (nextval)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA travel TO app_user, alexst, turidev;

-- ============================================
-- ESTABLECER PERMISOS FUTUROS POR DEFECTO
-- ============================================
-- Cualquier tabla/secuencia nueva que se cree con AUTHORIZATION administrador
-- automáticamente tendrá estos permisos para todos los usuarios de aplicación
ALTER DEFAULT PRIVILEGES FOR USER administrador IN SCHEMA travel 
  GRANT SELECT ON TABLES TO app_user, alexst, turidev;

ALTER DEFAULT PRIVILEGES FOR USER administrador IN SCHEMA travel 
  GRANT INSERT, UPDATE, DELETE ON TABLES TO app_user, alexst, turidev;

ALTER DEFAULT PRIVILEGES FOR USER administrador IN SCHEMA travel 
  GRANT USAGE, SELECT ON SEQUENCES TO app_user, alexst, turidev;

ALTER DEFAULT PRIVILEGES FOR USER administrador IN SCHEMA travel 
  GRANT USAGE, SELECT ON SEQUENCES TO alexst, turidev;

-- ============================================
-- CONFIRMACIÓN
-- ============================================
-- Verificar permisos asignados:
-- SELECT grantee, privilege_type FROM information_schema.role_table_grants 
--   WHERE table_schema = 'travel' AND grantee IN ('alexst', 'turidev');
