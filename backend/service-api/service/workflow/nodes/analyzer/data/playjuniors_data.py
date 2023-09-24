from service.workflow.nodes.analyzer.data.common_data import gpt_prompt_department_classification_template

department_list = [
    "Kids Activities",
    "Facilities",
    "Guest Relations"
]

department_sublist = {
    "Kids Activities": [
        "Craft",
        "Kids Zone",
        "Story"
    ]
}

activities = department_sublist['Kids Activities']

gpt_prompt_department_classification = gpt_prompt_department_classification_template.replace('__DEPARTMENT_LIST__', '''
Departments with their keywords:
1. Guest Relations: Host, Guest relation, hospitality, frontdesk, counter, guide, explained, help, instructed 
2. Facilities: Housekeeping, maintenance, security
3. Kids Activities
4. Craft
5. Kids Zone
6. Story
''')
