DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE EXTENSION pgcrypto;

CREATE TABLE Member (
id int PRIMARY KEY,
is_leader bool,
password text,
last_action_time timestamp
);

CREATE TABLE Authority (
  id int PRIMARY KEY
);

CREATE TABLE Project (
id int PRIMARY KEY,
authority int REFERENCES Authority(id)
);

CREATE TABLE Action (
id int PRIMARY KEY,
projectid int,
memberid int,
upvotes int,
downvotes int,
type text
);

CREATE TABLE Votes (
memberid int REFERENCES Member(id),
actionid int REFERENCES Action(id),
votetype text
);

CREATE TABLE Project_has_action (
project_id int REFERENCES Project(id),
action_id int REFERENCES Action(id)
);

CREATE TABLE Action_has_initiator (
action_id int REFERENCES Action(id),
votetype text
);

CREATE TABLE Identifiers (
  id int PRIMARY KEY
);

CREATE FUNCTION password_exists(passw text) RETURNS bool AS
$X$
  BEGIN
    RETURN EXISTS (SELECT * FROM member WHERE crypt(passw,gen_salt('bf'))=password);
  END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION validate_member(mem int, passw text) RETURN bool AS
$X$
  DECLARE
  m int;
  p text;
  BEGIN
        SELECT id,password INTO m,p FROM member
        WHERE id=mem;
        IF m IS NULL THEN
          RETURN true

        IF p=crypt(passw,gen_salt('bf')) THEN
          RETURN true;
        END IF;
        RETURN false;
  END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION check_password() RETURNS TRIGGER AS
$X$
  BEGIN
    SELECT id FROM member
    WHERE
  END
$X$


CREATE FUNCTION insert_to_identifiers() RETURNS TRIGGER AS
$X$
    BEGIN
      INSERT INTO Identifiers(id) VALUES(NEW.id);
      RETURN NEW;
    END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION on_insert_to_member() RETURNS TRIGGER AS
$X$
  BEGIN
      insert_to_identifiers();
  END
$X$

CREATE TRIGGER on_insert_to_member BEFORE INSERT ON member
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_project BEFORE INSERT ON project
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_action BEFORE INSERT ON action
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_authority BEFORE INSERT ON Authority
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER  BEFORE INSERT ON
