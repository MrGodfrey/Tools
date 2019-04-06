score={"L":0,"W":0,"H":0}

s=input("Enter>")
while s !="quit":
        try:
                score[s]+=1
        except:
                s=input("No Such Name.\nEnter>")
                continue
        print(score)
        s=input("Enter>")
print(score)