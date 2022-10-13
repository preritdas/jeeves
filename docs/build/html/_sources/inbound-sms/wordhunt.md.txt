# WordHunt

Solve a WordHunt board (Game Pigeon).

```{eval-rst}
.. image:: https://i.stack.imgur.com/JsxLT.jpg
    :alt: my-picture1
    :width: 200
```

APP_HELP = "Solve a WordHunt board."
APP_OPTIONS = {
    "height": "board height, default 4",
    "width": "board width, default 4",
    "limit": "max number of results, default 20"
}

| Option | Description |
| --- | --- |
| height | Board height. Default is 4. |
| width | Board width. Default is 4. |
| limit | Max number of results. Default is 20. |


`````{tabs}

````{tab} Sample Text

```text
app: wordhunt
oatrihpshtnrenei
```
````

````{tab} Sample Response

```text
2, 2 - haptens
2, 2 - haptene
3, 2 - pterins
4, 2 - staithe
1, 3 - hennier
1, 3 - henners
2, 3 - tenners
2, 2 - hapten
3, 2 - pterin
4, 2 - sprint
4, 2 - sprent
4, 2 - staith
1, 3 - henner
2, 3 - tenner
3, 3 - niente
4, 3 - rennet
1, 4 - enters
4, 4 - inners
4, 4 - inters
2, 1 - apter
2, 2 - haith
```
````
`````

The coordinates, ex. `2, 2`, are board coordinates, starting at `1, 1` (not `0, 0`). The results are sorted first by number of points, then by board position. 
