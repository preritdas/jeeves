# Groceries

Organize a grocery list by category and location for shopping at peak efficiency.


`````{tabs}

````{tab} Sample Text

```text
app: groceries
options: add = yes; id = 9a8scd; setup = whole foods

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
