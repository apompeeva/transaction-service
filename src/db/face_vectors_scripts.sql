CREATE TABLE face_vectors (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    embedding VARCHAR(1000) NOT NULL,
    path_to_image VARCHAR(255) NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO face_vectors (user_id, embedding, path_to_image, creation_time)
VALUES (1, '[1, 2, 3]', '/path/to/image', CURRENT_TIMESTAMP);

SELECT * FROM face_vectors;

UPDATE face_vectors
SET embedding = '[1, 2, 3, 4]', path_to_image = '/new/path/to/image', creation_time = CURRENT_TIMESTAMP
WHERE id = 1;

DELETE FROM face_vectors WHERE id = 1;
