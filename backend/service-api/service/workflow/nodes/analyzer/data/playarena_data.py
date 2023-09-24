from service.common.utils import merge_dict_arrays_comp
from service.workflow.nodes.analyzer.data.common_data import gpt_prompt_department_classification_template

department_list = [
    "Cashier",
    "Guest Relations",
    "Sales",
    "Booking Team",
    "Events",
    "Food & Beverages",
    "Juniors",
    "Sports",
    "Facilities",
    "Housekeeping",
    "Maintenance",
    "Security",
    "Medical",
    "Food and Beverages",
    "Indoor Activities",
    "Outdoor Activities"
]

department_sublist = {
    "Indoor Activities": [
        "Bowling",
        "Laser Tag",
        "Table Games",
        "Car Simulator",
        "VR Games",
        "Table Games",
    ],
    "Outdoor Activities": [
        "Gokart",
        "Wall Climbing",
        "Archery",
        "Rope Course",
        "Rocket Ejector",
        "7D Theatre",
        "ATV",
        "Paintball",
        "Exit 404",
        "Laser Maze",
        "Trampoline Park",
        "Carnival Games",
        "Cricket Simulator",
    ]
}

activities = merge_dict_arrays_comp(department_sublist)

gpt_prompt_department_classification = gpt_prompt_department_classification_template.replace('__DEPARTMENT_LIST__', '''
Departments with their keywords:
- Gokart
- Wall Climbing
- Archery
- Rope Course
- Rocket Ejector
- 7D Theatre
- ATV
- Paintball
- Exit 404
- Laser Maze
- Trampoline Park
- Carnival Games
- Cricket Simulator
- Bowling
- Laser Tag
- Shooting
- Car Simulator
- VR Games
- Table Games
- Indoor Activities
- Outdoor Activities
- Cashier: Counter, frontdesk, card loading, cashier
- Guest Relations: Host, Guest relation, hospitality, frontdesk, counter, guide, explained, help, instructed 
- Sales: Booking team, information, sales, calls
- Events: Coordination, events, decoration, artist
- Food and Beverages: Food, dish, host for f&b, kitchen, menu
- Juniors: Below 12 years, soft play, bouncies, sandpit, craft, art, kids talk, little gym, workshop 
- Sports: Basketball, cricket, courts, field, swimming, football, squash, badminton, karate, skating
- Facilities: Housekeeping, maintenance, security
- Medical: Medical, nurse, first aid
''')
