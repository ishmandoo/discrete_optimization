import numpy as np

george_before = [7, 8, 8, 8, 8, 7, 9, 7, 10, 5, 9]	
paul_before = [10, 5, 6, 9, 7, 10, 1, 5, 6, 10, 9]	
ringo_before = [4, 5, 3, 3, 5, 5, 2, 5, 4, 8, 6]	
john_before = [8, 7, 6, 7, 8, 7, 7, 5, 9, 7, 6]	


george_after = [9, 9, 10, 7, 9, 10, 6, 9, 8, 8, 7]
paul_after = [8, 5, 8, 10, 10, 8, 8, 6, 6, 2, 7]
ringo_after = [6, 5, 5, 3, 9, 4, 7, 7, 7, 10, 9]
john_after = [6, 7, 8, 9, 10, 10, 9, 7, 8, 8, 7]


before = np.array([george_before, paul_before, ringo_before, john_before])
after = np.array([george_after, paul_after, ringo_after, john_after])

data = np.array([before, after])

print("george", "paul", "ringo", "john")
print(np.median(before, axis=1))
print(np.median(after, axis=1))
print(np.std(before, axis=1))
print(np.std(after, axis=1))



emai: @ pjhil push git https://youtu.be/wfuFEfxkY_I

D3 Chicken with mixed vegs
Boneless spare ribs combo w/ wr
Chicken with broc w/ wr
Pokr looo