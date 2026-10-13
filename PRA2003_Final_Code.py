# PRA2003 - Bacterial abundance and momentum analysis
import csv
import math
import statistics as stats
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PAIRS = [
    ('E. coli', 211, -211), ('B. subtilis', 321, -321),
    ('P. aeruginosa', 2212, -2212), ('S. pneumoniae', 3122, -3122),
    ('M. tuberculosis', 3312, -3312), ('S. enterica', 3334, -3334)
]
NAMES = {i: f'{name} WT' for name, i, j in PAIRS}
NAMES.update({j: f'{name} variant' for name, i, j in PAIRS})


def mean_sd(values):
    return stats.mean(values), stats.stdev(values) if len(values) > 1 else 0.0


def save_csv(folder, filename, headings, rows):
    with (folder / filename).open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headings)
        writer.writerows(rows)


# Read the large input files event by event to avoid loading them into memory.
def analyse(path, widths):
    counts = {i: 0 for i in NAMES}
    bins = {i: defaultdict(int) for i in NAMES}
    events = valid = invalid = 0
    with path.open(encoding='utf-8') as file:
        while header := file.readline():
            if not header.strip():
                continue
            parts = header.split()
            if len(parts) != 2:
                raise ValueError(f'{path.name}: invalid event header: {header.strip()}')
            try:
                event_id, n_particles = map(int, parts)
            except ValueError as exc:
                raise ValueError(f'{path.name}: invalid event header') from exc
            if n_particles < 0:
                raise ValueError(f'{path.name}: negative particle count')
            events += 1
            has_target = False
            for _ in range(n_particles):
                line = file.readline()
                if not line:
                    raise ValueError(f'{path.name}: incomplete event {event_id}')
                parts = line.split()
                if len(parts) != 4:
                    invalid += 1
                    continue
                try:
                    px, py, pz = map(float, parts[:3])
                    bac_id = int(parts[3])
                    if not all(map(math.isfinite, (px, py, pz))):
                        raise ValueError('non-finite momentum')
                except ValueError:
                    invalid += 1
                    continue
                if bac_id in counts:
                    has_target = True
                    counts[bac_id] += 1
                    # Use the magnitude so momentum can be compared in one dimension.
                    p = math.sqrt(px**2 + py**2 + pz**2)
                    # Keep the same momentum range and bin widths across subsamples.
                    if p < 60:
                        bins[bac_id][int(p / widths[abs(bac_id)])] += 1
            # Empty events and events without target IDs are excluded from the denominator.
            valid += has_target
    if not valid:
        raise ValueError(f'{path.name}: no valid events')
    return {'file': path.name, 'events': events, 'valid': valid,
            'invalid': invalid, 'counts': counts, 'bins': bins}


def plot(folder, filename, title, x, y, width=None, errors=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    if errors is None:
        ax.bar(x, y, width=width, color='mediumpurple',
               edgecolor='black', linewidth=0.2)
        ax.set_ylabel('Bacteria (pooled counts)')
    else:
        ax.errorbar(x, y, yerr=errors, fmt='o', markersize=3,
                    color='indigo', ecolor='mediumvioletred', capsize=2)
        ax.axhline(0, color='grey', linestyle='--')
        ax.set_ylabel('Mean WT - variant counts per subsample')
    ax.set_xlabel('Momentum (raw dataset units)')
    ax.set_title(title)
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(folder / filename, dpi=180)
    plt.close(fig)


def main():
    root = Path(__file__).resolve().parent
    data = root / 'data' if (root / 'data').is_dir() else root
    # Set0 contains only one event, so only Sets 1-10 are used.
    files = [data / f'output-Set{i}.txt' for i in range(1, 11)]
    missing = [p.name for p in files if not p.is_file()]
    if missing:
        print('Missing:', ', '.join(missing))
        return
    figures, results_dir = root / 'figures', root / 'results'
    figures.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)
    # Bin widths match the presentation; momentum units are not confirmed.
    widths = {i: (1 if i == 211 else 2) for _, i, _ in PAIRS}
    samples = []
    for path in files:
        print('Processing', path.name, flush=True)
        samples.append(analyse(path, widths))
    # Pooled abundance uses all selected bacteria divided by all valid events.
    valid_total = sum(s['valid'] for s in samples)
    total = sum(s['events'] for s in samples)
    selected = sum(sum(s['counts'].values()) for s in samples)
    print(f'Events: {total:,}; valid: {valid_total:,}; bacteria: {selected:,}')
    save_csv(results_dir, 'subsamples.csv',
             ['file', 'events', 'valid_events', 'invalid_lines', 'bacteria'],
             [[s['file'], s['events'], s['valid'], s['invalid'],
               sum(s['counts'].values())] for s in samples])
    abundance = []
    for bac_id, name in NAMES.items():
        count = sum(s['counts'][bac_id] for s in samples)
        # Sample SD measures variation between the ten subsample averages.
        averages = [s['counts'][bac_id] / s['valid'] for s in samples]
        average, sd = mean_sd(averages)
        abundance.append([bac_id, name, count, count / valid_total,
                          average, sd, sd / math.sqrt(len(averages))])
    save_csv(results_dir, 'abundance.csv',
             ['id', 'strain', 'total_count', 'pooled_mean_per_valid_event',
              'mean_of_subsample_averages', 'sample_sd', 'sem'],
             abundance)
    differences = []
    for name, wt, variant in PAIRS:
        # Paired differences are calculated per valid event in each subsample.
        values = [(s['counts'][wt] - s['counts'][variant]) / s['valid']
                  for s in samples]
        mean, sd = mean_sd(values)
        differences.append([name, mean, sd, sd / math.sqrt(len(values))])
        width = widths[wt]
        combined = defaultdict(int)
        for bac_id in (wt, variant):
            hist = defaultdict(int)
            for s in samples:
                for b, count in s['bins'][bac_id].items():
                    hist[b] += count
                    combined[b] += count
            keys = sorted(hist)
            plot(figures, f'momentum_{bac_id}.png', NAMES[bac_id],
                 [(b + .5) * width for b in keys],
                 [hist[b] for b in keys], width=width)
        keys = sorted(combined)
        plot(figures, f'momentum_combined_{wt}_{variant}.png', f'{name}: combined',
             [(b + .5) * width for b in keys],
             [combined[b] for b in keys], width=width)
        all_bins = range(math.ceil(60 / width))
        rows = []
        for b in all_bins:
            wt_total = sum(sample['bins'][wt].get(b, 0) for sample in samples)
            variant_total = sum(sample['bins'][variant].get(b, 0)
                                for sample in samples)
            mean_difference = (wt_total - variant_total) / len(samples)

            # For independent Poisson counts, Var(WT - variant) = WT + variant.
            # Divide by the number of subsamples because the graph shows their mean.
            poisson_error = math.sqrt(wt_total + variant_total) / len(samples)
            rows.append([(b + .5) * width, mean_difference, poisson_error])
        save_csv(results_dir, f'momentum_difference_{wt}_{variant}.csv',
                 ['momentum_bin_centre', 'mean_WT_minus_variant_counts',
                  'poisson_error_on_mean'], rows)
        plot(figures, f'asymmetry_{wt}_{variant}.png',
             f'{name}: mean difference ± Poisson uncertainty',
             [r[0] for r in rows], [r[1] for r in rows],
             errors=[r[2] for r in rows])
    save_csv(results_dir, 'differences.csv',
             ['species', 'mean_difference_per_valid_event', 'sample_sd', 'sem'],
             differences)
    print('\nOverall WT - variant difference per valid event (mean ± SD):')
    for name, mean, sd, sem in differences:
        print(f'{name}: {mean:.8f} ± {sd:.8f}')
    print('\n24 figures saved to:', figures)
    print('9 CSV files saved to:', results_dir)


if __name__ == '__main__':
    main()
