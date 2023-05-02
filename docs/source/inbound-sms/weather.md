# Weather

Weather summary and data highlights.

| Option | Description |
| --- | --- |
| city | Optional. The default is set in `config.yaml`. |
| state | Optional. A U.S. state, if the `city` is in the U.S. The city is usually sufficient. |
| country | Optional, a country ISO code. As with `state`, the `city` is usually sufficient. |  


`````{tabs}

````{tab} Sample Text

```text
app: weather
options: city = london
```
````

````{tab} Sample Response

```text
It's currently 57 degrees outside. Today's high will be 58 degrees; the low will be 55 degrees. The sun will set at 5:12 pm.
```
````
`````
