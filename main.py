def parse_input(path):
    with open(path, "r") as f:
        lines = f.readlines()

    c, p = lines[0].split()
    c, p = int(c), int(p)
    contributors = {}
    projects_info = {}
    projects_roles = {}
    k = 1
    for _ in range(c):
        c_name, n_skills = lines[k].split()
        k += 1
        n_skills = int(n_skills)
        contributors[c_name] = {}
        for _ in range(n_skills):
            skill, level = lines[k].split()
            level = int(level)
            contributors[c_name][skill] = level
            k += 1

    for _ in range(p):
        p_name, d, s, b, r = lines[k].split()
        k += 1
        d, s, b, r = int(d), int(s), int(b), int(r)
        projects_info[p_name] = (d, s, b, r)
        projects_roles[p_name] = {}
        for _ in range(r):
            skill, level = lines[k].split()
            level = int(level)
            projects_roles[p_name][skill] = level
            k += 1

    return contributors, projects_info, projects_roles


def find_first_available(skill, level, contributors, availability):
    best_c = None
    min_avail = float("+inf")
    level_up = False
    for c, skills in contributors.items():
        if (skill in skills) and (skills[skill] >= level) and (availability[c] < min_avail):
            best_c = c
            min_avail = availability[c]
            level_up = skill == level
    return best_c, level_up


def solve_project(p, contributors, projects_info, projects_roles, availability):
    d, s, b, r = projects_info[p]
    max_avail = 0
    c_list = []
    skills_list = []
    level_up_list = []
    for skill, level in projects_roles[p].items():
        c, level_up = find_first_available(skill, level, contributors, availability)
        if c is None:
            return None, None
        c_list.append(c)
        level_up_list.append(level_up)
        skills_list.append(skill)
        max_avail = max(availability[c], max_avail)

    last_day = max_avail + d - 1
    penalty = min(b - last_day - 1, 0)
    score = s + penalty

    for c in c_list:
        availability[c] = max_avail + d

    for c, level_up, skill in zip(c_list, level_up_list, skills_list):
        contributors[c][skill] += 1
    return score, c_list


def solve(contributors, projects_info, projects_roles):
    availability = {c: 0 for c in contributors}
    projects_order = [
        x[0] for x in sorted(projects_info.items(), key=lambda x: -(x[1][1] + x[1][2] - x[1][0] * x[1][3]))
    ]

    for p in projects_order:
        score, c_list = solve_project(p, contributors, projects_info, projects_roles, availability)
        print(p, score, c_list)


contributors, projects_info, projects_roles = parse_input("a_an_example.in.txt")
solve(contributors, projects_info, projects_roles)
