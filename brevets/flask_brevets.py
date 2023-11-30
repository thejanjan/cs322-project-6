"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import logging
import os

import brevet_db

###
# Globals
###
app = flask.Flask(__name__)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    start_time = request.args.get('start_time', '2021-01-01T00:00', type=str)
    brevet_dist = request.args.get('brevet_dist', 200, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("start_time={}".format(start_time))
    app.logger.debug("brevet_dist={}".format(brevet_dist))
    app.logger.debug("request.args: {}".format(request.args))

    start_time_arrow = arrow.get(start_time)
    try:
        open_time = acp_times.open_time(km, brevet_dist, start_time_arrow).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(km, brevet_dist, start_time_arrow).format('YYYY-MM-DDTHH:mm')
    except AssertionError:
        open_time = start_time_arrow.format('YYYY-MM-DDTHH:mm')
        close_time = start_time_arrow.format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_submit")
def _submit():
    app.logger.debug("Got a submit request")

    # Parse json.
    try:
        start_time = request.args.get('start_time', '2021-01-01T00:00', type=str)
        brevet_dist = request.args.get('brevet_dist', 200, type=float)
        controls = [val for key, val in request.args.items(multi=True)
                    if key == 'controls']
        locations = [val for key, val in request.args.items(multi=True)
                     if key == 'locations']

        app.logger.debug("start_time={}".format(start_time))
        app.logger.debug("brevet_dist={}".format(brevet_dist))
        app.logger.debug("controls={}".format(controls))
        app.logger.debug("locations={}".format(locations))
        app.logger.debug("request.args: {}".format(request.args))
    except Exception as e:
        # Json parsing failed.
        app.logger.debug("submit json parse failure: {}".format(e))
        return flask.jsonify(result={"code": 1})

    # If no controls, don't store anything
    if all(c == '' for c in controls):
        return flask.jsonify(result={"code": 3})

    # Store values in db.
    try:
        if brevet_db.store_brevet(start_time, brevet_dist, controls, locations, app) == -1:
            app.logger.debug("db store attempt fail")
            return flask.jsonify(result={"code": 2})
    except Exception as e:
        # DB entry failed.
        app.logger.debug("db entry failure: {}".format(e))
        return flask.jsonify(result={"code": 2})

    # Send result and callback.
    return flask.jsonify(result={"code": 0})


@app.route("/_display")
def _display():
    app.logger.debug("Got a display request")

    # Try to get DB value.
    try:
        query = brevet_db.get_brevet(app=app)
        app.logger.debug("query={}".format(query))
    except Exception as e:
        # DB query failed.
        app.logger.debug("db query failure: {}".format(e))
        return flask.jsonify(result={"code": 1})

    # Return result.
    return flask.jsonify(result={"code": 0, "query": query})


#############

if __name__ == "__main__":
    app.debug = os.environ.get('DEBUG')
    if app.debug:
        app.logger.setLevel(logging.DEBUG)

    port = os.environ.get('PORT')
    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
