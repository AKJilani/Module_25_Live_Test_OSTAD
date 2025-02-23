/*All Query to create all tables which need for this APP*/


CREATE TABLE auth_permission (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);


CREATE TABLE auth_group (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);


CREATE TABLE auth_group_permissions (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
);


CREATE TABLE auth_user (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BIT NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BIT NOT NULL,
    is_active BIT NOT NULL,
    date_joined DATETIME NOT NULL,
    first_name VARCHAR(150) NOT NULL
);


CREATE TABLE auth_user_groups (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE
);


CREATE TABLE auth_user_user_permissions (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
);



CREATE TABLE django_content_type (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE (app_label, model)
);


CREATE TABLE auth_user (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BIT NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BIT NOT NULL,
    is_active BIT NOT NULL,
    date_joined DATETIME NOT NULL,
    first_name VARCHAR(150) NOT NULL
);


CREATE TABLE django_admin_log (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    object_id NVARCHAR(MAX) NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
    change_message NVARCHAR(MAX) NOT NULL,
    content_type_id INT NULL,
    user_id INT NOT NULL,
    action_time DATETIME NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);


CREATE TABLE django_migrations (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
);


CREATE TABLE django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data NVARCHAR(MAX) NOT NULL,
    expire_date DATETIME NOT NULL
);


CREATE TABLE social_app_post (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    content NVARCHAR(MAX) NOT NULL,
    image VARCHAR(100) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE social_app_comment (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    content NVARCHAR(MAX) NOT NULL,
    created_at DATETIME NOT NULL,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES social_app_post(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE NO ACTION 
);


CREATE TABLE social_app_like (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL,
    post_id INT NOT NULL,  
    user_id INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES social_app_post(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE NO ACTION  
);


CREATE TABLE social_app_share (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    comment NVARCHAR(MAX) NOT NULL,
    created_at DATETIME NOT NULL,
    original_post_id INT NOT NULL,  
    user_id INT NOT NULL,
    FOREIGN KEY (original_post_id) REFERENCES social_app_post(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE NO ACTION  
);


CREATE TABLE social_app_userprofile (
    id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    profile_picture VARCHAR(100) NOT NULL,
    bio NVARCHAR(MAX) NOT NULL, 
    location VARCHAR(100) NOT NULL,
    birth_date DATE,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
