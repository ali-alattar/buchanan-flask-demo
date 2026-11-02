"""Entirely fictional, hand-authored records for a local presentation.

No real firm, person, mandate, relationship or candidate is represented here.
Emails use .example; phone numbers use the UK 020 7946 0xxx or US 555-01xx
reserved fiction ranges. No records come from Bullhorn, news feeds or AI.
Assessment is a fixed 2 November 2026 snapshot, not a claim of live freshness.
"""

AS_OF = "2026-11-02"


def factors(hiring, access, delivery):
    return {
        "hiring": dict(zip(("requirement", "activity", "growth", "gap", "timing"), hiring, strict=True)),
        "access": dict(zip(("relationship", "route", "history", "position"), access, strict=True)),
        "delivery": dict(zip(("supply", "pay", "location", "availability"), delivery, strict=True)),
    }


def contact(name, title, firm, email, phone):
    return dict(name=name, title=title, firm=firm, email=email, phone=phone)


def evidence(event_id, date, source, title, relevance, kind="context", source_count=1):
    # One record per underlying event, even if it has several articles.
    return dict(event_id=event_id, date=date, source=source, title=title,
                relevance=relevance, kind=kind, source_count=source_count)


def candidate(name, level, experience, location, availability, verify):
    return dict(name=name, level=level, experience=experience, location=location,
                availability=availability, verify=verify, reviewed="2026-10-30")


OPPORTUNITIES = [
    {
        "id": "alder-vale", "firm": "Alder & Vale", "monogram": "AV",
        "location": "London", "practice": "Private credit", "level": "4–7 years PQE",
        "status": "confirmed", "status_label": "Confirmed requirement",
        "summary": "An approved search, with a clear route in.",
        "window": "Search open now", "start": "January–March 2027",
        "owner": "Sophie Bennett", "updated": "2026-10-30", "restriction": None,
        "briefing": [
            "Helen has confirmed budget for a 4–7 PQE private-credit associate after a departure left an unfilled gap. Six mandates against a comparable three-matter baseline support the capacity concern; the approved search is the stronger signal.",
            "Sophie’s current relationship with Helen and agreed supplier terms give Buchanan an accepted route to a competitive search. A recent finance placement provides relevant delivery experience.",
            "Two engaged London lawyers have sponsor-side lending experience. Their notice periods broadly fit a first-quarter start; checking pay flexibility and permission to introduce them would make the next conversation concrete.",
        ],
        "contact": contact("Helen Mercer", "Head of Legal Talent", "Alder & Vale", "helen.mercer@aldervale.example", "+44 20 7946 0132"),
        "evidence": [
            evidence("av-requirement", "2026-10-30", "Hiring-team call · Sophie Bennett", "Approved replacement search", "Helen confirmed budget, the 4–7 PQE brief and Buchanan’s supplier route. The search is active; desired start is Q1 2027.", "requirement"),
            evidence("av-mandates", "2026-10-28", "Team matter register · eight-week review", "Six distinct private-credit mandates", "Six unique matters versus an expected three from comparable 12-month coverage. Workload supports the discussion; it does not itself establish a vacancy."),
            evidence("av-team", "2026-10-27", "Client team review · Helen Mercer", "One associate gap remains", "The departing associate has not been replaced. Helen confirmed there is no separate growth programme."),
        ],
        "candidates": [
            candidate("Emma Whitfield", "5 years PQE", "Sponsor-side direct lending and unitranche transactions.", "London · England & Wales qualified", "Three-month notice; open to a Q1 move.", "Confirm pay flexibility above the current £155k base range."),
            candidate("Daniel Farrow", "6 years PQE", "Leveraged finance with a growing private-credit workload.", "London · England & Wales qualified", "Three-month notice; current interest checked.", "Confirm depth of borrower-side versus lender-side experience."),
        ],
        "candidate_note": "Both are open to exploring a move. Neither has authorised an introduction to this firm.",
        "factors": factors(
            [(1, "30 Oct call: budgeted, active requirement."), (1, "28 Oct review: six unique matters / three expected; uplift capped at 1."), (0, "27 Oct client review: no separate growth programme."), (1, "27 Oct: client confirms an unfilled replacement gap."), (1, "30 Oct: search open now, Q1 start agreed.")],
            [(1, "30 Oct: Sophie is discussing this team with Helen."), (1, "30 Oct: supplier process and terms confirmed."), (.75, "One relevant London finance placement in July."), (.5, "30 Oct: accepted route; competitive search.")],
            [(.75, "Two recently engaged, plausible candidates."), (.75, "£155k base range; one small negotiable gap."), (1, "Both London based and England & Wales qualified."), (.75, "Three-month notices broadly fit Q1; exact start needs agreement.")],
        ),
    },
    {
        "id": "marlowe-pierce", "firm": "Marlowe Pierce", "monogram": "MP",
        "location": "Miami", "practice": "Corporate / M&A", "level": "2019–2022 class years",
        "status": "confirmed", "status_label": "Confirmed requirement",
        "summary": "A growing sponsor practice with budget in place.",
        "window": "Search open now", "start": "By March 2027",
        "owner": "Oliver Nash", "updated": "2026-10-29", "restriction": None,
        "briefing": [
            "An approved associate search follows a committed expansion of the Miami sponsor team. Four attributed mandates versus three expected suggest modest growth; the hiring director has independently confirmed the need.",
            "Oliver is in an active discussion with Rafael and has an agreed agency route. One recent corporate placement adds credibility, although Buchanan is competing with other accepted suppliers.",
            "Two engaged Florida lawyers offer complementary sponsor-side experience and a plausible March start. The useful discussion is how much autonomous deal leadership the team expects, rather than the size of its latest buyout.",
        ],
        "contact": contact("Rafael Ellery", "Director of Attorney Recruiting", "Marlowe Pierce", "rafael.ellery@marlowepierce.example", "+1 305 555 0142"),
        "evidence": [
            evidence("mp-role", "2026-10-29", "Hiring director call · Oliver Nash", "Corporate associate budget approved", "Rafael confirmed an active Miami search for 2019–2022 class years and accepted Buchanan’s participation.", "requirement"),
            evidence("mp-expansion", "2026-10-22", "Firm practice announcement", "Miami sponsor practice investment", "The firm committed to expanding this specific team. The arriving partner and launch announcement are treated as one growth event."),
            evidence("mp-matters", "2026-10-28", "Office matter review · comparable coverage", "Four distinct mandates in eight weeks", "Against an expected three, the measured uplift is one third. This modest increase is supporting context, not a staffing conclusion."),
        ],
        "candidates": [
            candidate("Lucas Arden", "2020 class year", "Middle-market sponsor acquisitions; leads diligence workstreams.", "Miami · Florida admitted", "Eight weeks’ notice; March start feasible.", "Verify independent signing and closing responsibility."),
            candidate("Sofia Wren", "2021 class year", "Cross-border sponsor transactions and portfolio bolt-ons.", "Miami · Florida admitted", "Available from February 2027.", "Recheck bonus expectations against the base-and-bonus package."),
        ],
        "candidate_note": "Interest in the market is current. Firm-specific interest and permission to share details remain unconfirmed.",
        "factors": factors(
            [(1, "29 Oct: approved Miami search confirmed."), (1 / 3, "Four / three expected − 1; rounded contribution 6.67."), (1, "22 Oct: explicit Miami sponsor-team expansion."), (0, "29 Oct: hiring director confirmed no replacement gap."), (1, "Search active; start by March 2027.")],
            [(1, "29 Oct: Oliver and Rafael discussing this role."), (1, "29 Oct: terms and agency route agreed."), (.75, "One recent relevant corporate placement."), (.5, "Accepted, competitive supplier process.")],
            [(.75, "Two engaged, plausible Florida candidates."), (.75, "Base is aligned; bonus expectations need discussion."), (1, "Both prefer Miami and are Florida admitted."), (1, "Both can meet the March start window.")],
        ),
    },
    {
        "id": "calder-rowe", "firm": "Calder Rowe", "monogram": "CR",
        "location": "London", "practice": "Funds", "level": "3–6 years PQE",
        "status": "confirmed", "status_label": "Confirmed requirement",
        "summary": "A real opening; candidate coverage is narrower.",
        "window": "Search open now", "start": "February–April 2027",
        "owner": "Sophie Bennett", "updated": "2026-10-30", "restriction": None,
        "briefing": [
            "Priya has confirmed an approved funds associate role and a remaining departure gap. The team’s current matter run is at its usual level, so this is a replacement opportunity rather than a deal-volume story.",
            "Sophie’s recent check-in and an agreed supplier process create a credible route to Priya. Adjacent finance delivery helps, but Buchanan has less direct funds placement history here.",
            "One engaged funds lawyer has the right formation experience and a plausible spring start. Establishing the balance of primary funds and secondaries work will determine whether a wider shortlist is needed.",
        ],
        "contact": contact("Priya Hollis", "Senior Recruitment Manager", "Calder Rowe", "priya.hollis@calderrowe.example", "+44 20 7946 0248"),
        "evidence": [
            evidence("cr-role", "2026-10-30", "Hiring-team brief · Priya Hollis", "Approved funds associate replacement", "Priya confirmed budget, agency participation and a 3–6 PQE role. This is a hiring requirement, not an inference from a fund close.", "requirement"),
            evidence("cr-context", "2026-10-28", "Client capacity review", "Activity stable; replacement still outstanding", "Three mandates against three expected and no growth programme. The independent departure gap explains the role."),
        ],
        "candidates": [
            candidate("Clara Bellamy", "4 years PQE", "Private-fund formation, investor negotiations and some secondaries.", "London · England & Wales qualified", "Three-month notice; spring move feasible.", "Confirm how much secondaries experience the role requires."),
        ],
        "candidate_note": "Clara is exploring the market; no permission to introduce her to Calder Rowe has been given.",
        "factors": factors(
            [(1, "30 Oct: approved active search."), (0, "28 Oct: three matters / three expected; no uplift."), (0, "28 Oct: no planned team expansion confirmed."), (1, "30 Oct: one unresolved departure gap."), (1, "30 Oct: active search; spring start.")],
            [(.75, "Recent established contact, refreshed 30 Oct."), (1, "30 Oct: supplier process and terms agreed."), (.5, "Adjacent finance delivery, no direct funds placement."), (.5, "Accepted route in a competitive search.")],
            [(.5, "One recently engaged, plausible funds lawyer."), (1, "£135k base expectation within confirmed range."), (1, "London preference and qualification aligned."), (.75, "Three-month notice broadly fits spring start.")],
        ),
    },
    {
        "id": "westbridge", "firm": "Westbridge Counsel", "monogram": "WC",
        "location": "Dubai", "practice": "Finance", "level": "5–8 years PQE · to verify",
        "status": "verify", "status_label": "Needs verification",
        "summary": "A current vacancy; agency participation is open.",
        "window": "Vacancy rechecked 29 Oct", "start": "Not yet confirmed",
        "owner": "Amelia Reed", "updated": "2026-10-29", "restriction": None,
        "briefing": [
            "A current Dubai finance vacancy and a named growth plan provide a timely reason to ask about resourcing. The advert is current, but Leila has not confirmed budget, the exact level or whether it is an evergreen listing.",
            "Amelia has refreshed the hiring relationship and Leila is open to discussing agency support. Terms and the submission process remain unresolved, so this is a qualification conversation before any candidate introduction.",
            "Two engaged finance lawyers are interested in Dubai and broadly align on compensation. Their qualifications appear relevant; relocation logistics and the employer’s actual start date still need checking.",
        ],
        "contact": contact("Leila Fenwick", "Regional Hiring Manager", "Westbridge Counsel", "leila.fenwick@westbridge.example", "+44 20 7946 0386"),
        "evidence": [
            evidence("wc-advert", "2026-10-29", "Employer careers page · manual recheck", "Dubai finance associate listing remains open", "A revalidated official listing is closer to a requirement than deal news. Budget, exact experience and whether it is evergreen remain unconfirmed.", "vacancy"),
            evidence("wc-growth", "2026-10-20", "Firm office announcement", "Committed Dubai finance expansion", "The announcement identifies the Dubai finance practice. An eight-week baseline does not yet exist; growth is not counted as activity uplift."),
            evidence("wc-route", "2026-10-28", "Relationship call · Amelia Reed", "Hiring contact open to agency discussion", "Leila welcomed a follow-up on process, but has not agreed supplier terms. She confirmed no unresolved replacement gap."),
        ],
        "candidates": [
            candidate("Adam Cresswell", "6 years PQE", "Cross-border lending and regional acquisition finance.", "Dubai preferred · England & Wales qualified", "Three-month notice; relocation feasible in principle.", "Verify employer qualification requirements and relocation timing."),
            candidate("Nadia Linton", "7 years PQE", "Bank lending and sponsor financings in the Gulf.", "Dubai based · England & Wales qualified", "Two-month notice; start window not supplied by client.", "Confirm exact seniority and timetable against the client brief."),
        ],
        "candidate_note": "These are provisional fits to an advert, not a verified client brief. Neither candidate has agreed to an introduction.",
        "factors": factors(
            [(.75, "29 Oct: relevant official advert rechecked; approval unconfirmed."), (None, "Newly covered team; no comparable activity baseline."), (1, "20 Oct: specific Dubai finance expansion."), (0, "28 Oct: contact confirmed no unfilled departure gap."), (.5, "Current advert provides a reason to check; hire timing unknown.")],
            [(.75, "28 Oct: established relevant contact refreshed."), (.5, "Open to agency discussion; terms unresolved."), (.75, "One relevant regional finance placement."), (None, "Supplier competition not discussed.")],
            [(.75, "Two engaged, provisionally relevant lawyers."), (.75, "Published base range broadly aligns; package to verify."), (.5, "Qualifications appear relevant; relocation route needs checking."), (None, "Client timetable is unknown.")],
        ),
    },
    {
        "id": "fenmore", "firm": "Fenmore Legal", "monogram": "FL",
        "location": "London", "practice": "Restructuring", "level": "4–6 years PQE · provisional",
        "status": "verify", "status_label": "Needs verification",
        "summary": "Capacity pressure, with a smaller pipeline ahead.",
        "window": "Next client review in November", "start": "Not yet confirmed",
        "owner": "Oliver Nash", "updated": "2026-10-30", "restriction": None,
        "briefing": [
            "The team has reported pressure and one unresolved departure, but no hiring approval. A separate cancelled mandate reduces the forward pipeline, so the case for a permanent hire needs testing at the November review.",
            "Oliver’s current hiring-team relationship gives Buchanan a sensible way to ask whether the gap is temporary. The client is open to agency support, with terms still to be agreed.",
            "One engaged restructuring associate looks relevant and is London based. Pay and availability broadly align with an exploratory spring move; the actual remit and approved timing must come from the client.",
        ],
        "contact": contact("Marcus Elwood", "Head of Resourcing", "Fenmore Legal", "marcus.elwood@fenmore.example", "+44 20 7946 0521"),
        "evidence": [
            evidence("fl-pressure", "2026-10-30", "Hiring-team call · Oliver Nash", "Capacity pressure, approval not requested", "Marcus reported an associate gap but has not sought permanent headcount approval. The next capacity review is in November."),
            evidence("fl-pipeline", "2026-10-28", "Client pipeline review", "One independent mandate cancelled", "A planned restructuring mandate was cancelled. This is a separate forward-pipeline change, not the departure gap; it reduces the hiring-evidence score by ten points.", "contrary"),
            evidence("fl-matters", "2026-10-27", "Eight-week matter review", "Current activity is 50% above baseline", "Six current matters versus four expected under comparable coverage. The cancelled future mandate is excluded from both counts."),
        ],
        "candidates": [
            candidate("Thomas Alderney", "5 years PQE", "Creditor-side restructuring and distressed debt transactions.", "London · England & Wales qualified", "Three-month notice; exploratory spring preference.", "Verify approved role scope, compensation and start window."),
        ],
        "candidate_note": "Thomas is considering options; firm-specific interest and introduction permission are unconfirmed.",
        "contrary": {"points": 10, "note": "28 Oct: one independent future mandate cancelled; not counted in activity or gap factors."},
        "factors": factors(
            [(.25, "30 Oct: pressure reported, no hiring approval."), (.5, "Six / four expected − 1 = 0.5."), (0, "30 Oct: no growth programme confirmed."), (1, "30 Oct: client confirms unresolved associate departure."), (.5, "November capacity review; no confirmed hiring date.")],
            [(1, "30 Oct: active relevant client discussion."), (.5, "Open to support; terms unresolved."), (.5, "Adjacent distressed-finance delivery."), (.5, "Client accepts a competitive agency conversation.")],
            [(.5, "One recently engaged, plausible lawyer."), (.75, "Small gap against provisional £140k base guide."), (1, "London preference and qualification aligned."), (None, "Candidate explored timing, but no client schedule confirmed.")],
        ),
    },
    {
        "id": "ashford-lane", "firm": "Ashford Lane", "monogram": "AL",
        "location": "London", "practice": "Corporate / M&A", "level": "Associate level unconfirmed",
        "status": "research", "status_label": "Research lead",
        "summary": "A team launch; staffing plans are still unknown.",
        "window": "Expansion announced 26 Oct", "start": "Not yet confirmed",
        "owner": "Amelia Reed", "updated": "2026-10-28", "restriction": None,
        "briefing": [
            "A new sponsor team has been announced in London, but four associates are already arriving with its partners. The announcement establishes investment in the practice, not an unfilled role.",
            "Amelia knows the hiring manager from an adjacent search and can establish what staffing remains outstanding. Supplier eligibility and competing internal conversations must be checked before treating it as a search.",
            "No candidate shortlist has been assessed against an approved brief. Clarifying whether the incoming team already meets the need is more useful than proposing generic M&A profiles.",
        ],
        "contact": contact("Alice Penrose", "Legal Recruitment Manager", "Ashford Lane", "alice.penrose@ashfordlane.example", "+44 20 7946 0617"),
        "evidence": [
            evidence("al-launch", "2026-10-26", "Firm team-launch announcement", "London sponsor team opens with four associates", "The team and office are identified. Partners and arriving associates form one growth event. Further staffing needs are unknown."),
            evidence("al-relationship", "2026-10-28", "Account review · Amelia Reed", "Adjacent relationship; process needs checking", "Amelia refreshed Alice’s contact details. No requirement, supplier route or candidate timetable has been established."),
        ],
        "candidates": [], "candidate_note": "No role-specific shortlist assessed. Candidate readiness is unknown, not zero.",
        "factors": factors(
            [(None, "No confirmed requirement; absence of an advert is not a negative."), (None, "New team: no comparable 12-month baseline."), (1, "26 Oct: specific London sponsor-team launch."), (None, "No verified replacement information."), (.5, "Current launch is a reason to check, not a hiring timetable.")],
            [(.5, "Adjacent hiring relationship refreshed 28 Oct."), (None, "Agency route not checked."), (.5, "Adjacent delivery experience only."), (None, "Competitive position unknown.")],
            [(None, "No shortlist assessment completed."), (None, "No compensation range."), (None, "No verified role requirements."), (None, "No confirmed timetable.")],
        ),
    },
    {
        "id": "hartwell-stone", "firm": "Hartwell Stone", "monogram": "HS",
        "location": "Miami", "practice": "Corporate / M&A", "level": "Level unconfirmed",
        "status": "research", "status_label": "Research lead",
        "summary": "A large deal headline, without a hiring link.",
        "window": "Transaction announced 27 Oct", "start": "Not yet confirmed",
        "owner": "Oliver Nash", "updated": "2026-10-29", "restriction": None,
        "briefing": [
            "A $4.2bn acquisition names Hartwell Stone as adviser, but it does not identify the working office. Miami team involvement and any hiring requirement remain unverified; the price adds no priority points.",
            "Three articles describe the same transaction and count as one event. Much of the legal work may already be complete, so repeated coverage does not establish sustained capacity pressure.",
            "Buchanan has no verified relationship with this team and no role-specific candidate assessment. The useful first step is resolving the adviser team and existing account context before any approach.",
        ],
        "contact": contact("Julian Fairmont", "Director of Legal Recruitment", "Hartwell Stone", "julian.fairmont@hartwellstone.example", "+1 305 555 0168"),
        "evidence": [
            evidence("hs-acquisition", "2026-10-27", "Acquisition announcement + two reports", "$4.2bn acquisition; firm named as adviser", "Three sources, one underlying transaction. The working office is absent. Signing news may follow most of the work and gives no evidence of a Miami vacancy.", "context", 3),
            evidence("hs-review", "2026-10-29", "Account research note · Oliver Nash", "Hiring contact identified; team attribution unresolved", "Julian’s recruiting position is identified, but a current relationship, local mandate and permission to participate have not been verified."),
        ],
        "candidates": [], "candidate_note": "No verified team or brief to match against. A general candidate pool would not establish delivery readiness.",
        "identity_resolved": False,
        "factors": factors(
            [(None, "No evidence of a hiring requirement."), (None, "One event, unresolved office; no valid activity baseline."), (None, "No verified growth information."), (None, "No verified team-gap information."), (None, "Deal signing is not a Miami hiring timetable.")],
            [(None, "No verified current hiring-team relationship."), (None, "Commercial route unknown."), (None, "Local relevant delivery history unchecked."), (None, "Competitive position unknown.")],
            [(None, "No verified brief or shortlist assessment."), (None, "Compensation unknown."), (None, "Office and qualifications unresolved."), (None, "Hiring timetable unknown.")],
        ),
    },
    {
        "id": "kingsley-hart", "firm": "Kingsley Hart", "monogram": "KH",
        "location": "London", "practice": "Private credit", "level": "5–8 years PQE",
        "status": "paused", "status_label": "On hold · no contact",
        "summary": "Strong underlying fit; the client has asked us to wait.",
        "window": "Review on 16 November", "start": "Q1 2027 · under review",
        "owner": "Sophie Bennett", "updated": "2026-10-30",
        "restriction": {"title": "No contact before 16 November", "reason": "The hiring director has requested a pause during an internal team review. Sophie owns the account and must recheck permission on 16 November 2026; the restriction continues until the client lifts it."},
        "briefing": [
            "An approved private-credit role and a confirmed associate gap explain the strong underlying assessment. A separate growth commitment and above-baseline mandates add context, but do not override the current pause.",
            "Sophie has an established relationship and preferred supplier route, yet Beatrice requested no contact during the internal team review. That restriction takes precedence over the score until the client lifts it.",
            "Two engaged lawyers could align with a Q1 start. Candidate interest, availability and representation permission must be refreshed if the search resumes; the next review is 16 November.",
        ],
        "contact": contact("Beatrice Harlow", "Director of Talent", "Kingsley Hart", "beatrice.harlow@kingsleyhart.example", "+44 20 7946 0784"),
        "evidence": [
            evidence("kh-pause", "2026-10-30", "Client instruction · Beatrice Harlow", "No contact during internal review", "Review permission on 16 November; contact remains blocked until the client lifts the restriction. It is a hard condition, not a point deduction.", "restriction"),
            evidence("kh-role", "2026-10-26", "Hiring-team role brief", "Budgeted private-credit role and unresolved gap", "Budget, seniority, preferred supplier route and Q1 timing were confirmed before the later pause. These describe the underlying requirement, not current permission.", "requirement"),
            evidence("kh-context", "2026-10-24", "Client growth plan and matter review", "Separate growth commitment and six mandates", "Six unique mandates against four expected, alongside a separately funded practice expansion. These are distinct facts, not repeat articles about one event."),
        ],
        "candidates": [
            candidate("Isabel Thorpe", "6 years PQE", "Sponsor-side private credit and bespoke debt structures.", "London · England & Wales qualified", "Three-month notice at last discussion.", "Refresh availability and firm interest after the client lifts its pause."),
            candidate("James Elliston", "7 years PQE", "Direct-lending and special-situations finance.", "London · England & Wales qualified", "Q1 move was feasible at last review.", "Recheck timing, current process and representation permission."),
        ],
        "candidate_note": "No introductions are permitted during the pause. Neither candidate has authorised submission to Kingsley Hart.",
        "factors": factors(
            [(1, "26 Oct: approved role; later pause is handled as a gate."), (.5, "Six / four expected − 1 = 0.5."), (1, "24 Oct: separately committed practice expansion."), (1, "26 Oct: client confirms unfilled associate gap."), (1, "26 Oct: Q1 search timetable, subject to subsequent review.")],
            [(1, "Active relevant relationship; now subject to pause."), (1, "Established terms; current contact restriction takes precedence."), (1, "Repeated relevant London private-credit delivery."), (1, "Preferred supplier route confirmed before the pause.")],
            [(.75, "Two engaged plausible candidates at 30 Oct review."), (1, "Confirmed £170k base band aligns with expectations."), (1, "Both London based and appropriately qualified."), (.75, "Q1 broadly aligned; refresh after pause.")],
        ),
    },
]
