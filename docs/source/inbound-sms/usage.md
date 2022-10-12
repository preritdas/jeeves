# Usage

Get info on API usage. On each inbound sms use, the requested app and sender information is stored in a Deta Base for metrics (and, for this app). 

The formatting and parsing of data lookups is extremely bare bones right now, but because the data is all there, it's just a matter of making the response more organized, coherent, and insightful.


| Option | Description |
| --- | --- |
| date | If you want to filter the results by a certain date, ex. `2022-09-27`. |


`````{tabs}

````{tab} Sample Text

```text
app: usage
options: date = 2022-09-28
```
````

````{tab} Sample Response

```text
On 2022-10-12, I was pinged 17 times. App-specific pings are below.

{'jokes': 3, 'apps': 5, 'rt': 3, 'groceries': 4, 'invite': 2, 'usage': 1}

Person-specific pings:

{'Prerit Das': 18}
```
````
`````
