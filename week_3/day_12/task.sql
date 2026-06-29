-- When we use the reference ? - Column level short hand 
-- if going to create a table with link a single column use the references keyword
-- but it not support to modify the table or alter table in future


-- When we use the foreign key ? - Table level definition
-- if going to create a table with link a multiple column use the forigen keyword
-- it support to alter the table 


-- if i delete the user why it not affect occurs error ?
-- because we use reference or foregin key only if it need to delete automatically add the ON DELETE CASCADE rule to foriegn key configuration


-- types of Joins 
-- 1) left Join  - it return values from full left table values and common values from right tables
-- 2) right Join - it return values from full right values and common values from left tables
-- 3) inner Join or join - it return common values from both tables
-- 4) outer join - it return the common values from both tables and also uncommon values 


-- CASCADE is an automatic trigger that passes on action (like update or delete) from a parent row down to all its connected child rows.


-- what is index in postgresql ?
-- is a tool that helps to speed up the process of finding data in table.
-- without the index, it look entire of rows in the tables it makes slow.

-- types of indexes:
-- 1) B-Tree Index: 
--      default index type and well suited for most scenarios
--      best for: range queries and equality checks (<=,>=,<,>,==)
--      used for: login, search, filters

-- 2) Hash Index:
--      hash function to map values to locations in indexes
--      best for: exact match queries (=)
--      used for: exact match lookup


-- 3) GiST (Generalized Search Tree) Index:
--      flexible and support a wide range of data types and search operations
--      used for: maps and geo apps

-- 4) GIN (Generalized Inverted Index)
--      handling complex data types such as arrays and full text searches
--      used for: search engine, JSON

-- 5) BRIN (Block Range Index) 
--      suitable for large tables with ordered data
--      large datasets with ordered data 
--      used for: logs and analytics

-- what is transaction?
-- single unit of work that bundles one or more sql statmenets together so they in "all or nothing" manner.
-- Control Statements:
--    BEGIN - open new transaction
--    COMMIT - saves all operations
--    ROLLBACK - abort the current transaction and return back to pervious state
--    SAVEPOINT - create the intermediate marker inside the transaction to partial roll back the failures without cancel the transaction

-- ilike is casesenstitive and like is incase senstitve 


-- FLOW Order
-- SELECT  ->  DISTINCT  ->  FROM  ->  JOIN  ->  WHERE  ->  GROUPBY  ->  HAVING  ->  ORDER BY  -> LIMIT  ->  OFFSET
-- INSERT INTO -> VALUES
-- UPDATE -> SET -> WHERE
-- DELETE FROM -> WHERE


CREATE TABLE post(
    id SERIAL Primary KEY,
    user_id BIGINT NOT NULL, -- REFERENCES user(id),
    content TEXT NOT NULL,
    publishedat TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY(user_id) references users(id) on delete cascade
)

insert into post (id, user_id, content) values (1, 1, 'Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis.');
insert into post (id, user_id, content) values (2, 2, 'Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat.');
insert into post (id, user_id, content) values (3, 3, 'Fusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem. Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.');
insert into post (id, user_id, content) values (4, 4, 'Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.');
insert into post (id, user_id, content) values (5, 5, 'Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus.');
insert into post (id, user_id, content) values (6, 6, 'Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis.');
insert into post (id, user_id, content) values (7, 7, 'In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.');
insert into post (id, user_id, content) values (8, 8, 'Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus.');
insert into post (id, user_id, content) values (9, 9, 'In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst.');
insert into post (id, user_id, content) values (10, 10, 'Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.');
insert into post (id, user_id, content) values (11, 1, 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia.');
insert into post (id, user_id, content) values (12, 2, 'Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero.');
insert into post (id, user_id, content) values (13, 3, 'Vivamus in felis eu sapien cursus vestibulum. Proin eu mi.');
insert into post (id, user_id, content) values (14, 4, 'Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.');
insert into post (id, user_id, content) values (15, 5, 'Suspendisse potenti.');
insert into post (id, user_id, content) values (16, 6, 'Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.');
insert into post (id, user_id, content) values (17, 7, 'Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc.');
insert into post (id, user_id, content) values (18, 8, 'Morbi non quam nec dui luctus rutrum.');
insert into post (id, user_id, content) values (19, 9, 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus.');
insert into post (id, user_id, content) values (20, 10, 'In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.');


select users.id ,users.name , post.content from users
join post on users.id = post.user_id;


select users.name ,count(post.user_id) from users
join post on users.id = post.user_id 
group by users.id, users.name; 

insert into users(name,email,gender) values
('chandru','chan22@gmail.com','Male');

update users set email = 'chandrutd22@gamil.com' where name = 'chandru';

insert into post (id,user_id,content) values
(21,11,'Introduction of github'),
(22,11,'Introduction to PostgreSQL');

delete from users where id = 1;

insert into users (name,email, gender) values
('Hari','Hari22@gamil.com','Male');

select users.name, post.content from users 
left join post on users.id = post.user_id
order by users.name;


