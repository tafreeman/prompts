<p>I'd like suggestions for optimizing this brute force solution to <a href="http://projecteuler.net/index.php?section=problems&amp;id=1">problem 1</a>.  The algorithm currently checks every integer between 3 and 1000.  I'd like to cut as many unnecessary calls to <code>isMultiple</code> as possible:</p>

<pre><code>'''
If we list all the natural numbers below 10 that are multiples of 3 or 5, 
we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
'''

end = 1000

def Solution01():
    '''
        Solved by brute force
        #OPTIMIZE
    '''
    sum = 0
    for i in range(3, end):
        if isMultiple(i):
            sum += i 
    print(sum)

def isMultiple(i):
    return (i % 3 == 0) or (i % 5 == 0)
</code></pre>
