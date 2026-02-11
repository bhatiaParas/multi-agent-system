"""Test script to demonstrate different math tool calls with step-by-step results."""
from sub_agents.math_agent import MathAgent

agent = MathAgent()

print('=' * 70)
print('🧮 MATH AGENT - DIFFERENT TOOL CALLS')
print('=' * 70)

# Test 1: Add
print('\n▶️ TEST 1: ADD Operation')
result = agent.process('add', [50, 75])

# Test 2: Subtract
print('\n▶️ TEST 2: SUBTRACT Operation')
result = agent.process('subtract', 100, 25)

# Test 3: Multiply
print('\n▶️ TEST 3: MULTIPLY Operation')
result = agent.process('multiply', [10, 20, 2])

# Test 4: Divide
print('\n▶️ TEST 4: DIVIDE Operation')
result = agent.process('divide', 144, 12)

# Test 5: Power
print('\n▶️ TEST 5: POWER Operation')
result = agent.process('power', 2, 8)  # 2 to the power of 8

# Test 6: Square Root
print('\n▶️ TEST 6: SQUARE ROOT Operation')
result = agent.process('square_root', 144)

# Test 7: Average (for comparison)
print('\n▶️ TEST 7: AVERAGE Operation')
result = agent.process('average', [10, 20, 30, 40, 50])

# Test 8: Convert Seconds (Step-by-step)
print('\n▶️ TEST 8: CONVERT SECONDS Operation (Step-by-step)')
result = agent.process('convert_seconds', 56751)
if 'steps' in result:
    print('\n[MATH AGENT] 📋 STEP-BY-STEP SOLUTION:')
    for step in result['steps']:
        print(f'             {step}')
    if 'breakdown' in result:
        print(f'[MATH AGENT] 📊 BREAKDOWN: {result["breakdown"]}')

print('\n' + '=' * 70)
print('✅ All Math Agent tool calls completed!')
print('=' * 70)
