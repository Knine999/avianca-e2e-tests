# Manual validation of Test 4

This is a manual walk-through of the one-way flow on the English site, done by hand in a normal browser. It is not automated.

## Setup

- Site: https://www.avianca.com/en
- Date of the run: 2026-10-27 (local time)
- Origin: Miami (MIA). Destination: San Andres (ADZ). Two adults. Departure 14 days ahead.
- Browser: Google Chrome.

## Numbering

The challenge lists 20 entries under labels 1 to 18. Labels 13 and 16 each appear twice. The table uses the position in the list (1 to 20) and shows the challenge label next to it.

## Results

| Position | Label | Result | Notes |
|---|---|---|---|
| 1 | 1 | Pass | Cookie banner appeared. Accepting it removed the dark overlay. Round trip is available and the origin shows Miami. |
| 2 | 2 | Pass | Choosing One way removes the Return field. |
| 3 | 3 | Pass | San Andres fills the destination as expected. |
| 4 | 4 | Fail | The selected date is correct, but the Departure field shows it as MM/DD/YYYY. The challenge expects DD/MM/YYYY. |
| 5 | 5 | Pass | Adult count is 2, and the minus and plus icons are enabled. Matches the expected result. |
| 6 | 6 | Pass | Dropdown closes and the passenger selection is kept. Matches the expected result. |
| 7 | 7 | Pass | Booking page shows the outbound flights for the selected itinerary. Matches the expected result. |
| 8 | 8 | Pass | Fare options are displayed. Matches the expected result. |
| 9 | 9 | Pass | Upgrade pop-up opens. Matches the expected result. |
| 10 | 10 | Pass | Trip Summary screen is displayed. Matches the expected result. |
| 11 | 11 | Pass | Passenger Information screen opens. Matches the expected result. |
| 12 | 12 | Pass | Passenger details for both passengers are entered. Matches the expected result. |
| 13 | 13 | Pass | Contact details. |
| 14 | 13 | Pass | Click Continue. |
| 15 | 14 | Pass | The baggage section was not displayed for this itinerary. |
| 16 | 15 | Pass | Priority Boarding. |
| 17 | 16 | Pass | Save and Exit. |
| 18 | 16 | Pass | Go to Payment. |
| 19 | 17 | Pass | Purchase summary. |
| 20 | 18 | Pass | Close the browser. |

The run stopped at checkout, before payment. No payment data was entered or submitted. The browser was then closed (label 18).
