"""All site copy for Sabka Ved Wellness. Facts only from the brief: no invented staff, numbers, prices,
phone, hours or reviews. No em dashes."""

BRAND = 'Sabka Ved Wellness'
DOCTOR = 'Dr. Aditya Kunal'
DOCTOR_FULL = 'Dr. Aditya Kunal, BAMS'
DOCTOR_SITE = 'https://dradityakunal.com/'
PLACE = 'Near Bajrang Puri, Patna, Bihar'
SITE_URL = 'https://panchakarma.dradityakunal.com/'
PHONE = '+919102000359'
PHONE_DISPLAY = '+91 91020 00359'
WA_LINK = 'https://wa.me/919102000359'
BOOKING_URL = 'https://superprofile.bio/bookings/dradityakunal'
MAP_EMBED = 'https://www.google.com/maps?q=Bajrangpuri,+Patna,+Bihar&output=embed'
SOCIAL = [('Instagram', 'https://www.instagram.com/dr_aditya_kunal/'),
          ('YouTube', 'https://www.youtube.com/@dr_aditya_kunal'),
          ('Facebook', 'https://www.facebook.com/dr_aditya_kunal')]
NAP_NAME = 'Sabka Ved Wellness'
NAP_ADDRESS = 'near Bajrang Puri, Patna, Bihar'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Bajrang+Puri+Patna+Bihar'

CONTRA = ('Panchakarma is usually avoided or postponed during pregnancy, acute fever or infection, '
          'severe weakness, and in some heart conditions.')

THERAPIES = [
    dict(
        slug='panchakarma-consultation', name='Panchakarma Consultation', short='Consultation',
        category='First step', session='Typically 30 to 45 min',
        summary='Nadi pariksha, prakriti assessment and a full health history with Dr. Aditya Kunal. '
                'Every programme starts here, and so does the decision on whether Panchakarma suits you.',
        expect=['The consultation is an unhurried conversation. Dr. Aditya Kunal asks about your health history, '
                'current medicines, digestion, sleep, appetite, work and daily routine, then reads the pulse '
                '(nadi pariksha) and assesses your prakriti and present imbalance.',
                'At the end you receive a clear recommendation. That may be a full Panchakarma programme, a few '
                'supportive therapies, diet and routine changes only, or advice to wait. If Panchakarma is not '
                'right for you now, you will be told plainly and why.'],
        whofor='Anyone considering Panchakarma or an Ayurvedic therapy, and families who want to understand '
               'what is suitable for an elder or a member with an ongoing condition. Bring your prescriptions '
               'and recent reports.',
        list_title='Please bring',
        items=['Your current prescriptions', 'Recent blood reports, if any', 'A list of supplements you take',
               'Questions you want answered', 'A family member, if you like', 'An empty stomach is not needed'],
        img='doctor-consult-desk-wide', img2='doctor-with-patient-wide', img3='doctor-clinic-nehru-jacket'),
    dict(
        slug='vamana', name='Vamana', short='Vamana', category='Classical five',
        session='Main day typically half a day',
        summary='Therapeutic emesis, the classical procedure for conditions of Kapha. Done only after days of '
                'preparation and only when the assessment clearly supports it.',
        expect=['Vamana is never a single-day event. It is preceded by several days of internal oleation '
                '(snehapana) and steam (swedana) to prepare the body, with the exact number of days decided by '
                'the doctor according to your response.',
                'On the main day the procedure is carried out in the morning under the doctor\'s supervision, '
                'followed by rest and observation. A graded diet (samsarjana krama) over the following days lets '
                'digestion return gently. The full sequence is planned and explained before you begin.'],
        whofor='Vamana is considered for selected Kapha-dominant conditions in people with adequate strength. '
               'It is not suitable for everyone, and the decision is made only after assessment.',
        list_title='Usually not suitable during',
        items=['Pregnancy', 'Acute fever or infection', 'Severe weakness or exhaustion', 'Some heart conditions',
               'Very young or very elderly age', 'Bleeding disorders'],
        img='doctor-preparing-herbs', img2='stock-golden-milk-spices', img3='doctor-dispensary-herbs'),
    dict(
        slug='virechana', name='Virechana', short='Virechana', category='Classical five',
        session='Main day typically half a day',
        summary='Therapeutic purgation, the classical procedure for conditions of Pitta. Prepared with oleation '
                'and steam, then followed by a careful recovery diet.',
        expect=['Like every classical procedure, Virechana follows a sequence. Internal oleation and steam '
                'prepare the body over several days, and the doctor decides when you are ready for the main day.',
                'On the main day a prescribed herbal preparation is taken in the morning and you rest while the '
                'therapy works, with guidance on fluids and food. A graded diet follows for the next few days so '
                'the body settles before normal meals return.'],
        whofor='Virechana is considered for selected Pitta-related conditions and for seasonal cleansing in people '
               'with adequate strength, only when the assessment supports it.',
        list_title='Usually not suitable during',
        items=['Pregnancy', 'Acute fever or diarrhoea', 'Severe weakness or dehydration', 'Some heart conditions',
               'Recent surgery', 'Rectal bleeding or prolapse'],
        img='doctor-dispensary-herbs', img2='stock-herbs-capsules', img3='doctor-preparing-herbs'),
    dict(
        slug='basti', name='Basti', short='Basti', category='Classical five',
        session='Typically 30 to 45 min per session',
        summary='Medicated enema therapy with oils or herbal decoctions, given as a planned course. Classically '
                'regarded as the principal therapy for Vata.',
        expect=['Basti is given as a course rather than a single session. Oil-based (anuvasana) and '
                'decoction-based (niruha) bastis are alternated in a schedule set by the doctor, usually after a '
                'gentle oil massage and steam.',
                'Each session is short, followed by rest. The length of the course, from a few days to a few weeks, '
                'depends on your condition and how your body responds, and it is reviewed as you go.'],
        whofor='Basti is considered for selected Vata-related complaints, such as some joint, back and digestive '
               'concerns, after assessment. It is not a general detox and is not suitable for everyone.',
        list_title='Usually not suitable during',
        items=['Pregnancy', 'Acute fever or diarrhoea', 'Rectal bleeding or fissure', 'Severe weakness',
               'Some heart conditions', 'Recent abdominal surgery'],
        img='doctor-with-patient-wide', img2='doctor-manuscript-desk', img3='doctor-portrait-white-coat'),
    dict(
        slug='nasya', name='Nasya', short='Nasya', category='Classical five',
        session='Typically 20 to 30 min',
        summary='Administration of medicated oil or ghee through the nose, after a gentle face and neck massage and '
                'steam. Usually given as a short course.',
        expect=['A session begins with a light massage of the face, head and neck, followed by mild steam. The '
                'prescribed medicated oil or ghee is then placed in the nostrils while you lie back, and you rest '
                'for a few minutes afterwards.',
                'Nasya is usually prescribed as a short course, and you will be told what to avoid on those days, '
                'such as cold drinks, head baths and dust. Related head and eye therapies such as Netra Tarpana '
                'may be suggested alongside when appropriate.'],
        whofor='Nasya is considered for selected concerns of the head, neck and sinuses, after assessment. '
               'It is not given during an active cold with fever.',
        list_title='Usually not suitable during',
        items=['Pregnancy', 'Acute cold with fever', 'Immediately after meals', 'Right after a head bath',
               'Severe weakness', 'Some heart conditions'],
        img='stock-herbs-capsules', img2='doctor-green-kurta-herbs', img3='doctor-manuscript-desk'),
    dict(
        slug='raktamokshana', name='Raktamokshana', short='Raktamokshana', category='Classical five',
        session='Decided after assessment',
        summary='Classical bloodletting therapy, considered only in selected cases. Whether it is appropriate, '
                'and which method, is decided strictly after the doctor\'s assessment.',
        expect=['Raktamokshana is the most selective of the five classical procedures. The classical texts '
                'describe more than one method, and the choice depends on your condition, your strength and your '
                'other medical history.',
                'If it is considered suitable, the procedure, the precautions and the aftercare are explained '
                'fully before anything is done. For many people a different therapy is the better choice, and you '
                'will be told so.'],
        whofor='Raktamokshana is considered only for specific conditions where the doctor judges it appropriate. '
               'It is never offered as a routine or general wellness therapy.',
        list_title='Not suitable with',
        items=['Pregnancy', 'Anaemia or severe weakness', 'Bleeding disorders', 'Blood-thinning medicines',
               'Some heart conditions', 'Acute fever or infection'],
        img='doctor-manuscript-desk', img2='doctor-consult-desk-wide', img3='doctor-clinic-nehru-jacket'),
    dict(
        slug='abhyanga', name='Abhyanga', short='Abhyanga', category='Supportive therapy',
        session='Typically 45 to 60 min',
        summary='Full-body massage with warm medicated oil, chosen for your constitution. Often followed by '
                'Swedana, and a part of most Panchakarma preparations.',
        expect=['Warm medicated oil, selected after your consultation, is applied over the whole body with steady, '
                'rhythmic strokes. A session is usually followed by Swedana, a herbal steam that helps the oil '
                'work deeper, and then rest.',
                'Abhyanga is used on its own or as the external preparation (snehana) before a main procedure. '
                'Pizhichil, where warm oil is poured continuously while the body is gently massaged, may be '
                'recommended as a more intensive form when suitable.'],
        whofor='Abhyanga suits many adults as supportive care, especially in dry and cold seasons. It is still '
               'planned after a consultation, as the oil and pressure are chosen for you.',
        list_title='Usually postponed during',
        items=['Acute fever', 'Indigestion or a heavy stomach', 'Skin infections or open wounds',
               'Right after meals', 'Some heart conditions', 'Pregnancy, unless advised'],
        img='stock-shoulder-massage', img2='doctor-green-kurta-herbs', img3='doctor-dispensary-herbs'),
    dict(
        slug='shirodhara', name='Shirodhara', short='Shirodhara', category='Supportive therapy',
        session='Typically 30 to 45 min',
        summary='A steady stream of warm medicated oil, buttermilk or decoction poured over the forehead while '
                'you lie still. Calm, quiet and carefully timed.',
        expect=['You lie comfortably with your eyes covered while a thin, continuous stream of the prescribed '
                'liquid flows across the forehead. The temperature, the liquid and the duration are set by the '
                'doctor after your consultation.',
                'A short head massage usually follows, then rest. You will be advised to avoid cold wind, a head '
                'bath and heavy meals for the rest of the day.'],
        whofor='Shirodhara is often chosen as supportive care for stress, poor sleep and mental fatigue, '
               'alongside other treatment and after assessment. It does not replace care from your regular doctor.',
        list_title='Usually postponed during',
        items=['Acute cold, sinus block or fever', 'Recent head or neck injury', 'Scalp infection',
               'Very low blood pressure', 'Pregnancy, unless advised', 'Some heart conditions'],
        img='doctor-green-kurta-herbs', img2='stock-golden-milk-spices', img3='doctor-portrait-white-coat'),
    dict(
        slug='kati-basti-janu-basti', name='Kati Basti and Janu Basti', short='Kati, Janu and Greeva Basti',
        category='Supportive therapy', session='Typically 30 to 45 min',
        summary='Warm medicated oil held in a ring of dough over the lower back, knee or neck. Local care that is '
                'often part of a wider plan for joint and back complaints.',
        expect=['A ring of black gram dough is shaped on the skin over the area, then filled with warm medicated '
                'oil that is kept at a steady temperature for the session. Kati Basti is for the lower back, '
                'Janu Basti for the knees and Greeva Basti for the neck.',
                'The oil is then removed, the area gently massaged and sometimes given local steam. These are '
                'usually given over several consecutive days as part of the plan made at your consultation.'],
        whofor='These therapies are considered as supportive care for stiffness and discomfort in the back, knees '
               'or neck, after assessment. Any underlying condition stays under your regular doctor\'s care.',
        list_title='Usually postponed with',
        items=['Fresh injury or swelling', 'Open wounds or skin infection', 'Acute fever', 'Recent fracture',
               'Severe pain without a diagnosis', 'Pregnancy, for Kati Basti'],
        img='doctor-portrait-white-coat', img2='stock-shoulder-massage', img3='doctor-with-patient-wide'),
    dict(
        slug='udvartana', name='Udvartana', short='Udvartana', category='Supportive therapy',
        session='Typically 30 to 45 min',
        summary='A brisk massage with dry herbal powders in upward strokes. Light and invigorating, often '
                'suggested for Kapha and as part of a weight and lifestyle plan.',
        expect=['Warm, dry herbal powder is massaged into the skin with firm upward strokes, against the direction '
                'of the hair. The session is usually followed by steam and a warm bath after some time.',
                'Udvartana is usually given as a short course and works best alongside the diet and daily routine '
                'suggested at your consultation. It is not a stand-alone weight-loss treatment.'],
        whofor='Udvartana is considered for people with a Kapha tendency, heaviness and sluggishness, after '
               'assessment. It is not suitable for very dry or sensitive skin.',
        list_title='Usually not suitable with',
        items=['Very dry or sensitive skin', 'Skin infections or wounds', 'Pregnancy', 'Acute fever',
               'Severe weakness', 'Some heart conditions'],
        img='stock-turmeric', img2='doctor-preparing-herbs', img3='doctor-green-kurta-herbs'),
]

THERAPY_OPTIONS = ['Panchakarma consultation (nadi pariksha)', 'Vamana', 'Virechana', 'Basti', 'Nasya',
                   'Raktamokshana', 'Abhyanga', 'Swedana', 'Shirodhara', 'Kati Basti', 'Janu Basti',
                   'Greeva Basti', 'Netra Tarpana', 'Pizhichil', 'Udvartana', 'Not sure yet, please advise']

FAQ = [
    ('How do I book a consultation?',
     'Send a request through the appointment page with your preferred date and the therapy you are interested '
     'in. Every visit is by appointment, near Bajrang Puri, Patna, and your slot is confirmed directly by the '
     'clinic before you travel.'),
    ('How long does a Panchakarma programme take?',
     'It depends on you. A supportive therapy such as Abhyanga or Shirodhara typically takes 30 to 60 minutes. '
     'A full programme with preparation, main therapy and recovery typically runs from about one to three weeks. '
     'The exact length is decided after assessment.'),
    ('Is Panchakarma safe?',
     'Panchakarma is a structured medical procedure, not a spa routine. It is planned only after Dr. Aditya '
     'Kunal assesses you, and the intensity is adjusted to your strength. It is not suitable for everyone, which '
     'is why no therapy starts without a consultation.'),
    ('Who should avoid Panchakarma?',
     CONTRA + ' Young children and frail elders need special care. If you have a serious or ongoing condition, '
     'your regular doctor stays in charge of it, and we work alongside, never instead.'),
    ('Do I stop my regular medicines?',
     'No. Never stop or change a prescribed medicine without the doctor who prescribed it. Bring your '
     'prescriptions to the consultation so your plan is made around them.'),
    ('What should I eat during Panchakarma?',
     'Light, warm, freshly cooked food such as khichdi, moong dal and rice, with warm water through the day. '
     'Specific diet instructions are given for each phase, and they matter as much as the therapy itself.'),
]

FIRST_VISIT = [
    ('Step 01', 'Conversation',
     'We begin by listening: your health history, current medicines, digestion, sleep and daily routine, '
     'in your own words.', 'doctor-consult-desk-wide', (0.62, 0.45)),
    ('Step 02', 'Nadi pariksha',
     'Pulse assessment and a careful look at your prakriti. This is where the doctor decides whether '
     'Panchakarma suits you at all.', 'doctor-with-patient-wide', (0.58, 0.5)),
    ('Step 03', 'Your plan',
     'If Panchakarma is right for you, you receive a clear plan: preparation, main therapy, diet and recovery. '
     'If it is not, you are told plainly.', 'doctor-preparing-herbs', (0.6, 0.45)),
    ('Step 04', 'Follow-up',
     'Progress is reviewed through the programme, and therapies are adjusted or paused whenever your body '
     'asks for it.', 'doctor-dispensary-herbs', (0.7, 0.4)),
]

POSTS = [
    dict(
        slug='what-is-panchakarma-explained-simply', title='What is Panchakarma, explained simply',
        category='Ayurveda Basics', date='November 12, 2026', iso='2026-11-12',
        desc='A plain-language guide to Panchakarma: the five classical therapies, the three phases and who it '
             'is and is not for, from Sabka Ved Wellness in Patna.',
        img='doctor-dispensary-herbs', focus=(0.68, 0.4), feat='doctor-preparing-herbs', ffocus=(0.62, 0.45),
        intro='Panchakarma literally means five actions. It is the classical Ayurvedic system of procedures used to '
              'restore balance in the body, and it is very different from the spa packages that often borrow '
              'its name. Here is what it actually involves, in plain words.',
        h2='Five procedures, chosen for one person',
        h2p=['The five classical procedures are Vamana (therapeutic emesis), Virechana (therapeutic purgation), '
             'Basti (medicated enema), Nasya (nasal therapy) and Raktamokshana (bloodletting). Nobody receives all '
             'five. The doctor chooses what suits your body, your condition and the season, and sometimes the '
             'right answer is none of them.',
             'Around these sit supportive therapies such as Abhyanga, Swedana and Shirodhara, which prepare the '
             'body or support recovery.'],
        mid_title='The three phases of every programme',
        blocks=[('1. Purvakarma: preparation',
                 'Internal and external oleation with medicated ghee or oil, followed by steam. This prepares the '
                 'body for the main procedure and usually takes several days.', None),
                ('2. Pradhanakarma: the main therapy', None,
                 ['Done under the doctor\'s supervision', 'Chosen after assessment, never from a menu',
                  'Timed to your strength and response', 'Explained to you before it begins']),
                ('3. Paschatkarma: recovery',
                 'A graded diet and routine (samsarjana krama) let digestion and energy return gently. Skipping '
                 'this phase undoes much of the work.', None)],
        end_h='Who it is not for',
        end_p=CONTRA + ' Serious conditions stay with your regular doctor. Panchakarma is planned only after a '
              'consultation, which is the right first step for anyone curious about it.'),
    dict(
        slug='how-to-prepare-for-panchakarma', title='How to prepare for Panchakarma',
        category='Before You Begin', date='November 8, 2026', iso='2026-11-08',
        desc='Practical steps to prepare for Panchakarma in Patna: what to bring to the consultation, how to plan '
             'your days, food, rest and your regular medicines.',
        img='stock-golden-milk-spices', focus=(0.5, 0.45), feat='doctor-consult-desk-wide', ffocus=(0.62, 0.45),
        intro='Good preparation makes Panchakarma smoother and safer. Most of it is simple: honest information for '
              'the doctor, a lighter routine and enough time set aside. This is how families in Patna usually '
              'plan for it.',
        h2='Start with the consultation',
        h2p=['Bring your prescriptions, recent blood reports and a list of any supplements. Tell the doctor about '
             'past surgeries, pregnancy or the possibility of it, and any heart, blood pressure or sugar concerns.',
             'Never stop a prescribed medicine on your own. Your plan is made around your medicines, together with '
             'the doctor who prescribed them.'],
        mid_title='Planning your days around the programme',
        blocks=[('1. Choose the right time',
                 'Seasons matter in Ayurveda. The doctor may suggest a particular time of year for a particular '
                 'procedure, as part of ritucharya, the seasonal routine.', None),
                ('2. Clear your calendar', None,
                 ['Avoid travel during the programme', 'Keep work light on main therapy days',
                  'Plan for early nights and rest', 'Arrange a family member for support if needed']),
                ('3. Eat lighter in the days before',
                 'Warm, simple, home-cooked food is ideal. Cut down on fried food, outside meals, alcohol and '
                 'very late dinners, unless advised otherwise.', None)],
        end_h='Ask every question you have',
        end_p='You should know what will happen each day before it happens. If anything in your plan is unclear, '
              'ask at the consultation. A well-informed patient is part of what keeps Panchakarma safe.'),
    dict(
        slug='panchakarma-vs-spa-massage', title='Panchakarma vs a spa massage: the real difference',
        category='Clear Answers', date='November 3, 2026', iso='2026-11-03',
        desc='Why Panchakarma is a doctor-planned medical procedure and not a spa massage: assessment, '
             'sequence, supervision and aftercare explained by Sabka Ved Wellness, Patna.',
        img='stock-shoulder-massage', focus=(0.5, 0.45), feat='doctor-with-patient-wide', ffocus=(0.55, 0.5),
        intro='Many places in every city offer a "Panchakarma package" that turns out to be an oil massage. A '
              'relaxing massage has its place, but it is not Panchakarma. Here is the difference, so you know '
              'what to ask before you book anywhere.',
        h2='A spa starts with a menu. Panchakarma starts with a doctor.',
        h2p=['At a spa you pick a treatment. In Panchakarma, an Ayurvedic physician first takes your history, '
             'reads the pulse and assesses your constitution and present imbalance. Only then is a plan made, and '
             'it may not include the therapy you came in asking for.',
             'Classical procedures such as Vamana, Virechana and Basti are medical interventions with real '
             'precautions. They need supervision and a recovery plan.'],
        mid_title='Four questions to ask before you book',
        blocks=[('1. Who assesses me first?',
                 'A qualified Ayurvedic doctor should see you before any therapy is chosen, and should be willing to '
                 'say no.', None),
                ('2. Is there a full sequence?', None,
                 ['Preparation with oleation and steam', 'A main procedure chosen for you',
                  'A graded recovery diet afterwards', 'Review of how you are responding']),
                ('3. What happens if it is not right for me?',
                 'A good centre will tell you plainly that Panchakarma is not suitable, and suggest something '
                 'gentler, or nothing at all.', None)],
        end_h='Where massage fits in',
        end_p='Abhyanga, the Ayurvedic oil massage, is valuable supportive care and part of many programmes. It '
              'is simply one piece. At Sabka Ved Wellness every therapy, including massage, is planned after a '
              'consultation with Dr. Aditya Kunal.'),
]
