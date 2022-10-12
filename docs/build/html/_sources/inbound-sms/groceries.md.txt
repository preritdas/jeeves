# Groceries

Organize a grocery list by category and location for shopping at peak efficiency.


| Option | Description |
| --- | --- |
| add | If you want to append the contents of the current message to a previous list, properly re-sorted. This could also be useful if working with a long grocery list, breaching the 160 character text limit. |
| setup | Custom grocery setup, ex. `whole foods`, to order the list categories according to the store layout. Maximum shopping efficiency. |


`````{tabs}

````{tab} Sample Text

```text
app: groceries
options: add = last; setup = whole foods

2 apples
3 bananas
chicken
snacks
1 hair dye
```
````

````{tab} Sample Response

```text
List ID: 7asdc87

Fruit:
- 2 apples
- 3 bananas
- blueberries

Self Care:
- 1 hair dye

Meat:
- chicken
- 1 lamb
- 2 sausages

Snacks
- Snacks

```
````
`````


## Formatting guidelines

There really aren't any hard guidelines, just a few things to be aware of to avoid crashing the classification algorithm. 

- Don't used dashed lists. 
- New line for each item.
- Quantities go at the beginning, in numeric form. They are optional.
- Add special options in parenthesis, ex. `3 apples (the good ones)`
- Setup is optional. It efficiently reorders the categories based on store layout. 
  - Setup line is case insensitive
  - Line between setup and content is unnecessary
