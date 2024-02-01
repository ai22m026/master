from databallpy import get_match, get_open_match
import pickle

match = get_open_match(verbose=False)

print(match)

print(type(match.tracking_data))
print(match.tracking_data.columns)
print(len(match.tracking_data))
print(match.event_data.columns)
print(len(match.event_data))

# Pickle the variable to a file
with open('match.pkl', 'wb') as file:
    pickle.dump(match, file)
