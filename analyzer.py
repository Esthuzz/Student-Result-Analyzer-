import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt


def read_data(path):
    df = pd.read_csv(path)
    return df


def compute_statistics(df, pass_mark=40):
    # assume subject columns are all numeric columns except StudentID and Name
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    # if StudentID is numeric, exclude it
    possible_id = ['StudentID', 'ID']
    subject_cols = [c for c in numeric_cols if c not in possible_id]
    df['Average'] = df[subject_cols].mean(axis=1)

    topper_row = df.loc[df['Average'].idxmax()]
    topper = {'StudentID': topper_row.get('StudentID', ''), 'Name': topper_row.get('Name', ''), 'Average': topper_row['Average']}

    # pass if all subject marks >= pass_mark
    passed = (df[subject_cols] >= pass_mark).all(axis=1)
    pass_percentage = 100.0 * passed.sum() / len(df) if len(df) > 0 else 0.0

    subject_averages = df[subject_cols].mean()

    return {
        'df': df,
        'topper': topper,
        'pass_percentage': pass_percentage,
        'subject_averages': subject_averages,
        'passed_flags': passed,
        'subject_cols': subject_cols,
    }


def plot_results(stats, out_dir='outputs', show=False):
    os.makedirs(out_dir, exist_ok=True)

    df = stats['df']
    subject_averages = stats['subject_averages']

    # Histogram of student averages
    plt.figure(figsize=(8, 5))
    plt.hist(df['Average'], bins=8, color='tab:blue', edgecolor='black')
    plt.title('Distribution of Student Averages')
    plt.xlabel('Average')
    plt.ylabel('Number of Students')
    hist_path = os.path.join(out_dir, 'averages_hist.png')
    plt.tight_layout()
    plt.savefig(hist_path)
    if show:
        plt.show()
    plt.close()

    # Bar chart of subject averages
    plt.figure(figsize=(8, 5))
    subject_averages.plot(kind='bar', color='tab:green')
    plt.title('Average Marks per Subject')
    plt.ylabel('Average')
    bar_path = os.path.join(out_dir, 'subject_averages.png')
    plt.tight_layout()
    plt.savefig(bar_path)
    if show:
        plt.show()
    plt.close()

    # Pass vs Fail pie
    passed = stats['passed_flags'].sum()
    failed = len(stats['df']) - passed
    plt.figure(figsize=(6, 6))
    plt.pie([passed, failed], labels=['Pass', 'Fail'], autopct='%1.1f%%', colors=['#2ca02c', '#d62728'])
    plt.title('Pass vs Fail')
    pie_path = os.path.join(out_dir, 'pass_pie.png')
    plt.savefig(pie_path)
    if show:
        plt.show()
    plt.close()

    return {'hist': hist_path, 'bar': bar_path, 'pie': pie_path}


def print_summary(stats):
    topper = stats['topper']
    print('Topper: {} ({}) — Average: {:.2f}'.format(topper.get('Name', ''), topper.get('StudentID', ''), topper.get('Average', 0)))
    print('Pass percentage: {:.2f}%'.format(stats['pass_percentage']))
    print('\nSubject averages:')
    print(stats['subject_averages'].to_string())


def main():
    parser = argparse.ArgumentParser(description='Student Result Analyzer')
    parser.add_argument('csv', nargs='?', default='data/students.csv', help='Path to students CSV')
    parser.add_argument('--pass-mark', type=int, default=40, help='Pass mark (default 40)')
    parser.add_argument('--out', default='outputs', help='Output directory for graphs')
    parser.add_argument('--show', action='store_true', help='Show plots interactively')
    args = parser.parse_args()

    df = read_data(args.csv)
    stats = compute_statistics(df, pass_mark=args.pass_mark)
    print_summary(stats)
    paths = plot_results(stats, out_dir=args.out, show=args.show)
    print('\nSaved plots:')
    for k, v in paths.items():
        print('-', v)


if __name__ == '__main__':
    main()
