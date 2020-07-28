# SLU_AutoScriptForNewCourseSystem

![](https://img.shields.io/badge/tests-pass%20|%202019.1.4-brightgreen)
![](https://img.shields.io/badge/dependencies-python3.7-blue)

Due to the shortage of teaching resources, Shanghai Lixin University provides an decreasing number of courses that students can select. However, since the server of course system always break down due to that too many students visit the course selecting pages, students usually cannot take the courses they like.

Therefore, I make a script to autometically select courses. Fill the information in the blanks, and start it several seconds before the course selecting starts, and the program will use multiple threadings to help you select courses.

## Disclaimer
1. Commercial use is NOT permitted.
2. It is not allowed to set up too many processes, causing the server to break down due to excessive number of connections.
3. This script does not have a function of cancelling course selection.
4. This tool is just for feasibility test. If you are punished by the school, it is never related to this tool.

## Usage

1. Input username, password, number of threadings for login, number of threadings for course selection in `cfg_public.py`.
2. **During the pre-selecting round,** run `lixin1_listing.py` to save all the courses to a local `*.txt` file. Then, input the list of courses to select in `cfg_public.py`.
3. **Several seconds before selecting starts,** run `__init__.py` and monitor its running. Immediately stop it after you get courses you need.
