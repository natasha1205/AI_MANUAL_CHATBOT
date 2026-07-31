import os
import re


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


MANUAL_PATH = os.path.join(
    BASE_DIR,
    "manual",
    "manual.txt"
)


OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "manual",
    "clean_manual.txt"
)



def extract_alarm(text):

    alarms = []


    # split every alarm number

    sections = re.split(
        r"(?=No\.\s*:\s*\d+)",
        text
    )


    for section in sections:


        if "Alarm Name" not in section:
            continue



        alarm = clean_section(section)


        if alarm:

            alarms.append(alarm)



    return alarms



def clean_section(section):


    section = section.replace(
        "\n",
        " "
    )


    section = re.sub(
        r"\s+",
        " ",
        section
    )



    alarm_name = extract(
        section,
        "Alarm Name",
        "Description"
    )


    description = extract(
        section,
        "Description",
        "Cause"
    )


    cause = extract(
        section,
        "Cause",
        "Screen Display"
    )


    screen = extract(
        section,
        "Screen Display",
        "Machine State"
    )


    machine = extract(
        section,
        "Machine State",
        "Solution"
    )


    solution = extract(
        section,
        "Solution",
        None
    )



    result=f"""

Alarm Name:
{alarm_name}


Description:
{description}


Cause:
{cause}


Screen Display:
{screen}


Machine State:
{machine}


Solution:
{solution}

"""


    return result



def extract(text,start,end):


    try:

        if end:

            value=text.split(start)[1].split(end)[0]

        else:

            value=text.split(start)[1]


        return value.strip()


    except:

        return ""





# =====================
# RUN
# =====================


with open(
    MANUAL_PATH,
    "r",
    encoding="utf-8"
) as file:

    content=file.read()



alarms = extract_alarm(
    content
)



with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:


    for alarm in alarms:

        file.write(alarm)

        file.write(
            "\n\n====================\n\n"
        )



print(
    "Completed"
)


print(
    "Total alarms:",
    len(alarms)
)


print(
    "Saved:",
    OUTPUT_PATH
)