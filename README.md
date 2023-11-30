# UOCIS322 - Project 6 #

- Author: Micah Nichols
- Contact: micahanichols27@gmail.com

This application provides a calculator for determining the opening and closing times of defined controle checkpoints for a RUSA ACP Brevet.

## Algorithm

The open and close times are based on the individual control distance, the complete distance of the brevet, and the start time of the brevet.
To align with rider endurance, different kilometer spans have defined speed ranges (hovering around 15 km/hr min, 30 km/hr max).

The open times are based on the total time it would take to reach the control distance based on the maximum speed of each defined span.
The closed times are calculated similarly, but instead use the minimum speed of each defined span.
In addition, each brevet has a time limit for the close time of the final control, and the close time of the initial control is always one hour after opening.

The close time of brevets within the first 60 kilometers are calculated at 20 km/hr, and are allotted an additional hour.

## Startup

Navigate to the root directory and run:

`docker compose up -d`

The application will then be available at `localhost:5002`.

## Application

On the webpage, you can configure the brevet distance and its start time at the top.
From there, you can specify either miles or kilometers to obtain their open and close times. (One may also specify an optional location parameter.)

Pressing the Submit button will store all values in the form in a database. Pressing Display will retrieve all values and re-populate the table.

## API

Table of API requests:

|        | brevet                                                         | brevets                                                              |
|--------|----------------------------------------------------------------|----------------------------------------------------------------------|
| URL    | `http://localhost:5001/api/brevet/<brevet_id>`                 | `http://localhost:5001/api/brevets`                                  |
| GET    | Returns a brevet with a given id.                              | Returns all brevets stored in the database.                          |
| DELETE | Deletes a brevet with a given id.                              | N/A                                                                  |
| PUT    | Updates a brevet of a given id with the response format below. | N/A                                                                  |
| POST   | N/A                                                            | Inserts a brevet with the request format below. Returns a brevet id. |

The request format is shown below:

```json
{
  "start_time": "YYYY-MM-DD HH:mm",
  "length": float,
  "distances": float[],
  "locations": str[],
  "open_times": "YYYY-MM-DD HH:mm"[],
  "close_times": "YYYY-MM-DD HH:mm"[]
}
```
