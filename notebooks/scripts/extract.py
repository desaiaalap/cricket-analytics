import yaml
import pandas as pd
import glob
import os



def extract_deliveries(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    innings = data['innings']
    rows = []

    for inning in innings:
        for inning_name, inning_data in inning.items():
            team = inning_data['team']
            for delivery in inning_data['deliveries']:
                for ball_number, ball_info in delivery.items():
                    row = {
                        'inning': inning_name,
                        'batting_team': team,
                        'ball': ball_number,
                        'batsman': ball_info.get('batsman'),
                        'bowler': ball_info.get('bowler'),
                        'runs': ball_info['runs']['total'],
                        'extras': ball_info.get('extras', {}),
                        'wicket': ball_info.get('wicket', {})
                    }
                    rows.append(row)
    return pd.DataFrame(rows)


def convert_yaml_to_csv():
    """
    Convert YAML files to CSV format.
    """
    file_paths = glob.glob('data/external/icc_mens_t20_world_cup_male/*.yaml')
    skip_counter = 0
    total_files = len(file_paths)
    print(f"Total files to process: {total_files}")
    
    for file_path in file_paths:
        print(f"Processing {file_path}")
        try:
            df = extract_deliveries(file_path)

            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            innings = data.get('innings', [])
            info = data.get('info', {})
            raw_date = info.get('dates', ['unknown'])[0]

            if isinstance(raw_date, str):
                match_date_str = raw_date.replace('-', '')
            elif hasattr(raw_date, 'strftime'):
                match_date_str = raw_date.strftime('%Y%m%d')
            else:
                match_date_str = 'unknown_date'

            if len(innings) < 2:
                raise ValueError("Incomplete innings info")

            team1 = innings[0].get(list(innings[0].keys())[0], {}).get('team', 'Team1')
            team2 = innings[1].get(list(innings[1].keys())[0], {}).get('team', 'Team2')

            # Sanitize names
            team1_clean = team1.replace(" ", "_")
            team2_clean = team2.replace(" ", "_")

            match_name = f"{match_date_str}_{team1_clean}_vs_{team2_clean}.csv"
            output_path = os.path.join('data/raw', match_name)

            df.to_csv(output_path, index=False)
            print(f"✅ Saved CSV to: {output_path}")

        except Exception as e:
            print(f"⚠️ Skipping {file_path} due to error: {e}")
            skip_counter += 1
            continue

    print("\n--- Summary ---")
    print("✅ Files processed:", total_files - skip_counter)
    print("⚠️ Files skipped:", skip_counter)