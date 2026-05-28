"""Functions for organizing and calculating student exam scores."""


def round_scores(student_scores):
    output=[]
    for score in student_scores:
        score =round(score)
        output.append(score)
        output=sorted(output)
    return output
    """Round all provided student scores.

    Parameters:
        student_scores (list[float]): Student exam scores.

    Returns:
        list[int]: Student scores *rounded* to the nearest integer value.
    """

    pass


def count_failed_students(student_scores):
    output=[]
    for score in student_scores:
        if score <=40:
             output.append(score)
    return len(output)

def above_threshold(student_scores, threshold):
    output=[]
    for score in student_scores:
        if score >=threshold:
             output.append(score)
    return output
    """Determine how many of the provided student scores were 'the best' based on the provided threshold.

    Parameters:
        student_scores (list[int]): Integer scores.
        threshold (int): The threshold to cross to be the "best" score.

    Returns:
        list[int]: Integer scores that are at or above the "best" threshold.
    """

    pass


def letter_grades(highest):
    output=[41]
    for number in range(1, 4):
        step = (highest - 40) // 4
        level=41+step*number
        output.append(level)
    output=sorted(output)
    return output
    
    
    """Create a list of grade thresholds based on the provided highest grade.

    Parameters:
        highest (int): The value of the highest exam score.

    Returns:
        list[int]: Lower threshold scores for each D-A letter grade interval.

        For example, where the highest score is 100, and failing is <= 40,
        The result would be [41, 56, 71, 86]:
            41 <= "D" <= 55
            56 <= "C" <= 70
            71 <= "B" <= 85
            86 <= "A" <= 100
    """

    pass


def student_ranking(student_scores, student_names):
    pairs = []
    for index in range(len(student_names)):
        name = student_names[index]
        score = student_scores[index]
        pairs.append([name,score])
    ranking = []
    for index in range(len(pairs)):
        name = pairs[index][0]
        score = pairs[index][1]
        ranking.append(f"{index + 1}. {name}: {score}")
    return ranking
    """Organize the student's rank, name, and grade information in descending order.

    Parameters:
        student_scores (list): Scores in descending order.
        student_names (list[str]): Student names by exam score in descending order.

    Returns:
        list[str]: Strings in format ["<rank>. <student name>: <score>"].
    """

    pass


def perfect_score(student_info):
    for student in student_info:
        if student[1]==100:
            return student
    return []

    """Create a list that contains the name and grade of the first student to make a perfect score on the exam.

    Parameters:
        student_info (list[list[str, int]]): List of [<student name>, <score>] lists.

    Returns:
        list: First `[<student name>, 100]` found OR `[]` if no student score of 100 is found.
    """

    pass
