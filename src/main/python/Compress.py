'''
Prompt
Everyday we look at a lot of URLs, for example in our log files from client request.
We want our data science team to perform analytics and machine learning, but:
   1. we want to preserve the privacy of the user, but without completely obfuscating/hashing the URLs and making them useless,
   2. we simply have a lot of data and we want to reduce our storage/processing costs
In real world, we may solve this with hashing; due to the time constraints of the interview, we use numeronyms instead of compress Strings.
Example starter code
String compress(String s) {
   // requirement 1, 2, etc
   String compressed_s = fx(s);
   return compressed_s;
}
Part 1
Given a String, split it into "major parts" separated by special char '/'.
For each major part that's split by '/', we can further split it into "minor parts" separated by '.'.
We assume the given Strings:
   - Only have lower case letters and two separators ('/', '.').
   - Have no empty minor parts (no leading / trailing separators or consecutive separators like "/a", "a/", "./..").
   - Have >= 3 letters in each minor part.
Example:
   stripe.com/payments/checkout/customer.maria
   s4e.c1m/p6s/c6t/c6r.m3a
Part 2
In some cases, major parts consists of dozens of minor parts, that can still make the output String large.
For example, imagine compressing a URL such as "section/how.to.write.a.java.program.in.one.day".
After compressing it by following the rules in Part 1, the second major part still has 9 minor parts after compression.
Task:
Therefore, to further compress the String, we want to only keep m (m > 0) compressed minor parts from Part1 within each major part.
If a major part has more than m minor parts, we keep the first (m-1) minor parts as is, but concatenate the first letter of the m-th minor part and the last letter of the last minor part with the count
'''


class Compress:
    def compress(self, s, m=None):
        if m is None:
            return self._compress_part1(s)
        else:
            return self._compress_part2(s, m)
    
    def _compress_part1(self, s):
        result = []
        majors = s.split('/')
        
        for i, major in enumerate(majors):
            if i > 0:
                result.append('/')
            
            minors = major.split('.')
            for j, minor in enumerate(minors):
                if j > 0:
                    result.append('.')
                result.append(self._compress_minor(minor))
        
        return ''.join(result)
    
    def _compress_part2(self, s, m):
        result = []
        majors = s.split('/')
        
        for i, major in enumerate(majors):
            if i > 0:
                result.append('/')
            
            minors = major.split('.')
            
            c1 = ''
            c2 = ''
            length = 0
            
            for j, minor in enumerate(minors):
                if j < m - 1:
                    if j > 0:
                        result.append('.')
                    result.append(self._compress_minor(minor))
                    continue
                
                if j == m - 1:
                    c1 = minor[0]
                    length -= 1
                
                if j == len(minors) - 1:
                    c2 = minor[-1]
                
                length += len(minor) + 1
            
            if length > 0:
                if m > 1:
                    result.append('.')
                result.append(c1 + str(length - 2) + c2)
        
        return ''.join(result)
    
    def _compress_minor(self, s):
        length = len(s)
        return s[0] + str(length - 2) + s[-1]


def run():
    comp = Compress()
    print(comp.compress("stripe.com/payments/checkout/customer.maria"))
    print(comp.compress("stripe.com/payments/checkout/customer.maria", 1))
    print(comp.compress("section/how.to.write.a.java.program.in.one.day"))
    print(comp.compress("section/how.to.write.a.java.program.in.one.day", 3))


if __name__ == "__main__":
    run()