DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE EXTENSION pgcrypto;

CREATE TABLE Member (
id int PRIMARY KEY,
is_leader bool,
password text,
last_action_time timestamp,
upvotes int DEFAULT 0,
downvotes int DEFAULT 0
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
upvotes int DEFAULT 0,
downvotes int DEFAULT 0,
type text
);

CREATE TABLE Votes (
member_id int REFERENCES Member(id),
action_id int REFERENCES Action(id),
type text,
CONSTRAINT pk PRIMARY KEY (member_id, action_id)
);

CREATE TABLE Action_has_initiator (
action_id int REFERENCES Action(id),
member_id int REFERENCES Member(id)
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

CREATE FUNCTION member_exists(memid int) RETURNS bool AS
$X$
  BEGIN
    RETURN EXISTS (SELECT * FROM member WHERE id = memid);
  END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION is_active(t timestamp,n timestamp) RETURNS bool AS
$X$
  BEGIN
    RETURN (n-t < '1 year');
  END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION member_validation(mem int, passw text) RETURNS bool AS
$X$
  DECLARE
  m int;
  p text;
  BEGIN
        SELECT id,password INTO m,p FROM member
        WHERE id=mem;
        IF p = crypt(passw, p) THEN
          RETURN true;
        END IF;
        RETURN false;
  END
$X$ LANGUAGE plpgsql;


CREATE FUNCTION insert_to_identifiers() RETURNS TRIGGER AS
$X$
    BEGIN
      INSERT INTO Identifiers(id) VALUES(NEW.id);
      RETURN NEW;
    END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION insert_to_authority_too() RETURNS TRIGGER AS
$X$
    BEGIN
      INSERT INTO Authority(id) VALUES(NEW.authority);
      RETURN NEW;
    END
$X$ LANGUAGE plpgsql;

CREATE FUNCTION update_votes_count() RETURNS TRIGGER AS
$X$
    BEGIN
        IF NEW.type='upvote' THEN
          UPDATE member SET upvotes=upvotes+1 WHERE id=NEW.member_id;
          UPDATE action SET upvotes=upvotes+1 WHERE id=NEW.action_id;
        ELSE
          UPDATE member SET downvotes=downvotes+1 WHERE id=NEW.member_id;
          UPDATE action SET downvotes=downvotes+1 WHERE id=NEW.action_id;
        END IF;
        RETURN NEW;
    END
$X$ LANGUAGE plpgsql;

-- CREATE FUNCTION on_insert_to_member() RETURNS TRIGGER AS
-- $X$
--   BEGIN
--       insert_to_identifiers(NEW.id);
--       IF password_exists(NEW.password) THEN
--         RAISE EXCEPTION 'password is already used';
--       END IF
--       RETURN NEW;
--   END
-- $X$ LANGUAGE plpgsql;


CREATE TRIGGER on_insert_to_member BEFORE INSERT ON member
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_project BEFORE INSERT ON project
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_project2 BEFORE INSERT ON project
FOR EACH ROW EXECUTE PROCEDURE insert_to_authority_too();

CREATE TRIGGER on_insert_to_action BEFORE INSERT ON action
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_authority BEFORE INSERT ON Authority
FOR EACH ROW EXECUTE PROCEDURE insert_to_identifiers();

CREATE TRIGGER on_insert_to_votes BEFORE INSERT ON Votes
FOR EACH ROW EXECUTE PROCEDURE update_votes_count();
-- CREATE TRIGGER  BEFORE INSERT ON
