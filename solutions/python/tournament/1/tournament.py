def tally(rows):
    header = "Team                           | MP |  W |  D |  L |  P"

    teams = {}

    def add_team(team_name):
        if team_name not in teams:
            teams[team_name] = {
                "MP": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "P": 0,
            }

    for row in rows:
        first_team, second_team, result = row.split(";")

        add_team(first_team)
        add_team(second_team)

        # 两支球队都参加了一场比赛
        teams[first_team]["MP"] += 1
        teams[second_team]["MP"] += 1

        # result 描述的是第一支球队的结果
        if result == "win":
            teams[first_team]["W"] += 1
            teams[first_team]["P"] += 3
            teams[second_team]["L"] += 1

        elif result == "loss":
            teams[first_team]["L"] += 1
            teams[second_team]["W"] += 1
            teams[second_team]["P"] += 3

        elif result == "draw":
            teams[first_team]["D"] += 1
            teams[first_team]["P"] += 1

            teams[second_team]["D"] += 1
            teams[second_team]["P"] += 1

    sorted_team_names = sorted(
        teams,
        key=lambda team_name: (
            -teams[team_name]["P"],
            team_name,
        ),
    )

    result_table = [header]

    for team_name in sorted_team_names:
        team = teams[team_name]

        line = (
            f"{team_name:<31}"
            f"| {team['MP']:>2} "
            f"| {team['W']:>2} "
            f"| {team['D']:>2} "
            f"| {team['L']:>2} "
            f"| {team['P']:>2}"
        )

        result_table.append(line)

    return result_table