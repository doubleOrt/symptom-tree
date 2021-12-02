import symptomtree

tree = symptomtree.buildtree('data/symptom-tree-data.csv')
user_form = tree.get_user_form()

print(user_form)
