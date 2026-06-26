import sys

def solve_staircase(n):
    if n == 0:
        return 1
    if n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

if __name__ == "__main__": 

    n = int(sys.argv[1])
    result = solve_staircase(n)
    print(f"Number of ways to climb {n} steps: {result}")
    
