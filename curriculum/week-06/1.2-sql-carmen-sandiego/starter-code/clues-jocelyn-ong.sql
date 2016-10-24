-- Clue #1: We recently got word that someone fitting Carmen Sandiego's description has been
-- traveling through Southern Europe. She's most likely traveling someplace where she won't be noticed,
-- so find the least populated country in Southern Europe, and we'll start looking for her there.

SELECT "name", "population"
FROM country
WHERE "region"='Southern Europe'
ORDER BY 2 ASC
LIMIT 5;

-- ANSWER: HOLY SEE (VATICAN CITY STATE)

-- Clue #2: Now that we're here, we have insight that Carmen was seen attending language classes in
-- this country's officially recognized language. Check our databases and find out what language is
-- spoken in this country, so we can call in a translator to work with you.

SELECT "language"
FROM countrylanguage
WHERE "countrycode" IN
(SELECT "code" FROM country WHERE "name" IN
(SELECT "name"
FROM country
WHERE "region"='Southern Europe'
ORDER BY "population" ASC
LIMIT 1));

-- ANSWER: ITALIAN

-- Clue #3: We have new news on the classes Carmen attended – our gumshoes tell us she's moved on
-- to a different country, a country where people speak only the language she was learning. Find out which
--  nearby country speaks nothing but that language.

SELECT cn."name" AS "name"
FROM country AS cn
JOIN (SELECT c."countrycode"
FROM countrylanguage c
JOIN (SELECT "countrycode", COUNT("language")
AS "count" FROM countrylanguage
GROUP BY 1 HAVING COUNT("language") = 1) AS sub
ON c."countrycode"=sub."countrycode"
WHERE c."language"='Italian'
AND sub."count"=1) AS sub2
ON cn."code"=sub2."countrycode"
WHERE cn."name" NOT IN
(SELECT "name"
FROM country
WHERE "region"='Southern Europe'
ORDER BY "population" ASC
LIMIT 1);

-- ANSWER: SAN MARINO

-- Clue #4: We're booking the first flight out – maybe we've actually got a chance to catch her this time.
-- There are only two cities she could be flying to in the country. One is named the same as the country – that
-- would be too obvious. We're following our gut on this one; find out what other city in that country she might
--  be flying to.

SELECT city."name"
FROM city
WHERE city."countrycode" LIKE
(SELECT country."code" FROM country WHERE country."name" LIKE '%Marino')
AND city."name" NOT LIKE '%Marino';

-- ANSWER: SERRAVALLE

-- Clue #5: Oh no, she pulled a switch – there are two cities with very similar names, but in totally different
-- parts of the globe! She's headed to South America as we speak; go find a city whose name is like the one we were
-- headed to, but doesn't end the same. Find out the city, and do another search for what country it's in. Hurry!

SELECT city."name", city."countrycode"
FROM city
WHERE city."countrycode"
IN (SELECT country."code"
FROM country
WHERE "region"='South America')
AND city."name" LIKE 'Serr%';

SELECT "name"
FROM country
WHERE "code" LIKE 'BRA';

-- ANSWER: SERRA, BRA (BRAZIL)

-- Clue #6: We're close! Our South American agent says she just got a taxi at the airport, and is headed towards
 -- the capital! Look up the country's capital, and get there pronto! Send us the name of where you're headed and we'll
 -- follow right behind you!

SELECT city."name"
FROM city
WHERE city."id" =
(SELECT country."capital"
FROM country
WHERE country."name" LIKE 'Brazil');

-- Answer: Brasï¿½lia

-- Clue #7: She knows we're on to her – her taxi dropped her off at the international airport, and she beat us to
 -- the boarding gates. We have one chance to catch her, we just have to know where she's heading and beat her to the
 -- landing dock.

-- Clue #8: Lucky for us, she's getting cocky. She left us a note, and I'm sure she thinks she's very clever, but
-- if we can crack it, we can finally put her where she belongs – behind bars.

-- Our playdate of late has been unusually fun –
-- As an agent, I'll say, you've been a joy to outrun.
-- And while the food here is great, and the people – so nice!
-- I need a little more sunshine with my slice of life.
-- So I'm off to add one to the population I find
-- In a city of ninety-one thousand and now, eighty five.


-- We're counting on you, gumshoe. Find out where she's headed, send us the info, and we'll be sure to meet her at the gates with bells on.

SELECT city."name", city."countrycode"
FROM city
WHERE city."population" = 91084;

-- She's in SANTA MONICA, USA!
