-- ============================================
-- CREAR ESQUEMA Y TABLAS
-- ============================================
-- El esquema se crea con AUTHORIZATION administrador
-- Esto significa que administrador es el propietario
-- Las tablas también son propiedad de administrador

-- Conectar como administrador para crear el esquema
SET ROLE administrador;

CREATE SCHEMA IF NOT EXISTS travel AUTHORIZATION administrador;

-- Tabla de usuarios
CREATE TABLE travel.appuser (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255),
    bio TEXT
);

-- Tabla de viajes
CREATE TABLE travel.trip (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    user_id INTEGER REFERENCES travel.appuser(id) ON DELETE CASCADE,
    cover_photo_url VARCHAR(255),
    summary TEXT,
    created_at TIMESTAMP
);



-- Entradas de viaje (como un diario)
CREATE TABLE travel.trip_entry (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES travel.trip(id) ON DELETE CASCADE,
    title VARCHAR(255),
    date DATE,
    text_trip TEXT,
    created_at TIMESTAMP
);

-- Fotos
CREATE TABLE travel.photo (
    id SERIAL PRIMARY KEY,
    trip_entry_id INTEGER REFERENCES travel.trip_entry(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    caption TEXT,
    uploaded_at TIMESTAMP
);

-- Lugares visitados (NUEVA VERSIÓN NORMALIZADA)
CREATE TABLE travel.country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE travel.city (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INTEGER REFERENCES travel.country(id) ON DELETE CASCADE,
    lat FLOAT,
    lng FLOAT,
    UNIQUE (name, country_id)
);

CREATE TABLE travel.place_visited (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES travel.trip(id) ON DELETE CASCADE,
    country_id INTEGER REFERENCES travel.country(id) ON DELETE CASCADE,
    city_id INTEGER REFERENCES travel.city(id) ON DELETE CASCADE
);

-- Lista de deseos (normalizada)
CREATE TABLE travel.whislist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES travel.appuser(id) ON DELETE CASCADE,
    title TEXT,
    note TEXT,
    country_id INTEGER REFERENCES travel.country(id) ON DELETE CASCADE,
    city_id INTEGER REFERENCES travel.city(id) ON DELETE CASCADE,
    priority INTEGER
);

-- Etiquetas
CREATE TABLE travel.tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Relación n:m entre trip y tag
CREATE TABLE travel.trip_tag (
    trip_id INTEGER REFERENCES travel.trip(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES travel.tag(id) ON DELETE CASCADE,
    PRIMARY KEY (trip_id, tag_id)
);
