# fera 

fera is a general purpose procedural programming language that targets Brainfuck.
With fera it is possible to write programs that would be extremely complicated 
if written by hand.

## Syntax

The syntax of fera is inspired by C. A program in fera is made up of 4 parts. The first part is the `data` region, in the data region you declare global variables.
The second part of a fera program are the `inline` blocks, inline blocks of code
are routines that can be called from fera, but are pure brainfuck (along with some
helper compiler directives). The third part of a fera program contains the `proc`
blocks, proc's are procedures of fera code. Finally, the `entry` block is the entry
point of your fera program.

## Data types

At the moment the fera compiler only understands how to generate code for two 
data types: `byte` and `byte[]`. Byte is identical to one cell in a brainfuck
machine. However, `byte[]` contains 4 extra bytes of header data which is necessary 
to support indexing arbitrary items in the array, so the total memory usage is 
`n + 4` bytes where `n` is the lenght of the array.

## Example
See the [examples/](https://github.com/bbielsa/fera/tree/master/examples) folder for more examples of the fera programming language.

### Hello world
```
data {
    str: byte[14] = "Hello, world!";
}

inline _putsln {
    __org($0)
    >>>>
    [.>]
    ++++++++++
    .
    ----------
    <
    [<]
    <<<
    __ret($0)
}

entry {
    _putsln(str);
}
```

## Usage

### fera compiler
```bash
python3 -m compiler example.fra
```

### bf formatter
```bash
python3 -m formatter example.bf
```