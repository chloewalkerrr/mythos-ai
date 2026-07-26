-- stored procedures
-- chloe walker

DELIMITER //

-- get children by god parent
DROP PROCEDURE IF EXISTS GetCharactersByGodParent //
CREATE PROCEDURE GetCharactersByGodParent(IN god_name VARCHAR(100))
BEGIN
    SELECT c.* 
    FROM characters c
    JOIN gods g ON c.parent_god_id = g.id
    WHERE g.name = god_name;
END //

-- get quest details
DROP PROCEDURE IF EXISTS GetQuestDetails(IN quest_id INT)
BEGIN
    SELECT 
        q.title,
        q.status,
        q.difficulty_level,
        b.title as book
    FROM quests q
    LEFT JOIN books b ON q.book_id = b.id
    WHERE q.id = quest_id;
END //

-- update character status
DROP PROCEDURE IF EXISTS UpdateCharacterStatus(
    IN char_id INT,
    IN new_status VARCHAR(50)
)
BEGIN
    UPDATE characters 
    SET status = new_status 
    WHERE id = char_id;
END //

DELIMITER ;