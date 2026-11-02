# Buchanan opportunity desk

[View the running dashboard on Azure Container Apps](https://buchanan-flask-demo.whitecoast-9e12cb6c.uksouth.azurecontainerapps.io/)

A small recruitment opportunity demonstration for James: three fully assessed, active team-level briefs, a ranked shortlist, search, location/practice filters, relevant candidates, supporting evidence and a named hiring contact. Select a team to see its briefing; expand the evidence and candidate sections for detail. On narrow screens the selected brief replaces the shortlist, with a back button.

The interface follows the white space, black sans-serif typography and teal palette of [Buchanan's website](https://wearebuchanan.com/), using system fonts and plain text for the Buchanan name. No logos, brand favicon, invented brand slogan, totals strip or scoring breakdown appear in the interface.

**All firms, people, candidates, transactions, contact details and internal records in this application are fictional.** They are hand-authored in `opportunity_data.py`, not statements about real firms or Buchanan's actual relationships. Emails use `.example`; phone numbers use reserved UK London `020 7946 0xxx` or US `555-01xx` ranges. The Dubai contact has a reserved UK contact number. The fixed assessment snapshot is **2 November 2026**; dates do not refresh automatically.

There is no database, authentication, Bullhorn connection, news feed, external AI service, scraping or automatic messaging. A possible candidate fit is not permission to introduce or represent that person. Email/phone links open the user's own application; they do not send anything. The wider eight-record dataset is retained internally, but partially assessed, on-hold and unscored records are excluded from the dashboard API and its filter options. Only Alder & Vale, Marlowe Pierce and Calder Rowe are currently displayed. All three are confirmed requirements, so the redundant status filter has been removed.

## Local startup in VS Code

Use the existing `.venv`. No Python dependencies were added or changed. The installed environment has Python 3.14.2, Flask 3.1.3 and Gunicorn 26.2.0.

### Preview the production frontend through Flask (one server)

In a VS Code terminal, from the project root:

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
npm --prefix frontend ci
npm --prefix frontend run build
.venv/bin/gunicorn --bind 127.0.0.1:8000 --access-logfile - app:app
```

Open <http://127.0.0.1:8000>. Stop with Ctrl+C. Node is needed only for building; Flask/Gunicorn serves the resulting `frontend/dist` assets. After changing frontend source, rebuild before refreshing this preview. Without a build, `/` returns a helpful 503 message; `/health`, `/roles` and the opportunity API still work.

### Develop with Vite's fast refresh (two terminals)

Terminal 1, working directory `/Users/alialattar/Developer/buchanan-flask-demo`:

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
.venv/bin/python -m flask --app app run --debug --host 127.0.0.1 --port 8000
```

Terminal 2, working directory `/Users/alialattar/Developer/buchanan-flask-demo`:

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
npm --prefix frontend ci
npm --prefix frontend run dev
```

Open <http://127.0.0.1:5173>. Vite proxies `/api`, `/health` and `/roles` to Flask on port 8000. Stop both terminals with Ctrl+C. Use either the Gunicorn preview or Flask development server on port 8000, not both together. All local servers bind to loopback.

### Dependencies

Node **22.13.1** and npm **10.9.2** were already installed. The selected Vite/plugin versions support this Node version; no global installation or system upgrade was made. Exact versions are retained in `frontend/package.json` and `frontend/package-lock.json`:

| Dependency | Version | Purpose |
| --- | --- | --- |
| react | 19.3.1 | Interface |
| react-dom | 19.3.1 | Browser rendering |
| vite | 7.3.7 | Local dev server and static production build |
| @vitejs/plugin-react | 5.2.0 | React integration for Vite |

Only React and React DOM are runtime frontend dependencies. Transitive build dependencies are in the lockfile. Browser requests use native `fetch`; typography uses local system fonts. No additional Python packages or testing framework are needed.

## How priority works

`scoring.py` contains **all weights**, the internal 70% minimum per-area scoring threshold, and the stricter dashboard eligibility rule. The dashboard only receives meaningful, unrestricted scores with **100% factor coverage in every area** and no paused status. `opportunity_data.py` contains dated evidence and explicit factor judgements. These modest policy choices adapt section 5 of the supplied [research assessment](/Users/alialattar/Documents/Codex/2026-10-31/i-m-evaluating-an-idea-for/outputs/buchanan-opportunity-software-assessment.md); they are not calibrated forecasts.

**Priority = 50% hiring evidence + 30% relationship/access + 20% candidate readiness.** Each area is assessed on 0–100 points. Inputs range from 0 to 1; `None` means unknown. The interface retains the total priority points and rank; the component scores, coverage indicators and calculation disclosure were removed at the user's request. Factor judgements remain in the source and API for internal verification.

| Area | Factors and maximum points |
| --- | --- |
| Hiring evidence | Current requirement 45; comparable team activity uplift 20; specific committed growth 15; unresolved replacement gap 10; usable timing 10 |
| Relationship/access | Relevant current relationship 40; permitted commercial route 30; relevant delivery history 20; competitive position 10 |
| Candidate readiness | Engaged relevant supply 45; pay alignment 25; location/qualification fit 20; availability 10 |

- A confirmed approved requirement scores 1 on requirement evidence; a rechecked employer vacancy 0.75; client-reported pressure without approval 0.25. A zero needs confirmed absence in that window. Not finding an advert is unknown.
- Activity uplift is `clamp(unique matters / comparable expected matters - 1, 0, 1)`. A valid baseline needs comparable 12-month coverage; a new team without one remains unknown. Deal value is excluded. Articles are grouped by underlying event ID before authoring factor inputs. The app is not a general ingestion or deduplication engine.
- Growth is 1 for a specific committed practice expansion, 0.5 for relevant growth intent with supporting staffing unconfirmed. An office launch and its partner arrivals count once. Replacement is 1 for a client-confirmed unfilled gap, 0.5 for a verified departure with need unconfirmed. Growth and gap cannot reuse the same fact.
- Timing is 1 for an active/near-term confirmed search, 0.5 for a current reason to check without a confirmed hire date. Search timing and desired employment start remain separate.
- Relationship is 1 for an active relevant discussion, 0.75 for a recent established contact, 0.5 for a refreshed older/adjacent relationship. Commercial route is 1 for agreed terms/process, 0.5 for openness with terms unresolved. Relevant history is 1 for repeated delivery, 0.75 for one recent relevant success, 0.5 for adjacent work. Competitive position is 1 for a preferred/exclusive route, 0.5 for an accepted competitive route.
- Engaged candidate supply is 1 for three or more plausible people, 0.75 for two, 0.5 for one, 0.25 for a sourcing map only, 0 for a completed unsuccessful search. Pay, qualification/location and timing use supported alignment judgements described alongside the inputs; missing client requirements remain unknown.
- A separate, confirmed pipeline cancellation deducts 10 hiring points; broader confirmed contraction may deduct up to 20. The same fact cannot also reduce another factor. No evidence is treated as absence simply because it is missing.
- Unknown factors span 0 to their full factor weight; they are not silently set to zero, imputed or normalised away. Bounds are policy uncertainty ranges, not statistical confidence intervals. The internal assessment can produce a range at 70% coverage per area; incomplete or unscored records are excluded entirely from the dashboard and search/filter choices.
- Each factor contribution, area contribution and final total is rounded to two decimal places, half up. The total sums the rounded weighted area contributions exactly. For Alder & Vale: `85 × 50% + 90 × 30% + 80 × 20% = 85.5`. Marlowe Pierce illustrates rounding. Westbridge's range remains an internal example and is excluded from the dashboard.
- Current restrictions override scores. Kingsley Hart has 92.25 underlying points but is excluded because the client requested **no contact before 16 November, and until the client lifts its pause**. A paused record is excluded even without a separate restriction field. No score authorises contact or a candidate submission. The user must recheck the fixed snapshot before any real-world use.

This is deliberately smaller than the research's proposed production workflow: no automatic freshness decay, confidence model, individual candidate match score, fee prediction, feedback storage or live permission checks.

## Routes and source layout

| Route | Behaviour |
| --- | --- |
| `/` | Built React dashboard served by Flask |
| `/assets/<filename>` | Built hashed frontend assets |
| `/api/opportunities` | Three fully assessed, active briefs with deterministic assessments and ranks |
| `/health` | Existing `{"status":"ok"}` response |
| `/roles` | Original two roles and count, unchanged |

The production architecture is one Gunicorn/Flask application and static files, with **no Node production server**. `frontend/dist` and `node_modules` are generated/ignored; the lockfile is retained. The Dockerfile has a Node build stage and copies only its built frontend into the Python runtime. It preserves `app:app`, port 8000 and non-root `appuser` execution.

## Focused local checks

Working directory `/Users/alialattar/Developer/buchanan-flask-demo` for every command:

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
npm --prefix frontend run build
npm --prefix frontend test
.venv/bin/python -m unittest discover -s tests -v
git diff --check
```

The five Node checks cover search, combined filters, eligible filter options, reset/empty results and exact score presentation. The twelve Python checks cover score arithmetic, coverage and unknowns, rounding reconciliation, deterministic ordering, restrictions, dashboard eligibility in every scoring area, contrary evidence, duplicate coverage/deal-value invariance, contacts/candidates, API records, existing routes, built asset serving and the missing-build response.

Browser inspection should exercise the three selections; location/practice filters and reset; a no-match search; and candidate/evidence expansion for different teams. Confirm that excluded firms and their unique filter choices cannot appear, and that the totals, logos/slogan and scoring sections are absent. At a narrow width, select a team and use the back button. The dashboard intentionally stores no edits or state between reloads.

### Verification completed on 2 November 2026

- Production Vite build passed. Five Node tests and twelve Python tests passed; Python was also run with resource warnings treated as errors. `git diff --check` passed.
- npm reported no vulnerabilities during installation. Installed package engines accept the existing Node 22.13.1.
- Browser checked the three remaining selections, their named hiring contacts/job titles, evidence and candidates. Evidence/candidate disclosures reset when switching teams.
- Browser checked location/practice filters together, case-insensitive contact search, filter reset and empty results without stale detail content. A search for the excluded Kingsley record returns no matches.
- Browser confirmed only London/Miami and Corporate / M&A/Funds/Private credit are offered. There is no status filter, overview totals, logo, slogan, assessment strip or calculation disclosure.
- Laptop layout checked at 1366×900. Narrow layouts checked at 390×844 and 320×800, including selection/back navigation, focus return and no horizontal clipping. The temporary viewport override was reset.
- Built Flask/Gunicorn serving worked in the browser. Earlier verification also confirmed Vite's development proxy and `/health` and `/roles` through both ports 8000 and 5173; their configuration is unchanged.
- [Saved dashboard preview](docs/opportunity-desk.jpg). Temporary verification servers were stopped after checking.

No implementation work is pending. Container builds/runs, Azure configuration, registry access, image architecture compatibility and deployment were not verified by Codex during local implementation. The user subsequently confirmed the running ACA deployment linked above. Only the available browser engine was inspected locally; this was not an exhaustive cross-browser/accessibility audit. Dataset dates are fixed and no state persists.

### Files added or changed

| File | Change |
| --- | --- |
| `app.py` | Added dashboard, asset and opportunity API routes; retained health and roles. |
| `opportunity_data.py` | Added the eight fictional briefs, dated evidence, contacts, candidates and explicit scoring inputs. |
| `scoring.py` | Added the central policy, coverage/ranges, rounding, ordering and the fully assessed active dashboard eligibility rule. |
| `frontend/package.json` | Added the four pinned dependencies and dev/build/test commands. |
| `frontend/package-lock.json` | Added reproducible dependency resolution. |
| `frontend/index.html` | Added the page shell and metadata; removed the earlier brand favicon. |
| `frontend/vite.config.js` | Added React build support and the local Flask proxy. |
| `frontend/src/main.jsx` | Added the simplified dashboard, two filters, evidence/candidate disclosures, contacts, and loading/error/empty states. Removed totals, logos/slogan and scoring sections. |
| `frontend/src/styles.css` | Added website-inspired sans-serif, white/black/teal styling, keyboard focus and responsive layouts. |
| `frontend/src/opportunities.js` | Added search/filter and score/date presentation helpers. |
| `frontend/src/opportunities.test.js` | Added five focused native Node checks. |
| `tests/test_app.py` | Added twelve focused standard-library scoring/data/route checks. |
| `Dockerfile` | Added the frontend build stage; retained Python/Gunicorn, port 8000 and non-root runtime. Not executed. |
| `.dockerignore` | Excluded local frontend outputs/dependencies, tests and preview documentation. |
| `.gitignore` | Excluded Node dependencies; existing `dist/` rule already excludes builds. |
| `docs/opportunity-desk.jpg` | Added a browser screenshot of the verified production frontend. |
| `README.md` | Added usage, startup, scoring rationale, verification/file report and manual deployment instructions. |

Generated `frontend/dist/index.html` and its hashed JS/CSS assets are present locally but ignored by Git. `frontend/node_modules` is installed locally and ignored. `requirements.txt` is unchanged. No commit, push or pull request was made.

## Manual Docker and Azure steps — for you to run later

**Codex did not run Docker or Azure commands or perform a deployment.** The user has since provided the running ACA link above. These commands are manual instructions for future builds and updates. Codex edited the Dockerfile but did not build or run it. There is no deployment script or automatic workflow.

Run the following yourself in a **VS Code terminal using zsh**, in order. The working directory for **every block below** is `/Users/alialattar/Developer/buchanan-flask-demo`. Stop the local port-8000 preview first. The existing README documented the app name `buchanan-flask-demo` and this earlier endpoint: <https://buchanan-flask-demo.whitecoast-9e12cb6c.uksouth.azurecontainerapps.io/roles>. Its current availability was not checked.

### 1. Build and check locally

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
docker build -t buchanan-flask-demo:opportunity-v1 .
docker run --rm -p 127.0.0.1:8000:8000 buchanan-flask-demo:opportunity-v1
```

While the container runs, open <http://127.0.0.1:8000>, `/health` and `/roles` in your browser. Verify the interface and assets. Stop it with Ctrl+C before continuing. This validates the future multi-stage build and non-root runtime, which local Flask checks alone cannot confirm.

### 2. Sign in and confirm existing resources

Replace all three placeholders with **your existing values** before executing. The repository does not document a reliable subscription ID, resource group or ACR name; none have been invented. Confirm that `buchanan-flask-demo` is still the correct app in that resource group.

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
az login
az account show --output table
export BUCHANAN_SUBSCRIPTION_ID='<confirm-existing-subscription-id>'
export BUCHANAN_RESOURCE_GROUP='<confirm-existing-container-app-resource-group>'
export BUCHANAN_REGISTRY='<confirm-existing-acr-name>'
az account set --subscription "$BUCHANAN_SUBSCRIPTION_ID"
az acr show --name "$BUCHANAN_REGISTRY" --query '{name:name,resourceGroup:resourceGroup,loginServer:loginServer}' --output table
az containerapp show --name buchanan-flask-demo --resource-group "$BUCHANAN_RESOURCE_GROUP" --query '{name:name,ingress:properties.configuration.ingress,registries:properties.configuration.registries,image:properties.template.containers[0].image,revisionMode:properties.configuration.activeRevisionsMode}' --output json
```

Check subscription, registry access, ingress target port **8000**, current revision mode/traffic and existing registry authentication. If those differ from expectations, resolve them before updating. This guide reuses the existing registry/authentication and app; it does not create resources, grant roles or enable anonymous access. Keep the old image/revision details if you need to roll back. With multiple active revisions, traffic may require a separate deliberate decision after the image update.

### 3. Push the checked image to the existing registry

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
export BUCHANAN_IMAGE_TAG='opportunity-v1'
BUCHANAN_LOGIN_SERVER="$(az acr show --name "$BUCHANAN_REGISTRY" --query loginServer --output tsv)"
az acr login --name "$BUCHANAN_REGISTRY"
docker tag buchanan-flask-demo:opportunity-v1 "$BUCHANAN_LOGIN_SERVER/buchanan-flask-demo:$BUCHANAN_IMAGE_TAG"
docker push "$BUCHANAN_LOGIN_SERVER/buchanan-flask-demo:$BUCHANAN_IMAGE_TAG"
```

Use a fresh image tag for subsequent builds, updating both the local build/tag commands and `BUCHANAN_IMAGE_TAG`. A unique tag makes revisions and rollback easier to identify.

### 4. Update only the existing app image, then verify

```sh
cd /Users/alialattar/Developer/buchanan-flask-demo
az containerapp update --name buchanan-flask-demo --resource-group "$BUCHANAN_RESOURCE_GROUP" --image "$BUCHANAN_LOGIN_SERVER/buchanan-flask-demo:$BUCHANAN_IMAGE_TAG"
az containerapp show --name buchanan-flask-demo --resource-group "$BUCHANAN_RESOURCE_GROUP" --query '{fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName,latestReadyRevision:properties.latestReadyRevisionName,traffic:properties.configuration.ingress.traffic,image:properties.template.containers[0].image}' --output json
```

Confirm the intended revision is ready and receives the intended traffic. Use the **returned** hostname to check `/`, `/health`, `/roles` and a frontend asset in your browser. If you run into image-pull/authentication or revision/traffic problems, investigate the existing configuration rather than blindly changing credentials, creating new resources or switching traffic. These steps, registry permissions, architecture compatibility and the deployed app remain unverified until you execute them.
