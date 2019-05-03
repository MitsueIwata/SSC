from flask import Flask, render_template, request
from datetime import datetime
from flaskext.markdown import Markdown
import os
import json

app = Flask(__name__)
app.config['DEBUG'] = True

Markdown(app)

PATH = 'static/events'

# creates list of upcoming and past events


def get_events_lists():
    upcoming = []
    past = []
    present = datetime.now().date()

    for f in os.listdir(PATH):
        try:
            year, mon, day = int(f[0:4]), int(f[5:7]), int(f[8:10])
            if datetime.date(datetime(year, mon, day)) < present:
                event_dict = file_to_dict(f)
                event_dict['filename'] = f
                past.append(event_dict)
            else:
                event_dict = file_to_dict(f)
                event_dict['filename'] = f
                upcoming.append(event_dict)
            upcoming = sorted(upcoming, key=lambda event: event['filename'])
            past = sorted(past, key=lambda event: event['filename'])
        except:
            print('{} does not match event file naming convention'.format(f))
    return upcoming, past


def get_scopeathon_schedule():
    """Return ordered agenda dict for the two scopeathon days.

    :return: <Dict> Return day1 and day2 scopeathon event lists
    """
    events = []

    with open('static/agenda/agenda_2018.json') as file:
        events = json.load(file)

    return events


@app.route('/resources')
def resources():
    resources = get_scoping_resources()
    return render_template('resources.html', resources=resources, hack_flag=True)


def get_scoping_resources():
    with open('static/scoping_resources/resources.json') as file:
        resources = json.load(file)
    return resources

# makes event.txt into dictionary
def file_to_dict(filename):
    file_dict = {}
    with open(os.path.join(PATH, filename)) as f:
        content = f.read().split('|')
        if len(content) < 4:
            file_dict['title'] = content[0]
            file_dict['date'] = content[1]
            file_dict['description'] = content[2]
        else:
            file_dict['title'] = content[0]
            file_dict['date'] = content[1]
            file_dict['description'] = content[2]
            file_dict['website'] = content[3]
    return file_dict


@app.route('/')
def root():
    upcoming, _ = get_events_lists()
    return render_template('index.html', upcoming=upcoming, home_flag=True)


@app.route('/about')
def about():
    return render_template('about.html', about_flag=True)


@app.route('/scopeathon')
def scopeathon():
    _, past = get_events_lists()
    events = get_scopeathon_schedule()
    past.reverse()
    return render_template('2018scopeathon.html', events=events, past=past, hack_flag=True)

@app.route('/archive')
def archive_v2():
    _, past = get_events_lists()
    past.reverse()
    return render_template('past_events.html', past=past)

@app.route('/events_archive')
def archive():
    _, past = get_events_lists()
    past.reverse()
    return render_template('event_archive.html', past=past)


@app.route('/contact')
def contact():
    return render_template('contact.html', cont_flag=True)


@app.route('/error')
def error():
    return render_template('404.html')


@app.route('/civic-leaders')
def sponsors():
    return render_template('sponsors.html')


@app.route('/mentors')
def mentors():
    return render_template('mentors.html')


@app.route('/participants')
def participants():
    return render_template('participants.html', participants_flag=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
