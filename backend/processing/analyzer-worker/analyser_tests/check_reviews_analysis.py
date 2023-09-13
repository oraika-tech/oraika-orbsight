from uuid import UUID

from analyzer.model.structure_data_request import UnstructuredDataRequest
from analyzer.service.text_analysis import review_analysis

data_requests = [
    UnstructuredDataRequest(
        raw_data_id=1,
        raw_text="Manoj from play area guided about offers"
    ),
    UnstructuredDataRequest(
        raw_data_id=2,
        raw_text="Manoj gave us great buy one get one free offer"
    ),
    UnstructuredDataRequest(
        raw_data_id=3,
        raw_text="Bowling was superrrr fun!!"
    ),
    UnstructuredDataRequest(
        raw_data_id=4,
        raw_text="This place visited for the first time and it was good experience there lots of activities for adults also it's better than games having in any mall game zone and also kids sports activities are there so kid can learn football, cricket, swimming, skating etc. For kids toddlers age having more sports game than any other activities,also having lots of eateries and place to click beautiful pictures overall one can visit there for the whole day even if they don't want to do any activity or pay for that can go n sit there watch lots of people kids playing enjoying.."
    ),
    UnstructuredDataRequest(
        raw_data_id=5,
        raw_text="Go-kart is good here. Pulak was really helpful."
    ),
    UnstructuredDataRequest(
        raw_data_id=6,
        raw_text="Front desk santosh helped alot and assisted very professionally"
    ),
    UnstructuredDataRequest(
        raw_data_id=7,
        raw_text="Today we visited atv payal , manash , shrinivas. We played actually care it's very good for parfomenc...."
    ),
    UnstructuredDataRequest(
        raw_data_id=8,
        raw_text="Had so much fun at Play Arena..went with my office team,  best for one day outing 🙌 😁"
    ),
    UnstructuredDataRequest(
        raw_data_id=9,
        raw_text="Had a wonderful visit in playarena. Liked the go karting, laser tag and cricket simulator(Ashish was helpful with cricket simulator)"
    ),
    UnstructuredDataRequest(
        raw_data_id=10,
        raw_text="Bowling was very good. Pavani looked after all the team members very nicely. Thank you very much for the nice hospitality. Overall team experience was excellent!!!"
    ),
    UnstructuredDataRequest(
        raw_data_id=11,
        raw_text="good carnival game nirmala patil  good nature"
    ),
    UnstructuredDataRequest(
        raw_data_id=12,
        raw_text="All the games were fun. Beauti das was a good host for the carnival game."
    ),
    UnstructuredDataRequest(
        raw_data_id=13,
        raw_text="Wall climbing Pranjal and Jyoti extremely supportive and encouraging for each and everyone to climb. Very good person. lovely"
    ),
    UnstructuredDataRequest(
        raw_data_id=14,
        raw_text="Carnival game is super. Beauti Das is so cooperative and helpful."
    ),
    UnstructuredDataRequest(
        raw_data_id=15,
        raw_text="Trompholine park is very nice and staff name manju sunari is very very good and very friendly nature thank you so much mam"
    ),
    UnstructuredDataRequest(
        raw_data_id=16,
        raw_text="Frontdesk Santosh cashier . Good service"
    ),
    UnstructuredDataRequest(
        raw_data_id=17,
        raw_text="Santosh in the cash counter was really helpful"
    ),
    UnstructuredDataRequest(
        raw_data_id=18,
        raw_text="Santosh cashier is very helpful.  Gives the best suggestions available."
    ),
    UnstructuredDataRequest(
        raw_data_id=19,
        raw_text="All the activities are good. My kids had a great fun. I don't like the trampoline activity. It's too small n not maintained well. Food is also good."
    ),
    UnstructuredDataRequest(
        raw_data_id=20,
        raw_text="Great area to hang out with your friends and dear one !! We tried laser play it was awesome"
    ),
    UnstructuredDataRequest(
        raw_data_id=21,
        raw_text="Great to spend time with people here. Awesome management with great attitude! Pranaya,pulak,Tanmay"
    ),
    UnstructuredDataRequest(
        raw_data_id=22,
        raw_text="Nirupam pulak and tanmay and Kishan , really helped, and had crazy fun thanks"
    ),
    UnstructuredDataRequest(
        raw_data_id=23,
        raw_text="Go Karting is very nice expenses Pulak is very half"
    ),
    UnstructuredDataRequest(
        raw_data_id=24,
        raw_text="The service is really good. Ms Apeksha was very helpful while guiding about the games and recreations."
    ),
    UnstructuredDataRequest(
        raw_data_id=25,
        raw_text="enjoyed go karting pulak tonomay rajesh hospitalized us well"
    ),
    UnstructuredDataRequest(
        raw_data_id=26,
        raw_text="Nice game especially bowling staff suhana"
    ),
    UnstructuredDataRequest(
        raw_data_id=27,
        raw_text="It was a wonderful experience. Thank you Miss Gonemai for the great guidance and support through out the experience."
    ),
    UnstructuredDataRequest(
        raw_data_id=28,
        raw_text="Play Arena in Bengaluru offers a vibrant and diverse entertainment experience that caters to a wide range of interests. The facility boasts an impressive array of indoor and outdoor games, making it a fantastic destination for friends, families, and even corporate outings. The indoor gaming section is well-equipped with a variety of options, including bowling alleys, pool tables, and a selection of arcade games. This ensures that visitors have plenty of engaging activities to choose from, regardless of their preferences. The atmosphere is lively, and the staff is generally friendly and helpful, enhancing the overall experience. The outdoor section of Play Arena is equally enticing. The adventure sports offerings, such as go-karting, paintball, and rock climbing, add a thrilling dimension to the venue. These activities provide an excellent opportunity for team-building or simply enjoying an adrenaline rush with friends. One area where Play Arena could improve is its maintenance. Some visitors have noted occasional issues with equipment and facilities. Moreover, during peak hours, the place can get crowded, leading to longer waiting times for popular games and activities. In terms of dining, Play Arena has an on-site restaurant that serves a decent selection of food and beverages. However, the quality of the menu items can be inconsistent, and prices are relatively high compared to other eateries in the city. In summary, Play Arena offers an extensive range of indoor and outdoor entertainment options, making it a versatile destination for groups of all sizes. Despite some maintenance and dining drawbacks, the overall experience is enjoyable, making it a worthwhile spot for a day of fun and recreation."
    )
]


def check_tenant(tenant_id):
    analysis = [el.dict() for el in review_analysis(tenant_id, data_requests)]
    for el in analysis:
        print(f'{el["raw_data_id"]}, {el["emotion"]}, {el["tags"]}, {el["terms"]}')


# Careful ! Single test run cost 0.01 USD
check_tenant(UUID('02ddd60c-2d58-47cc-a445-275d8e621252'))
check_tenant(UUID('b6d5a44a-4626-491a-8fc0-3a11344d97f7'))
