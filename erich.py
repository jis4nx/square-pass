"""
Demonstrates a dynamic Layout
"""



from datetime import datetime

from time import sleep



from rich.panel import Panel
from rich.markdown import Markdown
from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from rich import box


from rich.live import Live
from rich.text import Text

console = Console()
layout = Layout()

layout.size =2


vars = """
  
## Supported Sequences
### Mathseq is python library that helps to generate inifinite sequences real quick ..</p>

- Fibonacci

- Lucas Number

- Prime Number
    - end (Positional Argument)

- Catalan Number

- Vaneck's sequence

- Composite Numbers

- Pronic Numbers

- Random sequence
    - seed
    - type

- Look and say
    - inverse

<br>

## Installation
<br>

**Using pip** 

    $ pip install mathseq

<br>

## Usage
<br>

**Imports**

```python

>>>from mathseq import seq

```
<br>

**Create Objects**

```python

>>>from mathseq import seq
>>>
>>>fibonacci = seq.fibonacci()
>>>fibonacci
<generator object fibonacci at 0x0000020F83BEC648>
>>>

```
<br>

**Iteration**


```python

from mathseq import seq

fibonacci = seq.fibonacci()

#printing through desired range
desired_range = 10
for _ in range(desired_range):
    fib = next(fibonacci)
    print(fib)


#keep generating to the infinity
for fib in fibonacci:
    print(fib)

```

<br>

**Use List Comprehension**
<br>

```python


from mathseq import seq

fibonacci = seq.fibonacci()
catalan = seq.catalan_numbers()

fib_list = [next(fibonacci) for _ in range(10)]
cat_list = [next(catalan) for _ in range(10)]

print("List of Fibonacci Numbers",fib_list)
print("List of Catalan Numbers",cat_list)

```
<br>

**Sequences**
<br>

```python


from mathseq import seq

luca = seq.lucas_number()
fibonacci = seq.fibonacci()
prime = seq.prime_numbers(100)
comp = seq.composite_numbers()
odd =seq.odd_seq()
even = seq.even_seq()
odd_inv =seq.odd_seq(inverse=True)
even_inv = seq.even_seq(inverse=True)
cat = seq.catalan_numbers()
van = seq.vaneck_seq()
pronic = seq.pronic_numbers()
xbo_six = seq.xibonacci(3)

```
<br>

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@Shoaib Islam](https://www.github.com/TheGreatestShoaib)

<br>

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.



"""

import os

os.system("clear")




dd = Panel(
            Markdown(vars
            ),
            box=box.ROUNDED,
            padding=(1, 2),
            title="[b red]Thanks for trying out Rich!",
            border_style="bright_blue",
        )



# layout.update(dd)
console.print(dd)


# console.print(layout)



# print(dir(layout))

# print(print(layout))
# obj = layout
# print(obj)

# class Clock:
    # """Renders the time in the center of the screen."""

    # def __rich__(self) -> Text:
        # return Text(datetime.now().ctime(), style="bold magenta", justify="center")



# with Live(layout, screen=True, redirect_stderr=False) as live:
    # try:
        # while True:
            # sleep(1)
    # except KeyboardInterrupt:
        # pass
