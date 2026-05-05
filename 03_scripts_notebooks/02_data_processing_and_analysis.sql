-- ==============================================================================
-- WORLD OF WARSHIPS MONETIZATION CASE STUDY
-- Phase 3 & 4: Data Processing and Analysis
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. CREATE MASTER SUMMARY TABLE
-- This query combines static ship traits with player performance stats, remvoing
-- any unmatched ships that were removed during cleaning.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE `portfolio-case-studies-495322.wows_case_study.master_ship_summary` AS
SELECT
 i.ship_id,
 i.name AS ship_name,
 i.is_premium,
 i.tier,
 i.event,
 i.nation,
 i.type,
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
 i.event,
 i.nation,
 i.type;

-- ------------------------------------------------------------------------------
-- 2. EVENT ENGAGEMENT
-- This query identifies which events drive the highest engagement.
-- ------------------------------------------------------------------------------
SELECT 
 event,
 SUM(total_battles) as total_event_battles
FROM `portfolio-case-studies-495322.wows_case_study.master_ship_summary`
WHERE event != 'Standard'
GROUP BY event
ORDER BY total_event_battles DESC;

-- ------------------------------------------------------------------------------
-- 3. OWNERSHIP PROXY
-- This query identifies which premium ships are played the most.
-- ------------------------------------------------------------------------------
SELECT
 ship_name,
 SUM(total_battles) as total_ship_battles
FROM `portfolio-case-studies-495322.wows_case_study.master_ship_summary`
WHERE is_premium = TRUE
GROUP BY ship_name
ORDER BY total_ship_battles DESC;

-- ------------------------------------------------------------------------------
-- 4. TECH TREE / STANDARD SHIP USAGE
-- This query identifies which tech tree (not premium) ships, not obtained during
-- a special event are played the most.
-- ------------------------------------------------------------------------------
SELECT
 ship_name,
 SUM(total_battles) as total_ship_battles
FROM `portfolio-case-studies-495322.wows_case_study.master_ship_summary`
WHERE event = 'Standard' AND is_premium = FALSE
GROUP BY ship_name
ORDER BY total_ship_battles DESC;

-- ------------------------------------------------------------------------------
-- 5. IN-GAME PERFORMANCE (PREMIUM VS TECH TREE)
-- This query uses CTEs to compare the performance of specific Premium ships 
-- against the aggregated average of their exact Tech Tree counterparts 
-- (matched by tier, nation, and class).
-- ------------------------------------------------------------------------------
WITH premium_stats AS (
  SELECT
    ship_name,
    tier,
    nation,
    type,
    SAFE_DIVIDE(SUM(total_wins), SUM(total_battles)) AS prem_win_rate,
    SAFE_DIVIDE(SUM(total_damage_dealt), SUM(total_battles)) AS prem_avg_damage,
    SAFE_DIVIDE(SUM(total_xp), SUM(total_battles)) AS prem_avg_xp
  FROM `portfolio-case-studies-495322.wows_case_study.master_ship_summary`
  WHERE is_premium = TRUE
  GROUP BY ship_name, tier, nation, type
),

tech_tree_stats AS (
  SELECT
    tier,
    nation,
    type,
    SAFE_DIVIDE(SUM(total_wins), SUM(total_battles)) AS tt_win_rate,
    SAFE_DIVIDE(SUM(total_damage_dealt), SUM(total_battles)) AS tt_avg_damage,
    SAFE_DIVIDE(SUM(total_xp), SUM(total_battles)) AS tt_avg_xp
  FROM `portfolio-case-studies-495322.wows_case_study.master_ship_summary`
  WHERE is_premium = FALSE AND event = 'Standard'
  GROUP BY tier, nation, type
)

SELECT
  p.ship_name,
  p.tier,
  p.nation,
  p.type,
  p.prem_win_rate,
  t.tt_win_rate,
  p.prem_avg_damage,
  t.tt_avg_damage,
  p.prem_avg_xp,
  t.tt_avg_xp
FROM premium_stats p
INNER JOIN tech_tree_stats t
  ON p.tier = t.tier
  AND p.nation = t.nation
  AND p.type = t.type
ORDER BY 
  p.tier DESC, 
  p.nation, 
  p.type,
  p.ship_name;