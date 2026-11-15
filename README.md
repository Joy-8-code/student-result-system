# Student Result Management System

A menu-driven Python application for managing student records, scores, grades and reports.

## Features
- Add, view, search, update and delete students
- Record scores for 5+ subjects, update scores
- Total, average and grade (A-F) calculation; report cards
- Sort by average or name; class statistics
- Save a text report to a file
- JSON data persistence (data/students.json, created automatically)

## Run
Requires Python 3.8+ (no external libraries).

    python main.py

## Grading
A: 70+, B: 60-69, C: 50-59, D: 40-49, F: below 40

## Structure
- main.py - menu and user input
- student.py - Student class, ID/date validation (regex)
- results.py - totals, averages, grades, statistics
- storage.py - load/save JSON
- reports.py - report card, tables, text report

## Python concepts used
Variables and type conversion, if/elif/else, loops, lists/dicts/tuples, functions,
sorting (sorted with key), try/except/else, file handling (json), modules,
OOP (Student class), datetime, regular expressions, os module.
