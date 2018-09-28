"""
MIT License

Copyright (c) 2018 https://github.com/pragma-once

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
import requests

current_version = "0.1"


class Lecture:
    def __init__(self, name: str, last_submitted_date: datetime.datetime, period: datetime.timedelta):
        self.name = name
        self.last_submitted_date = last_submitted_date
        self.period = period
        self.next_date = self.last_submitted_date \
                         + (int((datetime.datetime.now() - self.last_submitted_date) / self.period) * self.period) \
                         + self.period
        if datetime.datetime.now() < self.last_submitted_date:
            self.next_date -= self.period

    def __lt__(self, other):
        return self.last_submitted_date < other.last_submitted_date


latest_version = current_version
latest_version_link = ""

print("Kharazmi University Lectures date Checker v" + current_version)

while 1:
    print("Getting online info...")
    info = requests.get("https://kharazmi-lectures-checker.github.io/info_0_1.html").text.split(';')

    lecture_name = "N/A"
    last_submitted_date = None
    period = None
    lectures = []


    def clear_info():
        global lecture_name
        global last_submitted_date
        global period
        lecture_name = "N/A"
        last_submitted_date = None
        period = None


    def add_info():
        if not (last_submitted_date is None or period is None):
            lectures.append(Lecture(lecture_name, last_submitted_date, period))
            clear_info()


    for block in info:
        exp = block.split('=')
        if len(exp) < 2:
            continue
        if exp[0] == "lecture" or exp[0] == "lecture_name":
            clear_info()
            lecture_name = exp[1]
        if exp[0] == "last_submitted_date":
            try:
                last_submitted_date = datetime.datetime(year=int(exp[1][0:4]),
                                                        month=int(exp[1][5:7]),
                                                        day=int(exp[1][8:10]),
                                                        hour=12)

                last_submitted_date = datetime.datetime(year=int(exp[1][0:4]),
                                                        month=int(exp[1][5:7]),
                                                        day=int(exp[1][8:10]),
                                                        hour=int(exp[1][11:13]),
                                                        minute=int(exp[1][14:16]))
            except:
                pass
            add_info()
        elif exp[0] == "period":
            try:
                period = datetime.timedelta(days=int(exp[1]))
            except:
                pass
            add_info()
        elif exp[0] == "latest_version":
            latest_version = exp[1]
        elif exp[0] == "latest_version_link":
            latest_version_link = exp[1]

    lectures.sort()

    now = datetime.datetime.now()
    now_rounded = datetime.datetime(year=now.year, month=now.month, day=now.day)
    print()
    for lecture in lectures:
        next_date_rounded = datetime.datetime(year=lecture.next_date.year,
                                              month=lecture.next_date.month,
                                              day=lecture.next_date.day)
        if next_date_rounded - now_rounded < datetime.timedelta(days=0):
            relative_date = "This is IMPOSSIBLE! This is a bug! The 'next date' cannot be before now."
        elif next_date_rounded - now_rounded <= datetime.timedelta(days=0):
            relative_date = "Today"
        elif next_date_rounded - now_rounded <= datetime.timedelta(days=1):
            relative_date = "Tomorrow"
        else:
            weeks = int((next_date_rounded - now_rounded).days / 7)
            if (next_date_rounded.weekday() + 2) % 7 < (now_rounded.weekday() + 2) % 7:
                weeks += 1
            if weeks == 0:
                relative_date = "This week"
            elif weeks == 1:
                if now_rounded.weekday() == 4:
                    relative_date = "Coming week"
                else:
                    relative_date = "Next week"
            else:
                relative_date = str(weeks) + " weeks later"

        if lecture.next_date.weekday() == 5: weekday = "Sat"
        elif lecture.next_date.weekday() == 6: weekday = "Sun"
        elif lecture.next_date.weekday() == 0: weekday = "Mon"
        elif lecture.next_date.weekday() == 1: weekday = "Tue"
        elif lecture.next_date.weekday() == 2: weekday = "Wed"
        elif lecture.next_date.weekday() == 3: weekday = "Thu"
        elif lecture.next_date.weekday() == 4: weekday = "Fri"
        else: weekday = "Cool! That's a bug that seems impossible!"

        print("Next " + lecture.name + " lecture will be at: " + weekday + " " + str(lecture.next_date)
              + " (" + relative_date + ")")

    if current_version != latest_version:
        print()
        print("Current version: " + current_version)
        print("Latest version: " + latest_version)
        print("You can download the latest version from: " + latest_version_link)
        print("Do you want to download the latest version? (y/*)")
        if input() == "y":
            open(__file__, 'wb').write(requests.get(latest_version_link).content)

    print("Enter r to retry and anything to exit:")

    if input() != 'r':
        break
