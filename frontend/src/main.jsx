import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { DEFAULT_FILTERS, filterOpportunities, filterOptions, scoreLabel, dateLabel } from './opportunities';
import './styles.css';

function Icon({ name, size = 18 }) {
  const paths = {
    search: <><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4.5 4.5" /></>,
    arrow: <><path d="M5 19 19 5M5 5h14v14" /></>,
    mail: <><rect x="3" y="5" width="18" height="14" rx="2" /><path d="m3 6 9 7 9-7" /></>,
    phone: <path d="M7 3H4a1 1 0 0 0-1 1c0 9.4 7.6 17 17 17a1 1 0 0 0 1-1v-3l-5-2-2 2a14 14 0 0 1-7-7l2-2-2-5Z" />,
    chevron: <path d="m6 9 6 6 6-6" />,
    back: <path d="m12 5-7 7 7 7M5 12h15" />,
    reset: <><path d="M4 10a8 8 0 1 1 1 8M4 4v6h6" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

function Status({ opportunity }) {
  return <span className={`status status-${opportunity.status}`}><span className="status-dot" />{opportunity.status_label}</span>;
}

function Expandable({ title, subtitle, children, className = '' }) {
  return <details className={`expandable ${className}`}>
    <summary><span><strong>{title}</strong><span className="summary-subtitle">{subtitle}</span></span><Icon name="chevron" /></summary>
    <div className="expanded-content">{children}</div>
  </details>;
}

function Contact({ contact }) {
  const email = <><Icon name="mail" /><span>{contact.email}</span></>;
  const phone = <><Icon name="phone" /><span>{contact.phone}</span></>;
  return <section className="contact-section" aria-labelledby="contact-heading">
    <div className="section-label" id="contact-heading">What’s next</div>
    <div className="contact-content">
      <div><h3>{contact.name}</h3><p>{contact.title}</p><p className="muted">{contact.firm}</p></div>
      <address className="contact-links">
        <a href={`mailto:${contact.email}`}>{email}</a>
        <a href={`tel:${contact.phone.replaceAll(' ', '')}`}>{phone}</a>
      </address>
    </div>
  </section>;
}

function OpportunityDetail({ opportunity, onBack, panelRef }) {
  return <article className="detail-panel" aria-label={`${opportunity.firm} opportunity details`} ref={panelRef} tabIndex={-1}>
    <button className="mobile-back text-button" onClick={onBack}><Icon name="back" />Back to opportunities</button>
    <div className="detail-eyebrow"><span>TEAM BRIEF / {String(opportunity.rank).padStart(2, '0')}</span><span>Reviewed {dateLabel(opportunity.updated)}</span></div>
    <div className="detail-title-row">
      <div><Status opportunity={opportunity} /><h2>{opportunity.firm}</h2><p className="detail-practice">{opportunity.practice}<span> / </span>{opportunity.location}</p></div>
      <div className="priority-score"><span>Priority points</span><strong>{scoreLabel(opportunity.assessment)}</strong><span>out of 100</span></div>
    </div>
    <dl className="team-facts">
      <div><dt>Experience</dt><dd>{opportunity.level}</dd></div>
      <div><dt>Hiring window</dt><dd>{opportunity.window}</dd></div>
      <div><dt>Buchanan owner</dt><dd>{opportunity.owner}</dd></div>
    </dl>
    <section className="briefing" aria-labelledby="briefing-heading"><div className="section-label">The opportunity</div><h3 id="briefing-heading">Why this is worth a conversation</h3><ul>{opportunity.briefing.map((bullet, index) => <li key={bullet}><span className="bullet-number">0{index + 1}</span><p>{bullet}</p></li>)}</ul></section>
    <Contact contact={opportunity.contact} />
    <div className="detail-secondary">
      <Expandable title="Supporting evidence" subtitle={`${opportunity.evidence.length} records · sources, dates & caveats`}>
        <p className="small muted">Desired employment start: {opportunity.start}. A transaction announcement is evidence of legal work, not a confirmed hiring requirement.</p>
        <ol className="evidence-list">{opportunity.evidence.map((record) => <li key={record.event_id}>
          <div className="evidence-meta"><time dateTime={record.date}>{dateLabel(record.date)}</time><span className={`evidence-kind kind-${record.kind}`}>{({ requirement: 'Client-confirmed', vacancy: 'Official vacancy', contrary: 'Contrary evidence', restriction: 'Contact restriction', context: 'Supporting context' })[record.kind]}</span></div>
          <h4>{record.title}</h4><p className="source">{record.source}</p><p>{record.relevance}</p>
          {record.source_count > 1 && <p className="small source-count">{record.source_count} sources grouped as one event · no extra points for repeated coverage</p>}
        </li>)}</ol>
      </Expandable>
      <Expandable title="Candidate fit" subtitle={opportunity.candidates.length ? `${opportunity.candidates.length} potential ${opportunity.candidates.length === 1 ? 'match' : 'matches'} · permission to introduce unconfirmed` : 'Not yet assessed · verified brief needed'}>
        <p className="candidate-permission">{opportunity.candidate_note}</p>
        <div className="candidates">{opportunity.candidates.map((candidate) => <section className="candidate" key={candidate.name}>
          <div className="candidate-heading"><h4>{candidate.name}</h4><span>{candidate.level}</span></div>
          <p>{candidate.experience}</p><p className="small muted">{candidate.location}</p><p className="small">{candidate.availability}</p>
          <p className="verify-note"><strong>To verify</strong> {candidate.verify}</p><p className="small muted">Last discussed {dateLabel(candidate.reviewed)}</p>
        </section>)}</div>
      </Expandable>
    </div>
  </article>;
}

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [retry, setRetry] = useState(0);
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [selectedId, setSelectedId] = useState(null);
  const [mobileDetail, setMobileDetail] = useState(false);
  const panelRef = useRef(null);

  useEffect(() => {
    const controller = new AbortController();
    setError('');
    fetch('/api/opportunities', { signal: controller.signal })
      .then((response) => { if (!response.ok) throw new Error(`Request failed (${response.status})`); return response.json(); })
      .then(setData)
      .catch((failure) => { if (failure.name !== 'AbortError') setError('The opportunity desk could not be loaded. Check that Flask is running, then try again.'); });
    return () => controller.abort();
  }, [retry]);

  const opportunities = data?.opportunities ?? [];
  const visible = useMemo(() => filterOpportunities(opportunities, filters), [data, filters]);
  const selected = visible.find((o) => o.id === selectedId) ?? visible[0];
  const filtered = Object.values(filters).some(Boolean);
  useEffect(() => {
    if (selected && selected.id !== selectedId) setSelectedId(selected.id);
  }, [selected?.id, selectedId]);

  function select(id) {
    setSelectedId(id);
    setMobileDetail(true);
    requestAnimationFrame(() => {
      const panel = panelRef.current;
      const narrowScreen = window.matchMedia('(max-width: 900px)').matches;
      if (panel && (narrowScreen || panel.getBoundingClientRect().top < 0)) {
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      if (narrowScreen) panel?.focus({ preventScroll: true });
    });
  }

  function reset() {
    setFilters({ ...DEFAULT_FILTERS });
    setMobileDetail(false);
  }

  const selectFilter = (key, value) => { setFilters((current) => ({ ...current, [key]: value })); setMobileDetail(false); };
  return <>
    <a className="skip-link" href="#opportunity-list">Skip to opportunities</a>
    <header className="site-header"><div className="header-inner"><span className="brand">Buchanan</span><div className="desk-label">OPPORTUNITY DESK</div><span className="header-markets">London <span>·</span> Miami <span>·</span> Dubai</span></div></header>
    <main>
      <section className="page-intro"><div><div className="eyebrow">Relationships meet opportunity</div><h1>Your next conversation.</h1><p>A considered view of where Buchanan can make a difference.</p></div><div className="snapshot"><span>DESK OVERVIEW</span><time dateTime={data?.as_of}>{data ? dateLabel(data.as_of) : '2 Nov 2026'}</time></div></section>
      {error ? <section className="load-state" role="alert"><h2>Let’s get the desk back.</h2><p>{error}</p><button className="solid-button" onClick={() => setRetry((value) => value + 1)}>Try again</button></section> : !data ? <div className="load-state" role="status">Preparing the opportunity desk…</div> : <>
        <form className="filters" onSubmit={(event) => event.preventDefault()} aria-label="Filter opportunities">
          <label className="search-field"><Icon name="search" /><span className="sr-only">Search opportunities</span><input type="search" placeholder="Search firm, practice or contact…" value={filters.query} onChange={(event) => selectFilter('query', event.target.value)} /></label>
          {[['location', 'Location', 'All locations'], ['practice', 'Legal practice', 'All practices']].map(([key, label, placeholder]) => <label className="select-field" key={key}><span className="sr-only">{label}</span><select value={filters[key]} onChange={(event) => selectFilter(key, event.target.value)}><option value="">{placeholder}</option>{filterOptions(opportunities, key).map((value) => <option key={value}>{value}</option>)}</select><Icon name="chevron" /></label>)}
          <button type="button" className="reset-button" disabled={!filtered} onClick={reset}><Icon name="reset" size={16} />Reset</button>
        </form>
        <div className={`workspace ${mobileDetail ? 'show-detail' : ''}`}>
          <section className="shortlist" id="opportunity-list" tabIndex={-1} aria-label="Ranked opportunities"><div className="shortlist-heading"><h2>The shortlist <span aria-live="polite">{visible.length}</span></h2><span>Priority ↓</span></div>
            {visible.length ? <ol className="opportunity-list">{visible.map((o) => <li key={o.id}><button className={`opportunity-row ${selected?.id === o.id ? 'selected' : ''}`} aria-pressed={selected?.id === o.id} aria-controls="selected-opportunity" onClick={() => select(o.id)}>
              <div className="row-top"><span className="rank">{String(o.rank).padStart(2, '0')}</span><Status opportunity={o} /><span className="row-score">{scoreLabel(o.assessment)}</span></div>
              <div className="row-firm"><h3>{o.firm}</h3><Icon name="arrow" size={17} /></div><p className="row-practice">{o.practice}<span>·</span>{o.location}</p><p className="row-summary">{o.summary}</p>
            </button></li>)}</ol> : <div className="empty-state"><Icon name="search" size={28} /><h3>No teams match this view.</h3><p>Try another firm or contact, broaden a filter, or start again.</p><button className="solid-button" onClick={reset}>Reset all filters</button></div>}
            <div className="shortlist-foot">{visible.length} of {opportunities.length} opportunities</div>
          </section>
          <div id="selected-opportunity" className="detail-container">{selected ? <OpportunityDetail key={selected.id} opportunity={selected} panelRef={panelRef} onBack={() => { setMobileDetail(false); requestAnimationFrame(() => document.querySelector('#opportunity-list')?.focus()); }} /> : <div className="detail-empty"><h2>A fresh perspective starts here.</h2><p>Adjust your search to find the next team worth understanding.</p></div>}</div>
        </div>
      </>}
      <footer className="site-footer"><span>Buchanan <span>/</span> Opportunity desk</span></footer>
    </main>
  </>;
}

createRoot(document.getElementById('root')).render(<App />);
