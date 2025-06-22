-- Crear esquema si no existe
CREATE DATABASE traveling_memories
    OWNER administrador
    ENCODING 'UTF8'
    CONNECTION LIMIT -1;

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

-- Lugares visitados
CREATE TABLE travel.place_visited (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER REFERENCES travel.trip(id) ON DELETE CASCADE,
    country VARCHAR(100),
    city VARCHAR(100),
    lat FLOAT,
    lng FLOAT
);

-- Lista de deseos
CREATE TABLE travel.whislist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES travel.appuser(id) ON DELETE CASCADE,
    title TEXT,
    note TEXT,
    country VARCHAR(100),
    city VARCHAR(100),
    lat FLOAT,
    lng FLOAT,
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
