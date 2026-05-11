state = {
    "user_input": "hello",
    "actions": []
}

new_state = {
    **state
}
print(new_state)
#####################
state2 = {
    "user_input": "hello",
    "actions": []
}
new_state2 = {
    **state,
    "actions": [{"intent":"joke"}]
}

print(new_state2)

new_state3 = {
    **new_state2,
    "user":"alpha"
}
#################
#Example with list
num = [1,2,3]
new_num = [*num,4,5]
print(new_num)

##########
#packing
def add_num(*args):
    print(args)
add_num(1,2,3,4)