-- views for percy jackson database
-- chloe walker

-- character power summary
DROP VIEW IF EXISTS character_power_summary;
CREATE VIEW character_power_summary AS
SELECT
    c.id,
    c.name AS character_name,
    c.age,
    g.name AS godly_parent,
    COUNT(cp.power_id) AS total_powers,
    GROUP_CONCAT(p.name SEPARATOR ', ') AS power_list
FROM characters c
LEFT JOIN gods g ON c.parent_god_id = g.id
LEFT JOIN character_powers cp ON c.id = cp.character_id
LEFT JOIN powers p ON cp.power_id = p.id
GROUP BY c.id, c.name, c.age, g.name;

-- quest statistics
DROP VIEW IF EXISTS quest_statistics;
CREATE VIEW quest_statistics AS
SELECT
    q.id,
    q.title,
    q.status,
    q.difficulty_level,
    b.title AS book_title,
    COUNT(DISTINCT qp.character_id) AS participant_count,
    COUNT(DISTINCT qm.monster_id) AS monster_count,
    sl.name AS start_location,
    el.name AS end_location
FROM quests q
LEFT JOIN books b ON q.book_id = b.id
LEFT JOIN quest_participants qp ON q.id = qp.quest_id
LEFT JOIN quest_monsters qm ON q.id = qm.quest_id
LEFT JOIN locations sl ON q.start_location_id = sl.id
LEFT JOIN locations el ON q.end_location_id = el.id
GROUP BY q.id, q.title, q.status, q.difficulty_level, b.title, sl.name, el.name;

-- active demigods
DROP VIEW IF EXISTS active_demigods;
CREATE VIEW active_demigods AS
SELECT
    c.id,
    c.name,
    c.age,
    g.name AS godly_parent,
    cab.cabin_number,
    COUNT(DISTINCT qp.quest_id) AS quests_completed,
    COUNT(DISTINCT cp.power_id) AS power_count,
    w.name AS primary_weapon
FROM characters c
JOIN gods g ON c.parent_god_id = g.id
LEFT JOIN cabins cab ON c.cabin_id = cab.id
LEFT JOIN quest_participants qp ON c.id = qp.character_id
LEFT JOIN character_powers cp ON c.id = cp.character_id
LEFT JOIN weapons w ON c.id = w.owner_id
WHERE c.status = 'alive'
GROUP BY c.id, c.name, c.age, g.name, cab.cabin_number, w.name;