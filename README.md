## Names and Stevens Login
Ramanish Reddy Eeda reeda@stevens.edu
Chih-Chao Wang cwang126@stevens.edu

## Github Repo
[Repo](https://github.com/Eeda-RR/CS-515-A-FOC-PROJECT-2)

## Estimate of hours
Around 7 days were spent on this project.

## How we tested our code
Initially, we tested our code manually. Once we completed the baseline features, we wrote a single file [tests.py](./tests.py) for testing and continuously added relevant test cases to ensure the features worked correctly. Additionally, we created a [simple file](.github/workflows/github-action.yml)  to activate Github Actions and confirm that the tests worked well. Made use of doctests for testing.

## Bugs and Issues that could not be resolved
No

## An example of difficult issue how I resolved
After tokenise the input, the main difficulty we faced is handling precedence of various operators. To handle it we made use of stacks and converted it from infix to postfix. And this approach helped us to have a simpler evaluation logic as we already have postfix notation which already took care of precedence.

And also while working having the doctests helped us to know if any new piece of code that we r introducing as part of extensions or baseline functionality isn't breaking the existing logic.

## Extensions
- [Op-equals](#op-equals)
- [Relational Operations](#relational-operations)
- [Boolean Operations](#boolean-operations)
- [Comments](#comments)


### Op-equals
Implement `op=` for every binary operation op. x op= e is equivalent to x = x op (e) 
```python
    x = 2
    y = 5
    print x += -1
    print y *= 2
    print y /= 2
                      
    1.0
    10.0
    5.0
```
### Relational Operations
```python
    x = 100
    y = 5
    print x == y, x <= 100, y >= 4 
    print x != y, x != 100          
    print x > 101, y < 4
    0 1 1
    1 0
    0 0
```
### Boolean Operations
Since we implement op-equals extension, we include **op=** in Boolean Operations as well.
```python
    x = 1
    y = 2
    print x && y, x || 0, y != 1, !x
    print x != 0, x ||= 0, y &&= 1
    1 1 1 0
    1 1 1
```
### Comments
Multi line comments being with `/*` and end with `*/`. The `#` character introduces a single line comment.
```python
    x = 1
    /*
     
    x = 2
    y = 3
    
    */
    y = 4
    # print 0
    print x , y
    1.0 4.0
```
