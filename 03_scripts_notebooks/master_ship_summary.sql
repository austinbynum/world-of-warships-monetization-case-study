SELECT
 i.ship_id,
 i.name AS ship_name,
 i.is_premium,
 i.tier,
 i.category,
 SUM(s.battles) AS total_battles,
 SUM(s.wins) AS total_wins,
 SUM(s.damage_dealt) AS total_damage_dealt,
 SUM(s.frags) AS total_frags,
 SUM(s.xp) AS total_xp,
 SUM(s.survived_battles) AS total_survived_battles
FROM `portfolio-case-studies-495322.wows_case_study.stats` s
INNER JOIN `portfolio-case-studies-495322.wows_case_study.info` i
ON s.ship_id = i.ship_id
GROUP BY 
 i.ship_id,
 ship_name,
 i.is_premium,
 i.tier,
 i.category