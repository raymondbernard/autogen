from ai_pb2 import AI

# Create an instance of AIagent
agent = AI(
    date="2024-01-26",
    message="Sample message",
    system="System X",
    open="Open Y",
    score="Score Z",
    high="High A",
    low="Low B"
)

# Serialize to a byte string
serialized_data = agent.SerializeToString()

print(serialized_data)