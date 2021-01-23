import Levenshtein
import sys


def match_properties(obj_first, obj_second):
    keys_first = {obj_first[i]['prop']['value'] for i in range(len(obj_first))}
    keys_second = {obj_second[i]['prop']['value'] for i in range(len(obj_second))}
    matched_keys = keys_first.intersection(keys_second)
    mismatched_keys_first = keys_first - matched_keys
    mismatched_keys_second = keys_second - matched_keys
    matched = {}
    mismatched = {}
    for key in matched_keys:
        matched[key] = {'first': [], 'second': []}
    for key in mismatched_keys_first | mismatched_keys_second:
        mismatched[key] = None
    for i in range(len(obj_first)):
        key = obj_first[i]['prop']['value']
        if key in matched_keys:
            matched[key]['first'].append(i)
    for i in range(len(obj_second)):
        key = obj_second[i]['prop']['value']
        if key in matched_keys:
            matched[key]['second'].append(i)
    return matched, mismatched


def linear_dist(x, y):
    return abs(int(x) - int(y))


def iterate_over_key(obj_first, obj_second, matched, key, dist_function):
    lowest_distance = sys.maxsize
    for pos_match_first in matched[key]['first']:
        for pos_match_second in matched[key]['second']:
            dist = dist_function(obj_first[pos_match_first]['val']['value'],
                                 obj_second[pos_match_second]['val']['value'])
            if dist < lowest_distance:
                lowest_distance = dist
    return lowest_distance


def calculate_metric(obj_first, obj_second):
    matched, mismatched = match_properties(obj_first, obj_second)
    scores = {}
    for key in matched.keys():
        if key in ("http://schema.org/datePublished", "http://schema.org/dateCreated"):
            lowest_distance = iterate_over_key(obj_first, obj_second, matched, key, linear_dist)
        else:
            lowest_distance = iterate_over_key(obj_first, obj_second, matched, key, Levenshtein.distance)
        scores[key] = 1 / (1 + lowest_distance)
    score = sum(scores.values()) / (len(matched) + len(mismatched) / 2)
    return {'total_score': score, 'partial_scores': scores}
