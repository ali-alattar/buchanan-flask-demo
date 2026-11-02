import test from 'node:test';
import assert from 'node:assert/strict';
import { DEFAULT_FILTERS, filterOpportunities, filterOptions, scoreLabel, range } from './opportunities.js';

const records = [
  { id: 'a', firm: 'Alder & Vale', location: 'London', practice: 'Private credit', status: 'confirmed', level: '4–7 PQE', summary: 'Approved search', owner: 'Sophie Bennett', contact: { name: 'Helen Mercer' } },
  { id: 'b', firm: 'Marlowe Pierce', location: 'Miami', practice: 'Corporate / M&A', status: 'confirmed', level: '2020 class', summary: 'Growing sponsor practice', owner: 'Oliver Nash', contact: { name: 'Rafael Ellery' } },
  { id: 'c', firm: 'Calder Rowe', location: 'London', practice: 'Funds', status: 'confirmed', level: '3–6 PQE', summary: 'Approved replacement', owner: 'Sophie Bennett', contact: { name: 'Priya Hollis' } },
];

test('search finds firms, contacts, locations and practice across case and whitespace', () => {
  for (const [query, ids] of [['  HELEN  ', ['a']], ['London credit', ['a']], ['Marlowe', ['b']], ['Miami', ['b']]]) {
    assert.deepEqual(filterOpportunities(records, { ...DEFAULT_FILTERS, query }).map((o) => o.id), ids);
  }
});

test('location and practice filters combine without changing rank order', () => {
  const filtered = filterOpportunities(records, { query: '', location: 'London', practice: 'Funds' });
  assert.deepEqual(filtered.map((o) => o.id), ['c']);
  assert.deepEqual(filterOpportunities(records, { ...DEFAULT_FILTERS, location: 'London' }).map((o) => o.id), ['a', 'c']);
});

test('filter options come only from the returned opportunities, with no status control', () => {
  assert.deepEqual(filterOptions(records, 'location'), ['London', 'Miami']);
  assert.deepEqual(filterOptions(records, 'practice'), ['Corporate / M&A', 'Funds', 'Private credit']);
  assert.deepEqual(Object.keys(DEFAULT_FILTERS), ['query', 'location', 'practice']);
});

test('empty results and resetting every filter', () => {
  assert.equal(filterOpportunities(records, { ...DEFAULT_FILTERS, query: 'no such firm' }).length, 0);
  assert.equal(filterOpportunities(records, { ...DEFAULT_FILTERS, location: 'Dubai' }).length, 0);
  assert.deepEqual(filterOpportunities(records, { ...DEFAULT_FILTERS }), records);
});

test('score presentation keeps exact displayed arithmetic and distinguishes unknown', () => {
  assert.equal(scoreLabel({ meaningful: true, lower: 81.84, upper: 81.84 }), '81.84');
  assert.equal(scoreLabel({ meaningful: true, lower: 57.38, upper: 72.38 }), '57.38–72.38');
  assert.equal(scoreLabel({ meaningful: false, lower: 0, upper: 100 }), 'Not scored');
  assert.equal(range(70, 70), '70');
});
