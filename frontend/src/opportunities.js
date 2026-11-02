export const DEFAULT_FILTERS = { query: '', location: '', practice: '' };

export function filterOptions(opportunities, key) {
  return [...new Set(opportunities.map((opportunity) => opportunity[key]))].sort();
}

export function filterOpportunities(opportunities, filters) {
  const terms = filters.query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return opportunities.filter((o) => {
    const searchable = [o.firm, o.location, o.practice, o.level, o.summary, o.owner, o.contact.name].join(' ').toLocaleLowerCase();
    return (!filters.location || o.location === filters.location)
      && (!filters.practice || o.practice === filters.practice)
      && terms.every((term) => searchable.includes(term));
  });
}

export function number(value) {
  return new Intl.NumberFormat('en-GB', { maximumFractionDigits: 2 }).format(value);
}

export function range(lower, upper) {
  return lower === upper ? number(lower) : `${number(lower)}–${number(upper)}`;
}

export function scoreLabel(assessment) {
  return assessment.meaningful ? range(assessment.lower, assessment.upper) : 'Not scored';
}

export function dateLabel(date) {
  return new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${date}T12:00:00Z`));
}
