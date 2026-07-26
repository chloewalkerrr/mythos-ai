-- views for percy jackson database
-- chloe walker

-- character power summary
CREATE VIEW character_power_summary AS
SELECT 
    c.name,
    g.name as god_parent,
    COUNT(cp.power_id) as power_count
FROM characters c
LEFT JOIN gods g ON c.parent_god_id = g.id
LEFT JOIN character_powers cp ON c.id = cp.character_id
GROUP BY c.id;

-- quest statistics
CREATE VIEW quest_statistics AS
SELECT 
    q.title,
    q.status,
    COUNT(qp.character_id) as participants
FROM quests q
LEFT JOIN quest_participants qp ON q.id = qp.quest_id
GROUP BY q.id;

-- active demigods
CREATE VIEW active_demigods AS
SELECT 
    c.name,
    c.age,
    g.name as god_parent,
    c.status
FROM characters c
LEFT JOIN gods g ON c.parent_god_id = g.id
WHERE c.status = 'alive';