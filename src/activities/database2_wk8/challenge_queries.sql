
-- 1. List all countries in the database
SELECT country FROM Country;

-- 2. Retrieve all games with their year and type
SELECT year, type FROM Games;

-- 3. Find all disabilities recorded in the database
SELECT description FROM Disability;

-- 4. Get all games that took place after the year 2000
SELECT year, type FROM Games WHERE year > 2000;

-- 5. Find all teams from a specific country (e.g., 'Canada')
SELECT name, code FROM Team
JOIN Country ON Team.country_id = Country.id
WHERE Country.country = 'Canada';

-- 6. List all hosts located in a specific country (e.g., 'Japan')
SELECT place_name FROM Host
JOIN Country ON Host.country_id = Country.id
WHERE Country.country = 'Japan';

-- 7. Show all games along with their host city and host country
SELECT Games.year, Games.type, Host.place_name, Country.country
FROM Games
JOIN GamesHost ON Games.id = GamesHost.games_id
JOIN Host ON GamesHost.host_id = Host.id
JOIN Country ON Host.country_id = Country.id;

-- 8. List all disabilities associated with each game
SELECT Games.year, Games.type, Disability.description
FROM Games
JOIN GamesDisability ON Games.id = GamesDisability.games_id
JOIN Disability ON GamesDisability.disability_id = Disability.id;

-- 9. Find all teams that participated in a specific game (e.g., year = 2016)
SELECT Team.name, Team.code
FROM Games
JOIN GamesTeam ON Games.id = GamesTeam.games_id
JOIN Team ON GamesTeam.team_id = Team.code
WHERE Games.year = 2016;

-- 10. Count how many teams participated in each game
SELECT Games.year, Games.type, COUNT(GamesTeam.team_id) AS team_count
FROM Games
JOIN GamesTeam ON Games.id = GamesTeam.games_id
GROUP BY Games.year, Games.type;
