import sys

def repeat (s,exclaim):
    result = s*3
    if exclaim == "true":
        result = result + '!!!'
    print (result)

def fibonacci(n):
    a, b = 0, 1
    print(n)
    while(a < n):
        a, b = b, a+b
        print (a)
        
    
        
def main():
    n = int(sys.argv[1])
    fibonacci(n)
    
#   repeat (sys.argv[1],sys.argv[2])
    
if __name__ == "__main__":
    main()

    
    
        
    


    


    
    

