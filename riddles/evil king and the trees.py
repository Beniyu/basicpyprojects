correct=0
wrong=0

def evilkingandtrees(A,B):
    global correct
    global wrong
    if A+B==18 or A+B==20:
        #Setting up variables that both A and B can know
        definiteA=20
        definiteB=0
        #Important information each person knows
        mindofA=[A,definiteB,definiteA]
        mindofB=[B,definiteA,definiteB]
        #Beginning of day counter
        days=0
        while True:
            days+=1
            print("Day {} -".format(days))
            #A is asked the question, if min B + A is more than 18, it has to be 20
            if mindofA[0]+mindofA[1]>18:
                print("A: *At minimum, we can make {}*".format(mindofA[0]+mindofA[1]))                
                print("A: It must be 20!")
                guess=20
                break
            #A passes if he can't answer it
            else:
                #Maximum possible A is decreased
                print("A: I pass")
                mindofB[1]-=2
                mindofA[2]-=2
                print("B: *If he was {} or {}, he would have known the answer was 20 as my minimum is {} so he's at most {}*".format(mindofB[1]+1,mindofB[1]+2,mindofB[2],mindofB[1]))
            #B is asked the question, if max A + B is lower than 20, it has to be 18
            if mindofB[0]+mindofB[1]<20:
                print("B: *At maximum, we can make {}*".format(mindofB[0]+mindofB[1]))            
                print("B: It must be 18!")
                guess=18
                break
            #B passes if he can't answer it
            else:
                #Minimum possible B is increased
                print("B: I pass")
                mindofA[1]+=2
                mindofB[2]+=2
                print("A: *If he was {} or {}, he would have known the answer was 18 as my maximum is {} so he's at least {}*".format(mindofA[1]-2,mindofA[1]-1,mindofA[2],mindofA[1]))
                print("") 
        #loop breaks when guess is given, answer is checked
        if guess==A+B:
            print("Logician: Correct! A was {} and B was {}.\n\n".format(A,B))       
            correct+=1
        else:
            print("Logician: Incorrect! A was {} B was {} so together you made {}.\n\n".format(A,B,A+B))
            wrong+=1
            
for i in range(9,11):
    for j in range(0,i*2):
        evilkingandtrees(j,i*2-j)
            
print("Results:\n{} correct, {} wrong".format(correct,wrong))
            
