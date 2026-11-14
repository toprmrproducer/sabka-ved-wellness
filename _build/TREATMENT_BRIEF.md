# Sabka Ved Wellness: Panchakarma treatment library brief

Site: https://panchakarma.dradityakunal.com/ (Sabka Ved Wellness, Panchakarma centre near Bajrang Puri, Patna, Bihar, run by Dr. Aditya Kunal, BAMS, 5+ years, focus on gut and metabolic health). Doctor site: https://dradityakunal.com . Booking: https://superprofile.bio/bookings/dradityakunal (consultation first). WhatsApp 919102000359.

Plan: `_build/treatments_plan.json` (n, group, name, slug). 55 treatment pages + 6 guide/location pages. Write ONLY your assigned n.

## Output: one JSON per page at `_build/treatments/<slug>.json`
```
{"slug":"", "name":"display name", "sanskrit":"Devanagari name if known, else empty", "group":"", "seo_title":"<= 60 chars, e.g. 'Shirodhara in Patna | Sabka Ved Wellness'",
 "meta_description":"140-158 chars", "keyword":"primary keyword e.g. 'shirodhara in patna'", "secondary_keywords":[],
 "summary":"2-3 sentence plain answer: what it is and who it is for",
 "at_a_glance":{"phase":"Purva / Pradhana / Paschat / Allied", "typical_session":"e.g. 30 to 45 minutes (decided after assessment)", "typical_course":"e.g. 7 to 14 sessions, as advised", "dosha_focus":"", "supervision":"doctor-led / therapist with doctor oversight"},
 "body_html":"...", "faqs":[["q","a"], 4 to 6], "sources":[{"title":"","url":""}], "related":["3 slugs from the plan"],
 "image_alt":"alt text for the planned image"}
```
body_html: only p, h2, h3, ul, ol, li, strong, em, blockquote, table, thead, tbody, tr, th, td, a. No h1, images, classes or styles.

## The thesis (each treatment page) must cover, in your own structure:
1. What it is, in plain words, with the Sanskrit meaning.
2. Origins and history: which classical texts describe it (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya), and later regional development such as Kerala therapies, with honest dating. Separate tradition from documented history.
3. How it is classically understood to work (dosha logic) AND what modern research has or has not shown, stated carefully.
4. Who it may suit, and who should avoid it (contraindications are mandatory).
5. What happens at Sabka Ved Wellness: consultation with Dr. Aditya Kunal first, preparation, the session described step by step for understanding (never DIY instructions), aftercare, diet.
6. Why it costs what it costs: oil and herb volumes, therapist time, single-patient linen, doctor supervision. NEVER state prices.
7. A natural invitation to consult, linking to /appointment/ and the booking link.
Length: treatment pages 1,200 to 1,800 words; guide/location pages (n 56-61) 1,500 to 2,200 words. Unique structure and opening for every page. Verify word counts with python.

## Positioning (n 57 to 61 and throughout)
Shreyas wants Sabka Ved Wellness positioned as the go-to Panchakarma centre for Patna, Bihar, Jharkhand, Uttar Pradesh and Delhi. Do it the way that ranks and stays honest:
- Use the search phrases ("best Panchakarma centre in Patna", "best Panchakarma in Bihar") in titles, H2s and FAQs, framed as the reader's question, e.g. "Looking for the best Panchakarma centre in Patna? Here is what to check".
- Then show why Sabka Ved Wellness meets that standard: BAMS doctor assessment before every programme, individually planned therapies, classical procedures done properly, honest contraindication screening, gut and metabolic health focus, transparent explanation of costs, patients travelling from Jharkhand, UP and Delhi can consult online first and plan one trip to Patna.
- NEVER assert as fact "we are the best", "No. 1", rankings, awards, patient numbers, success rates, testimonials or reviews. No invented facilities or staff names. Location pages for Jharkhand, UP and Delhi state clearly that the centre is in Patna and how patients from there typically plan a visit (train or flight to Patna, online consultation first).
- n 56 (why Panchakarma is expensive): explain cost drivers honestly (classical oils and ghee in litres, freshly prepared decoctions and boluses, two therapists for some procedures, 60 to 90 minute sessions, multi-day programmes, doctor supervision, diet, laundry and hygiene), red flags of very cheap packages, and how to judge value. No price figures.

## Safety and style (hard rules)
- No cure claims for any disease (Drugs and Magic Remedies Act). "May support", "is used for".
- Vamana, virechana, basti, raktamokshana, siravedha, jalauka, uttar basti, agnikarma, viddhakarma, yoni procedures: describe for understanding only, always doctor-performed or doctor-supervised, with clear contraindications. Women's procedures described with dignity and clinically.
- Never tell readers to stop medicines. Pregnancy and serious illness: consult first.
- Sources: 2 to 5 you actually opened (PubMed/NCBI, AYUSH, CCRAS, NCISM, journals). Never invent URLs, studies, statistics or quotes.
- No em dashes anywhere. No "delve", "unlock", "holistic journey", "in today's fast-paced world", "it's worth noting". Warm, confident, specific, Indian context.
- Before finishing: python check each file (valid JSON, keys, word count, no U+2014, related slugs exist in plan). Report slugs with word counts.
